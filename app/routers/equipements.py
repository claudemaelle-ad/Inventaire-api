from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.models import StatutEquipement, TypeEquipement

router = APIRouter(prefix="/equipements", tags=["Équipements"])

ERREUR_404 = {404: {"description": "Équipement introuvable"}}
ERREUR_409 = {409: {"description": "Numéro de série déjà utilisé"}}


def _get_or_404(db: Session, equipement_id: int):
    equipement = crud.obtenir(db, equipement_id)
    if equipement is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Équipement {equipement_id} introuvable")
    return equipement


def _verifier_numero_serie_libre(db: Session, numero_serie: str, exclure_id: int | None = None):
    existant = crud.obtenir_par_numero_serie(db, numero_serie)
    if existant and existant.id != exclure_id:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Le numéro de série '{numero_serie}' existe déjà")


@router.get("", response_model=schemas.PageEquipements, summary="Lister les équipements")
def lister_equipements(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter (pagination)"),
    limit: int = Query(50, ge=1, le=200, description="Nombre maximum d'éléments retournés"),
    type: TypeEquipement | None = Query(None, description="Filtrer par type"),
    statut: StatutEquipement | None = Query(None, description="Filtrer par statut"),
    q: str | None = Query(None, min_length=1, description="Recherche (nom, marque, modèle, n° de série, utilisateur)"),
    db: Session = Depends(get_db),
):
    total, items = crud.lister(db, skip, limit, type, statut, q)
    return {"total": total, "skip": skip, "limit": limit, "items": items}


@router.get("/statistiques", response_model=schemas.Statistiques, summary="Statistiques de l'inventaire")
def statistiques(db: Session = Depends(get_db)):
    return crud.statistiques(db)


@router.get("/{equipement_id}", response_model=schemas.EquipementRead, responses=ERREUR_404,
            summary="Consulter un équipement")
def lire_equipement(equipement_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, equipement_id)


@router.post("", response_model=schemas.EquipementRead, status_code=status.HTTP_201_CREATED,
             responses=ERREUR_409, summary="Ajouter un équipement")
def creer_equipement(donnees: schemas.EquipementCreate, db: Session = Depends(get_db)):
    _verifier_numero_serie_libre(db, donnees.numero_serie)
    return crud.creer(db, donnees)


@router.put("/{equipement_id}", response_model=schemas.EquipementRead, responses={**ERREUR_404, **ERREUR_409},
            summary="Remplacer un équipement")
def remplacer_equipement(equipement_id: int, donnees: schemas.EquipementCreate, db: Session = Depends(get_db)):
    equipement = _get_or_404(db, equipement_id)
    _verifier_numero_serie_libre(db, donnees.numero_serie, exclure_id=equipement_id)
    return crud.modifier(db, equipement, schemas.EquipementUpdate(**donnees.model_dump()))


@router.patch("/{equipement_id}", response_model=schemas.EquipementRead, responses={**ERREUR_404, **ERREUR_409},
              summary="Modifier partiellement un équipement")
def modifier_equipement(equipement_id: int, donnees: schemas.EquipementUpdate, db: Session = Depends(get_db)):
    equipement = _get_or_404(db, equipement_id)
    if donnees.numero_serie:
        _verifier_numero_serie_libre(db, donnees.numero_serie, exclure_id=equipement_id)
    return crud.modifier(db, equipement, donnees)


@router.delete("/{equipement_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ERREUR_404,
               summary="Supprimer un équipement")
def supprimer_equipement(equipement_id: int, db: Session = Depends(get_db)):
    crud.supprimer(db, _get_or_404(db, equipement_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
