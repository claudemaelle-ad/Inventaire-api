from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import StatutEquipement, TypeEquipement


class EquipementBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100, examples=["PC Portable Dev 01"])
    type: TypeEquipement = Field(..., examples=["ordinateur_portable"])
    marque: str | None = Field(None, max_length=50, examples=["Dell"])
    modele: str | None = Field(None, max_length=100, examples=["Latitude 5440"])
    numero_serie: str = Field(..., min_length=1, max_length=100, examples=["SN-DL-0001"])
    statut: StatutEquipement = StatutEquipement.en_stock
    localisation: str | None = Field(None, max_length=100, examples=["Marseille - Bureau 204"])
    utilisateur: str | None = Field(None, max_length=100, examples=["j.dupont"])
    date_achat: date | None = None
    prix_achat: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=2, examples=[1249.90])
    notes: str | None = None


class EquipementCreate(EquipementBase):
    """Corps de requête pour créer un équipement."""


class EquipementUpdate(BaseModel):
    """Mise à jour partielle : seuls les champs envoyés sont modifiés."""

    nom: str | None = Field(None, min_length=1, max_length=100)
    type: TypeEquipement | None = None
    marque: str | None = Field(None, max_length=50)
    modele: str | None = Field(None, max_length=100)
    numero_serie: str | None = Field(None, min_length=1, max_length=100)
    statut: StatutEquipement | None = None
    localisation: str | None = Field(None, max_length=100)
    utilisateur: str | None = Field(None, max_length=100)
    date_achat: date | None = None
    prix_achat: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=2)
    notes: str | None = None


class EquipementRead(EquipementBase):
    id: int
    cree_le: datetime
    modifie_le: datetime

    model_config = ConfigDict(from_attributes=True)


class PageEquipements(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[EquipementRead]


class Statistiques(BaseModel):
    total: int
    par_statut: dict[str, int]
    par_type: dict[str, int]
    valeur_totale: Decimal
