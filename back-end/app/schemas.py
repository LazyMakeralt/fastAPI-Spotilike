from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import List, Optional

# --- Configuration Globale pour SQLAlchemy (Pydantic V2) ---
# Ceci remplace la classe interne 'Config'
SQLA_CONFIG = {
    'from_attributes': True
}

# --- Genres ---
class GenreBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None

class GenreCreate(GenreBase): 
    pass
    
class Genre(GenreBase):
    id: int
    model_config = SQLA_CONFIG # Utilisation du dictionnaire de configuration

# --- Artists ---
class ArtistBase(BaseModel):
    name: str = Field(..., max_length=100)
    biography: Optional[str] = None
    avatar_url: Optional[str] = None

class ArtistCreate(ArtistBase): 
    pass
    
class Artist(ArtistBase):
    id: int
    model_config = SQLA_CONFIG

# --- Songs (Morceaux) ---
class SongBase(BaseModel):
    title: str = Field(..., max_length=100)
    duration: int = Field(..., description="Duration in seconds")
    artist_id: int
    album_id: int

class SongCreate(SongBase):
    genre_ids: List[int] # IDs des genres à lier

class Song(SongBase):
    id: int
    genres: List[Genre] = [] 
    model_config = SQLA_CONFIG

# --- Albums ---
class AlbumBase(BaseModel):
    title: str = Field(..., max_length=150)
    release_date: date
    artist_id: int
    cover_image_url: Optional[str] = None

class AlbumCreate(AlbumBase): 
    pass

class Album(AlbumBase):
    id: int
    songs: List[Song] = []
    model_config = SQLA_CONFIG

# --- Users ---
class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr

class UserSignup(UserBase):
    password: str = Field(..., min_length=6) # SANS HASHAGE

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    model_config = SQLA_CONFIG

# --- JWT Token ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None