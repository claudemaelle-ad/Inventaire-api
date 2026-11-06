-- Schéma PostgreSQL de l'inventaire informatique
-- (équivalent SQL de app/models.py ; l'API crée aussi les tables au démarrage)

DO $$ BEGIN
    CREATE TYPE type_equipement AS ENUM (
        'ordinateur_portable', 'ordinateur_fixe', 'serveur', 'ecran',
        'imprimante', 'reseau', 'telephone', 'autre'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE statut_equipement AS ENUM (
        'en_stock', 'en_service', 'en_maintenance', 'hors_service'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS equipements (
    id            SERIAL PRIMARY KEY,
    nom           VARCHAR(100)      NOT NULL,
    type          type_equipement   NOT NULL,
    marque        VARCHAR(50),
    modele        VARCHAR(100),
    numero_serie  VARCHAR(100)      NOT NULL UNIQUE,
    statut        statut_equipement NOT NULL DEFAULT 'en_stock',
    localisation  VARCHAR(100),
    utilisateur   VARCHAR(100),
    date_achat    DATE,
    prix_achat    NUMERIC(10, 2) CHECK (prix_achat >= 0),
    notes         TEXT,
    cree_le       TIMESTAMPTZ NOT NULL DEFAULT now(),
    modifie_le    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_equipements_type   ON equipements (type);
CREATE INDEX IF NOT EXISTS ix_equipements_statut ON equipements (statut);
