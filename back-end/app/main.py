from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import albums, artists, genres, users

app = FastAPI(
    title="Spotilike API",
    description="API REST avec JWT et connexion MySQL.",
    version="1.0.0"
)

origins = ["http://localhost:4200", "*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(albums.create_router(), prefix="/api", tags=["Albums & Songs"])
app.include_router(artists.create_router(), prefix="/api", tags=["Artists"])
app.include_router(genres.create_router(), prefix="/api", tags=["Genres"])
app.include_router(users.create_router(), prefix="/api", tags=["Users & Auth"])

@app.get("/")
def read_root():
    return {"message": "Spotilike API is running. Check /docs for endpoints."}