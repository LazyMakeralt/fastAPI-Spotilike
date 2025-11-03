from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..database import models
from .. import schemas

def create_router():
    router = APIRouter()
    
    # 4. GET /api/genres: Récupère la liste de tous les genres
    @router.get("/genres", response_model=List[schemas.Genre])
    def get_all_genres(db: Session = Depends(get_db)):
        genres = db.query(models.Genre).all()
        return genres

    # 12. PUT /api/genres/:id: Modification du genre précisé par :id
    @router.put("/genres/{genre_id}", response_model=schemas.Genre)
    def update_genre(genre_id: int, genre_data: schemas.GenreCreate, db: Session = Depends(get_db)):
        genre = db.query(models.Genre).filter(models.Genre.id == genre_id)
        if not genre.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
            
        genre.update(genre_data.model_dump())
        db.commit()
        
        return genre.first()
        
    return router