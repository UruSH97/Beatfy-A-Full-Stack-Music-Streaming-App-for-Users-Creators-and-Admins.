from flask import request, current_app as app
from flask_restful import Resource, abort, marshal, fields
from flask_caching import Cache
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import db, User, Admin, Album, Song, Playlist
from sqlalchemy import func
import datetime
import secrets
import os

cache = Cache()

song_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'lyrics': fields.String,
    'artist': fields.String,
    'song_url': fields.String,
    'album': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'artist': fields.String,
    }),
    'ratings': fields.Float(),
}

album_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'artist': fields.String,
    'user_id': fields.Integer(attribute='user_id'), 
    'songs': fields.List(fields.Nested(song_fields)), 
}

playlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'user_id': fields.Integer,
    'songs': fields.List(fields.Nested(song_fields)),
}

user_fields = {
    'id': fields.Integer(attribute='user_id'), 
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'is_creator': fields.Boolean,
    'is_blocked': fields.Boolean,
}

def save_file(file):
    hex_name = secrets.token_hex(6)
    _, file_ext = os.path.splitext(file.filename)
    file_name = hex_name + file_ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path) 
    return file_name



class AdminLoginResource(Resource):
    def post(self):
        email = request.get_json().get('email')
        password = request.get_json().get('password')

        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            abort(404, message='Incorrect admin email!') 
        if admin.password != password:
            abort(400, message='Incorrect password. Please try again')

        token = create_access_token(identity={'id': admin.admin_id, 'role': 'admin'})
        return {'token': token, 'message': 'Admin logged in successfully'}, 200

class RegistrationResource(Resource):
    def post(self):
        name = request.get_json().get('username')
        email = request.get_json().get('email')
        password = request.get_json().get('password')

        if not name or not email or not password:
            abort(400, message='Username, email, and password are required.') 

        user = User.query.get(email)
        if user:
            abort(400, message='User already exists') 
        new_user = User(username=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201
       

class LoginResource(Resource):
    def post(self):
        email = request.get_json().get('email')
        password = request.get_json().get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, message='User not found!') 
        if user.password != password:
            abort(400, message='Incorrect password. Please try again')

        user.last_login = datetime.datetime.now()
        db.session.commit()
        token = create_access_token(identity={'id': user.user_id, 'role': 'user'})
        return {'token': token, 'message': 'User logged in successfully'}, 200


class CreatorLoginResource(Resource):
    def post(self):
        email = request.get_json().get('email')
        password = request.get_json().get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, message='User not found!') 
        if user.password != password:
            abort(400, message='Incorrect password. Please try again')

        if user.is_blocked:
            abort(403, message='Creator account is blocked.')
                    
        if not user.is_creator:
            user.is_creator = True

        user.last_login = datetime.datetime.now()
        db.session.commit()
        token = create_access_token(identity={'id': user.user_id, 'role': 'creator'})
        return {'token': token, 'message': 'Creator logged in successfully'}, 200        

        
