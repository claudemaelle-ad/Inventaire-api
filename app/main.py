from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import equipements


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée les tables au démarrage si elles n'existent pas (en production : migrations Alembic).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "API REST de gestion d'un inventaire de matériel informatique.\n\n"
        "- **CRUD** complet sur les équipements\n"
        "- Filtres par type / statut, recherche plein texte et pagination\n"
        "- Statistiques de l'inventaire\n"
        "- Stockage PostgreSQL via SQLAlchemy"
    ),
    lifespan=lifespan,
)

app.include_router(equipements.router)


@app.get("/health", tags=["Supervision"], summary="État de l'API et de la base")
def health():
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
