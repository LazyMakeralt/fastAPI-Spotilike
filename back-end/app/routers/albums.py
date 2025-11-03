from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database.database import get_db
from ..database import models
from .. import schemas
from .users import get_current_user 

def create_router():
    router = APIRouter()
    
    # ------------------ ALBUMS ------------------

    # 1. GET /api/albums: Récupère la liste de tous les albums
    @router.get("/albums", response_model=List[schemas.Album])
    def get_all_albums(db: Session = Depends(get_db)):
        albums = db.query(models.Album).options(
            joinedload(models.Album.artist),
            joinedload(models.Album.songs).joinedload(models.Song.genres)
        ).all()
        return albums

    # 2. GET /api/albums/:id: Récupère les détails de l'album précisé par :id
    @router.get("/albums/{album_id}", response_model=schemas.Album)
    def get_album_details(album_id: int, db: Session = Depends(get_db)):
        album = db.query(models.Album).options(
            joinedload(models.Album.artist),
            joinedload(models.Album.songs).joinedload(models.Song.genres)
        ).filter(models.Album.id == album_id).first()
        
        if not album:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
        return album

    # 8. POST /api/albums: Ajout d'un album
    @router.post("/albums", response_model=schemas.Album, status_code=status.HTTP_201_CREATED)
    def create_album(album_data: schemas.AlbumCreate, db: Session = Depends(get_db)):
        artist = db.query(models.Artist).filter(models.Artist.id == album_data.artist_id).first()
        if not artist:
            raise HTTPException(status_code=400, detail="Artist not found")

        new_album = models.Album(**album_data.model_dump())
        db.add(new_album)
        db.commit()
        db.refresh(new_album)
        
        return new_album

    # 11. PUT /api/albums/:id: Modification de l'album précisé par :id
    @router.put("/albums/{album_id}", response_model=schemas.Album)
    def update_album(album_id: int, album_data: schemas.AlbumCreate, db: Session = Depends(get_db)):
        album = db.query(models.Album).filter(models.Album.id == album_id)
        if not album.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
        
        album.update(album_data.model_dump())
        db.commit()
        
        return album.first()
        
    # 14. DELETE /api/albums/:id: Suppression de l'album précisé par :id (Protégé par JWT)
    @router.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT, 
                   dependencies=[Depends(get_current_user)])
    def delete_album(album_id: int, db: Session = Depends(get_db)):
        album = db.query(models.Album).filter(models.Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
        
        db.delete(album)
        db.commit()
        return
        
    # ------------------ SONGS (MORCEAUX) ------------------

    # 3. GET /api/albums/:id/songs: Récupère les morceaux de l'album précisé par :id
    @router.get("/albums/{album_id}/songs", response_model=List[schemas.Song])
    def get_songs_by_album(album_id: int, db: Session = Depends(get_db)):
        songs = db.query(models.Song).filter(models.Song.album_id == album_id).options(
            joinedload(models.Song.artist),
            joinedload(models.Song.genres)
        ).all()
        
        if not songs and not db.query(models.Album).filter(models.Album.id == album_id).first():
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
             
        return songs
        
    # 9. POST /api/albums/:id/songs: Ajout d'un morceau dans l'album précisé par :id
    @router.post("/albums/{album_id}/songs", response_model=schemas.Song, status_code=status.HTTP_201_CREATED)
    def add_song_to_album(album_id: int, song_data: schemas.SongCreate, db: Session = Depends(get_db)):
        album = db.query(models.Album).filter(models.Album.id == album_id).first()
        artist = db.query(models.Artist).filter(models.Artist.id == song_data.artist_id).first()
        genres = db.query(models.Genre).filter(models.Genre.id.in_(song_data.genre_ids)).all()

        if not album or not artist:
            raise HTTPException(status_code=404, detail="Album or Artist not found")
        if len(genres) != len(song_data.genre_ids):
            raise HTTPException(status_code=400, detail="One or more Genre IDs are invalid")
  
        song_data_dict = song_data.model_dump(exclude={"genre_ids", "album_id"})

        new_song = models.Song(**song_data_dict, album_id=album_id)
        new_song.genres = genres
    
        db.add(new_song)
        db.commit()
        db.refresh(new_song)
    
        return new_song

    return router