class AlbumAPI(Resource):
    @jwt_required() 
    @cache.cached(120)
    def get(self):
        current_user = get_jwt_identity()
        if request.args and 'id' in request.args:
            id = int(request.args.get('id'))
            album = Album.query.get(id)
            if not album:
                abort(404, message='Album not found')
            return {'album': marshal(album, album_fields)}, 200
        else:
            if current_user.get('role') == 'creator':
                albums = Album.query.filter_by(user_id = current_user.get('id')).all()
            else:
                albums = Album.query.all()
        return {'albums': marshal(albums, album_fields)}, 200
        
    @jwt_required()    
    def post(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'creator':
            return {'message': 'Unauthorized access! Creator login required.'}, 403
        
        name = request.get_json().get('name')
        artist = request.get_json().get('artist')

        if not name or not artist:
            abort(400, message='Album name and artist name are required.') 

        new_album = Album(name=name, artist=artist, user_id=current_user.get('id'))
        db.session.add(new_album)
        db.session.commit()
        return {'message': 'Album added successfully'}, 201

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'creator':
            return {'message': 'Unauthorized access! Creator login required.'}, 403
        
        album = Album.query.filter_by(id=id, user_id=current_user.get('id')).first()
        if not album:
            abort(404, message='Album not found')

        name = request.get_json().get('name')
        artist = request.get_json().get('artist')

        if not name or not artist:
            abort(400, message='Album name and artist name are required.')  

        album.name = name
        album.artist = artist
        db.session.commit()
        return {'message': 'Album updated successfully'}, 200
        
    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        album = Album.query.get(id)
        if not album:
            abort(404, message='Album not found')

        if current_user.get('role') == 'creator' and album.user_id != current_user.get('id'):
            abort(404, message='Album not found')

        db.session.delete(album)
        db.session.commit()
        return {'message': 'Album removed successfully'}, 200


class SongAPI(Resource):
    @jwt_required()
    @cache.cached(120)
    def get(self):
        current_user = get_jwt_identity()
        if request.args and 'id' in request.args:
            id = int(request.args.get('id'))
            song = Song.query.get(id)
            if not song:
                abort(404, message='Song not found')
            return {'song': marshal(song, song_fields)}, 200
        
        else:
            if current_user.get('role') == 'creator':
                songs = Song.query.filter_by(user_id = current_user.get('id')).all()
            else:
                songs = Song.query.all()
            return {'songs': marshal(songs, song_fields)}, 200

    @jwt_required()        
    def post(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'creator':
            return {'message': 'Unauthorized access! Creator login required.'}, 403
        
        name = request.form.get('name')
        artist = request.form.get('artist')
        lyrics = request.form.get('lyrics')
        album_id = request.form.get('album_id') 

        if not name or not artist:
            abort(400, message='Song name and artist name are required.') 

        audio_name = 'BS.mp3'
        if request.files.get('song_file'):
            file = request.files.get('song_file')
            print(file.filename)
            if not file.filename.endswith('.mp3'):
                abort(400, message='Please upload a valid MP3 file.')
            audio_name = save_file(file)

        new_song = Song(name=name, artist=artist, lyrics=lyrics, album_id=int(album_id),
                        song_url=audio_name, user_id=current_user.get('id'))
        db.session.add(new_song)
        db.session.commit()
        return {'message': 'Song uploaded successfully'}, 201

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'creator':
            return {'message': 'Unauthorized access! Creator login required.'}, 403

        song = Song.query.filter_by(id=id, user_id=current_user.get('id')).first()
        if not song:
            abort(404, message='Song not found')

        name = request.form.get('name')
        artist = request.form.get('artist')
        lyrics = request.form.get('lyrics')
        album_id = request.form.get('album_id') 

        if not name or not artist:
            abort(400, message='Song name and artist name are required.') 

        song.name = name
        song.artist = artist
        song.lyrics = lyrics
        song.album_id = album_id
        db.session.commit()
        return {'message': 'Song updated successfully'}, 200

    @jwt_required()
    def patch(self, id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {'message': 'Unauthorized access! User login required.'}, 403

        song = Song.query.get(id)
        if not song:
            abort(404, message='Song not found.')

        points = request.get_json().get('rating')
        old_rating = song.ratings * song.no_of_ratings
        new_rating = round((old_rating + float(points)) / (song.no_of_ratings + 1), 1)

        song.ratings = new_rating
        song.no_of_ratings += 1
        db.session.commit()
        return {'message': 'Thank you for rating!'}, 200

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        song = Song.query.get(id)
        if not song:
            abort(404, message='Song not found')     

        if current_user.get('role') == 'creator' and song.user_id != current_user.get('id'):
            abort(404, message='Song not found')
        
        db.session.delete(song)
        # song.delete_with_playlists()
        db.session.commit()
        return {'message': 'Song removed successfully'}, 200

class SongSearchAPI(Resource):
    def get(self):
        query = request.args.get('q')
        query_string = f'%{query}%'
        songs = Song.query.filter((func.lower(Song.name).like(query_string)) | (func.lower(Song.artist).like(query_string))).all()
        return {'songs': marshal(songs, song_fields)}, 200

class PlaylistAPI(Resource):
    @jwt_required()
    @cache.cached(120)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {'message': 'Unauthorized access! User login required.'}, 403

        if request.args and 'id' in request.args:
            id = int(request.args.get('id'))
            playlist = Playlist.query.filter_by(id = id, user_id = current_user.get('id')).first()
            if not playlist:
                abort(404, message='Playlist not found.')

            return {'playlist': marshal(playlist, playlist_fields)}, 200

        playlists = Playlist.query.filter_by(user_id = current_user.get('id')).all()
        return {'playlists': marshal(playlists, playlist_fields)}, 200
    
    @jwt_required() 
    def post(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {'message': 'Unauthorized access! User login required.'}, 403

        name = request.get_json().get('name')

        if not name:
            abort(400, message='Please enter a valid name.')

        new_playlist = Playlist(name = name.strip(), user_id = current_user.get('id'))
        db.session.add(new_playlist)
        db.session.commit()
        return {'message': 'Playlist created successfully.'}, 201

    @jwt_required()
    def put(self, id, song_id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {'message': 'Unauthorized access! User login required.'}, 403

        playlist = Playlist.query.filter_by(id = id, user_id = current_user.get('id')).first()
        if not playlist:
            abort(400, message='Playlist not found.')

        song = Song.query.filter_by(id = song_id).first()
        if not song:
            abort(404, message='Song not found') 

        if song in playlist.songs:
            abort(400, message="Song is already in the playlist!")

        playlist.songs.append(song)
        db.session.commit()
        return {'message': 'Added to Playlist.'}, 200

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {'message': 'Unauthorized access! User login required.'}, 403

        playlist = Playlist.query.get(id)
        if not playlist:
            abort(400, message='Playlist not found.')
        
        if playlist.user_id != current_user.get('id'):
            abort(400, message='Playlist not found.')

        db.session.delete(playlist)
        db.session.commit()
        return {'message': 'Playlist deleted successfully.'}, 200
    
class AdminAPI(Resource):
    @jwt_required()
    @cache.cached(120)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {'message': 'Unauthorized access! Admin login required.'}, 403
        

        total_songs = Song.query.count()
        total_albums = Album.query.count()
        total_users = User.query.count()
        total_playlists = Playlist.query.count()
        total_creators = User.query.filter_by(is_creator=True).count()

        top_songs = Song.query.order_by(Song.ratings.desc()).limit(5).all()
        top_songs_data = [ {'name': song.name, 'rating': song.ratings, 'artist': song.artist} for song in top_songs ]
        details = {
            'songs': total_songs,
            'albums': total_albums,
            'users': total_users,
            'creators': total_creators,
            'top_songs': top_songs_data,
            "playlists": total_playlists
        }
        return {'details': details}, 200
    
class UserAPI(Resource):
    @jwt_required()
    @cache.cached(120)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {'message': 'Unauthorized access! Admin login required.'}, 403
        
        creators = User.query.filter_by(is_creator=True).all()
        return {'creators': marshal(creators, user_fields)}, 200
    
    @jwt_required()
    def post(self, id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {'message': 'Unauthorized access! Admin login required.'}, 403
        
        creator = User.query.filter_by(user_id=id, is_creator=True).first()
        if not creator:
            abort(404, message='Creator not found')

        creator.is_blocked = not creator.is_blocked
        db.session.commit()
        return {'message': 'Creator status updated successfully'}, 200
    


        