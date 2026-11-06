import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TypeEquipement(str, enum.Enum):
    ordinateur_portable = "ordinateur_portable"
    ordinateur_fixe = "ordinateur_fixe"
    serveur = "serveur"
    ecran = "ecran"
    imprimante = "imprimante"
    reseau = "reseau"
    telephone = "telephone"
    autre = "autre"


class StatutEquipement(str, enum.Enum):
    en_stock = "en_stock"
    en_service = "en_service"
    en_maintenance = "en_maintenance"
    hors_service = "hors_service"


class Equipement(Base):
    __tablename__ = "equipements"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    type: Mapped[TypeEquipement] = mapped_column(Enum(TypeEquipement, name="type_equipement"), index=True)
    marque: Mapped[str | None] = mapped_column(String(50))
    modele: Mapped[str | None] = mapped_column(String(100))
    numero_serie: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    statut: Mapped[StatutEquipement] = mapped_column(
        Enum(StatutEquipement, name="statut_equipement"), default=StatutEquipement.en_stock, index=True
    )
    localisation: Mapped[str | None] = mapped_column(String(100))
    utilisateur: Mapped[str | None] = mapped_column(String(100))
    date_achat: Mapped[date | None] = mapped_column(Date)
    prix_achat: Mapped[float | None] = mapped_column(Numeric(10, 2))
    notes: Mapped[str | None] = mapped_column(Text)
    cree_le: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modifie_le: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
