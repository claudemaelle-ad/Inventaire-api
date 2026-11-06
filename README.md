# API Inventaire Informatique — FastAPI & PostgreSQL

![Tests](https://github.com/claudemaelle-ad/inventaire-api/actions/workflows/tests.yml/badge.svg)

API REST de gestion d'un inventaire de matériel informatique (postes, serveurs, écrans, équipements réseau…).

**Stack :** Python 3.12 · FastAPI · SQLAlchemy 2 · PostgreSQL 16 · Pydantic v2 · Pytest · Docker · GitHub Actions

## Fonctionnalités

- **CRUD complet** : ajout, consultation, modification (totale `PUT` / partielle `PATCH`) et suppression des équipements
- **Filtres, recherche et pagination** : par type, par statut, recherche texte insensible à la casse
- **Statistiques** : nombre d'équipements par statut et par type, valeur totale du parc
- **Validation** des données (Pydantic) et **codes HTTP** adaptés : `201`, `204`, `404`, `409` (n° de série en double), `422`
- **Documentation interactive** générée automatiquement (Swagger UI et ReDoc)
- **15 tests automatisés** exécutés sur une vraie base PostgreSQL, en local et en CI

## Démarrage rapide (Docker)

```bash
docker compose up --build
```

- API : http://localhost:8000
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

La base est initialisée avec `sql/schema.sql` et un jeu de démonstration (`sql/seed.sql`).

## Démarrage sans Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # adapter DATABASE_URL si besoin
psql -U inventaire -d inventaire -f sql/schema.sql -f sql/seed.sql   # optionnel
uvicorn app.main:app --reload
```

## Endpoints

| Méthode | Route | Description | Codes |
|---|---|---|---|
| `GET` | `/equipements` | Lister (filtres `type`, `statut`, `q`, pagination `skip` / `limit`) | 200 |
| `GET` | `/equipements/{id}` | Consulter un équipement | 200, 404 |
| `POST` | `/equipements` | Ajouter un équipement | 201, 409, 422 |
| `PUT` | `/equipements/{id}` | Remplacer un équipement | 200, 404, 409, 422 |
| `PATCH` | `/equipements/{id}` | Modifier certains champs | 200, 404, 409, 422 |
| `DELETE` | `/equipements/{id}` | Supprimer un équipement | 204, 404 |
| `GET` | `/equipements/statistiques` | Statistiques du parc | 200 |
| `GET` | `/health` | État de l'API et de la connexion à la base | 200 |

### Exemples

```bash
# Ajouter
curl -X POST localhost:8000/equipements -H "Content-Type: application/json" -d '{
  "nom": "PC Portable Dev 03", "type": "ordinateur_portable", "marque": "Dell",
  "numero_serie": "SN-DL-0003", "statut": "en_service", "utilisateur": "m.martin",
  "prix_achat": 1199.00
}'

# Rechercher les serveurs en service
curl "localhost:8000/equipements?type=serveur&statut=en_service"

# Passer un équipement en maintenance
curl -X PATCH localhost:8000/equipements/1 -H "Content-Type: application/json" -d '{"statut": "en_maintenance"}'

# Supprimer
curl -X DELETE localhost:8000/equipements/1
```

## Modèle de données

Table `equipements` :

| Champ | Type | Contraintes |
|---|---|---|
| `id` | SERIAL | clé primaire |
| `nom` | VARCHAR(100) | obligatoire |
| `type` | ENUM | `ordinateur_portable`, `ordinateur_fixe`, `serveur`, `ecran`, `imprimante`, `reseau`, `telephone`, `autre` |
| `marque`, `modele` | VARCHAR | |
| `numero_serie` | VARCHAR(100) | obligatoire, **unique** |
| `statut` | ENUM | `en_stock` (défaut), `en_service`, `en_maintenance`, `hors_service` |
| `localisation`, `utilisateur` | VARCHAR(100) | |
| `date_achat` | DATE | |
| `prix_achat` | NUMERIC(10,2) | ≥ 0 |
| `notes` | TEXT | |
| `cree_le`, `modifie_le` | TIMESTAMPTZ | remplis automatiquement |

Index sur `type`, `statut` et `numero_serie`.

## Tests

Les tests utilisent une base PostgreSQL dédiée (`inventaire_test`), réinitialisée avant chaque test.

```bash
createdb -U inventaire inventaire_test
pytest -v
```

Ils couvrent : création, valeurs par défaut, doublon de numéro de série (409), données invalides (422), lecture, 404, pagination, filtres, recherche, statistiques, `PUT`, `PATCH`, suppression et génération de la documentation OpenAPI.

Ils tournent aussi automatiquement sur GitHub Actions à chaque push (`.github/workflows/tests.yml`), avec un service PostgreSQL.

## Architecture

```
app/
├── main.py              # création de l'app FastAPI, /health
├── config.py            # configuration via variables d'environnement
├── database.py          # moteur SQLAlchemy, session par requête
├── models.py            # modèle ORM (table equipements)
├── schemas.py           # schémas Pydantic (validation entrée / sortie)
├── crud.py              # accès aux données (requêtes SQL)
└── routers/
    └── equipements.py   # endpoints REST
sql/                     # schéma et données de démo PostgreSQL
tests/                   # tests Pytest
```

Séparation en couches : les **routes** gèrent HTTP (codes, erreurs), le **CRUD** gère la base, les **schémas** valident les données.

## Pistes d'évolution

- Migrations de schéma avec **Alembic**
- Authentification **JWT** et gestion des rôles
- Historique des affectations (qui a eu quel matériel, quand)
- Import / export CSV de l'inventaire
- Front-end **Angular** et déploiement sur **OpenShift** via un pipeline **Jenkins**
