from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# --- Tables d'Association (Many-to-Many) ---
song_genre_association = Table(
    'song_genre_association', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

# --- Modèles (Classes de la Base de Données) ---

class User(Base):
    __tablename__ = "users"
    
    # UTILISATEUR
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) 
    email = Column(String, unique=True, index=True)    
    password = Column(String)                          

class Artist(Base):
    __tablename__ = "artists"
    
    # ARTISTE
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)        
    biography = Column(String)               
    avatar_url = Column(String)             
    
    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", back_populates="artist")

class Genre(Base):
    __tablename__ = "genres"
    
    # GENRE
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True) #
    description = Column(String)                   
    
    songs = relationship("Song", secondary=song_genre_association, back_populates="genres")

class Album(Base):
    __tablename__ = "albums"
    
    # ALBUM
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)                   
    release_date = Column(Date)             
    cover_image_url = Column(String)         
    
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="albums")
    
    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan") 

class Song(Base):
    __tablename__ = "songs"
    
    # MORCEAU
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)                   
    duration = Column(Integer)              
    
    # Relations
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="songs") 
    
    album_id = Column(Integer, ForeignKey("albums.id"))
    album = relationship("Album", back_populates="songs") 
    
    # Genres
    genres = relationship("Genre", secondary=song_genre_association, back_populates="songs") 