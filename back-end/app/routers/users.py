import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import schemas
from ..database import models
from ..database.database import get_db

# Charge les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dépendance pour l'authentification
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

def create_router():
    router = APIRouter()

    # 6. POST /api/users/signup: Ajout d'un utilisateur
    @router.post("/users/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
    def signup_user(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
        db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password 
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return schemas.User.model_validate(new_user)

    # 7. POST /api/users/login: Connexion d'un utilisateur (JWT)
    @router.post("/users/login", response_model=schemas.Token)
    def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.email == user_data.username).first()
        
        # Vérification du mot de passe en clair
        if not user or user.password != user_data.password:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        access_token = create_access_token(data={"user_id": user.id})
        
        return schemas.Token(access_token=access_token)
        
    # 13. DELETE /api/users/:id: Suppression de utilisateur précisé par :id (Protégé par JWT)
    @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, 
                   dependencies=[Depends(get_current_user)])
    def delete_user(user_id: int, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(user)
        db.commit()
        return

    return router