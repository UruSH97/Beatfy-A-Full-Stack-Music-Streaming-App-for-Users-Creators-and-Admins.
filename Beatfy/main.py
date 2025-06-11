from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from backend.models import db, Admin
from backend.api import cache
from backend.worker import celery
from backend.task import *
from datetime import timedelta
import os

def create_app():
  app = Flask(__name__)

  basedir = os.path.abspath(os.path.dirname(__file__))
    
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"BeatfyDB.sqlite3")
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = "SecretOfBeatfy"
  app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'src/assets/audio')

  app.config["CACHE_TYPE"] = "redis"
  app.config['CACHE_REDIS_DB'] = 0
  app.config['CACHE_REDIS_HOST'] = "localhost"
  app.config['CACHE_REDIS_PORT'] = 6379
  app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"  
  app.config['CACHE_DEFAULT_TIMEOUT'] = 300

  CORS(app)           
  api = Api(app)
  db.init_app(app)
  cache.init_app(app)
  app.config['JWT_SECRET_KEY'] = 'secret'
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 10)
  JWTManager(app)
  app.app_context().push()
  return app, api

app, api = create_app()
app.app_context().push()

@app.before_request
def clear_cache_for_non_get():
    if request.method != 'GET':
      cache.clear()
      pass

from backend.api import *
api.add_resource(AdminLoginResource, '/api/admin-login')
api.add_resource(CreatorLoginResource, '/api/creator-login')
api.add_resource(LoginResource, '/api/user-login')
api.add_resource(RegistrationResource, '/api/user-register')

api.add_resource(SongAPI, '/api/song', '/api/add-song', '/api/song/<int:id>')
api.add_resource(AlbumAPI, '/api/album', '/api/add-album', '/api/album/<int:id>')
api.add_resource(PlaylistAPI, '/api/playlist', '/api/playlist/<int:id>', '/api/playlist/<int:id>/<int:song_id>',)
api.add_resource(SongSearchAPI, '/api/search')
api.add_resource(AdminAPI, '/api/details')
api.add_resource(UserAPI, '/api/creator', '/api/creator/<int:id>')

    
def add_admin():
  query = Admin.query.all()
  if len(query) == 0:
    admin = Admin(email = "admin@beatfy.com", password = "1010", adminname = 'Admin')
    db.session.add(admin)
    db.session.commit()
    print("Admin added.")


if __name__ == '__main__':
  db.create_all()
  add_admin()
  app.run(debug=True)