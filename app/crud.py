"""Accès aux données : toute la logique SQL est isolée ici."""

from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app import models, schemas


def lister(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    type: models.TypeEquipement | None = None,
    statut: models.StatutEquipement | None = None,
    recherche: str | None = None,
) -> tuple[int, list[models.Equipement]]:
    query = select(models.Equipement)
    if type:
        query = query.where(models.Equipement.type == type)
    if statut:
        query = query.where(models.Equipement.statut == statut)
    if recherche:
        motif = f"%{recherche}%"
        query = query.where(
            or_(
                models.Equipement.nom.ilike(motif),
                models.Equipement.marque.ilike(motif),
                models.Equipement.modele.ilike(motif),
                models.Equipement.numero_serie.ilike(motif),
                models.Equipement.utilisateur.ilike(motif),
            )
        )
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(query.order_by(models.Equipement.id).offset(skip).limit(limit)).all()
    return total, list(items)


def obtenir(db: Session, equipement_id: int) -> models.Equipement | None:
    return db.get(models.Equipement, equipement_id)


def obtenir_par_numero_serie(db: Session, numero_serie: str) -> models.Equipement | None:
    return db.scalar(select(models.Equipement).where(models.Equipement.numero_serie == numero_serie))


def creer(db: Session, donnees: schemas.EquipementCreate) -> models.Equipement:
    equipement = models.Equipement(**donnees.model_dump())
    db.add(equipement)
    db.commit()
    db.refresh(equipement)
    return equipement


def modifier(db: Session, equipement: models.Equipement, donnees: schemas.EquipementUpdate) -> models.Equipement:
    for champ, valeur in donnees.model_dump(exclude_unset=True).items():
        setattr(equipement, champ, valeur)
    db.commit()
    db.refresh(equipement)
    return equipement


def supprimer(db: Session, equipement: models.Equipement) -> None:
    db.delete(equipement)
    db.commit()


def statistiques(db: Session) -> schemas.Statistiques:
    E = models.Equipement
    par_statut = dict(db.execute(select(E.statut, func.count()).group_by(E.statut)).all())
    par_type = dict(db.execute(select(E.type, func.count()).group_by(E.type)).all())
    return schemas.Statistiques(
        total=db.scalar(select(func.count()).select_from(E)) or 0,
        par_statut={k.value: v for k, v in par_statut.items()},
        par_type={k.value: v for k, v in par_type.items()},
        valeur_totale=db.scalar(select(func.coalesce(func.sum(E.prix_achat), 0))) or Decimal(0),
    )
