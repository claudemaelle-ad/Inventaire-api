"""Fixtures de test : chaque test tourne sur une base PostgreSQL vierge.

La base de test est définie par TEST_DATABASE_URL (par défaut : inventaire_test en local).
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg2://inventaire:inventaire@localhost:5432/inventaire_test"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def equipement_exemple():
    return {
        "nom": "PC Portable Dev 01",
        "type": "ordinateur_portable",
        "marque": "Dell",
        "modele": "Latitude 5440",
        "numero_serie": "SN-DL-0001",
        "statut": "en_service",
        "localisation": "Marseille - Bureau 204",
        "utilisateur": "j.dupont",
        "date_achat": "2025-03-15",
        "prix_achat": "1249.90",
    }
