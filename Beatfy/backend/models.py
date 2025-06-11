from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# Secondary table for many-to-many relationship between playlists and songs
playlist_songs = db.Table('playlist_songs',
                          db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
                          db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
                          )

class Admin(db.Model):
    __tablename__='admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    adminname = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    def get_id(self):
        return str(self.admin_id)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False) 
    password = db.Column(db.String(80), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_creator = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    playlists = db.relationship('Playlist', backref='user', lazy=True)

class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    songs = db.relationship('Song', back_populates='album', lazy=True, cascade="all, delete-orphan")

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text, nullable=True)
    song_url = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    no_of_ratings = db.Column(db.Integer, default=0)
    ratings = db.Column(db.Float, default=0.0)
    album = db.relationship('Album', back_populates='songs', lazy=True)


class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    songs = db.relationship('Song', secondary=playlist_songs)
