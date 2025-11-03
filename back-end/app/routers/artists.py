from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database.database import get_db
from ..database import models
from .. import schemas
from .users import get_current_user
from ..schemas import Artist

def create_router():
    router = APIRouter()
    
    # 5. GET /api/artists/:id/songs: Récupère la liste de tous les morceaux de l'artiste précisé par :id
    @router.get("/artists/{artist_id}/songs", response_model=List[schemas.Song])
    def get_songs_by_artist(artist_id: int, db: Session = Depends(get_db)):
        songs = db.query(models.Song).filter(models.Song.artist_id == artist_id).options(
            joinedload(models.Song.artist),
            joinedload(models.Song.genres)
        ).all()
        
        if not songs and not db.query(models.Artist).filter(models.Artist.id == artist_id).first():
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
             
        return songs
        
    # 10. PUT /api/artists/:id: Modification de l'artiste précisé par :id
    @router.put("/artists/{artist_id}", response_model=schemas.Artist)
    def update_artist(artist_id: int, artist_data: schemas.ArtistCreate, db: Session = Depends(get_db)):
        artist = db.query(models.Artist).filter(models.Artist.id == artist_id)
        if not artist.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
            
        artist.update(artist_data.model_dump())
        db.commit()
        
        return artist.first()
        
    # 15. DELETE /api/artists/:id: Supression de l'artiste précisé par :id (Cascade et Protégé par JWT)
    @router.delete("/artists/{artist_id}", status_code=status.HTTP_204_NO_CONTENT, 
                   dependencies=[Depends(get_current_user)])
    def delete_artist(artist_id: int, db: Session = Depends(get_db)):
        artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
        if not artist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

        db.delete(artist)
        db.commit()
        return
    
    @router.get("/artists/{artist_id}", response_model=Artist)
    def get_artist_detail(artist_id: int, db: Session = Depends(get_db)):
        artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()

        if not artist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

        return artist

    return router