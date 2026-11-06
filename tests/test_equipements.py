def creer(client, data, **surcharges):
    r = client.post("/equipements", json={**data, **surcharges})
    assert r.status_code == 201, r.text
    return r.json()


# --- Création -------------------------------------------------------------

def test_creer_equipement(client, equipement_exemple):
    data = creer(client, equipement_exemple)
    assert data["id"] > 0
    assert data["nom"] == "PC Portable Dev 01"
    assert data["statut"] == "en_service"
    assert "cree_le" in data and "modifie_le" in data


def test_creer_statut_par_defaut(client):
    data = creer(client, {"nom": "Écran", "type": "ecran", "numero_serie": "SN-E-1"})
    assert data["statut"] == "en_stock"


def test_creer_numero_serie_duplique_409(client, equipement_exemple):
    creer(client, equipement_exemple)
    r = client.post("/equipements", json=equipement_exemple)
    assert r.status_code == 409


def test_creer_donnees_invalides_422(client):
    assert client.post("/equipements", json={"nom": "X"}).status_code == 422
    r = client.post("/equipements", json={"nom": "X", "type": "grille-pain", "numero_serie": "S"})
    assert r.status_code == 422
    r = client.post("/equipements", json={"nom": "X", "type": "ecran", "numero_serie": "S", "prix_achat": -5})
    assert r.status_code == 422


# --- Consultation ---------------------------------------------------------

def test_lire_equipement(client, equipement_exemple):
    cree = creer(client, equipement_exemple)
    r = client.get(f"/equipements/{cree['id']}")
    assert r.status_code == 200
    assert r.json()["numero_serie"] == "SN-DL-0001"


def test_lire_equipement_inexistant_404(client):
    assert client.get("/equipements/9999").status_code == 404


def test_lister_pagination_et_filtres(client, equipement_exemple):
    creer(client, equipement_exemple)
    creer(client, equipement_exemple, numero_serie="SN-2", nom="Serveur BDD", type="serveur", statut="en_maintenance")
    creer(client, equipement_exemple, numero_serie="SN-3", nom="Imprimante RDC", type="imprimante", marque="HP")

    r = client.get("/equipements")
    assert r.json()["total"] == 3

    r = client.get("/equipements", params={"limit": 2})
    assert r.json()["total"] == 3 and len(r.json()["items"]) == 2

    r = client.get("/equipements", params={"type": "serveur"})
    assert [e["nom"] for e in r.json()["items"]] == ["Serveur BDD"]

    r = client.get("/equipements", params={"statut": "en_maintenance"})
    assert r.json()["total"] == 1

    r = client.get("/equipements", params={"q": "hp"})
    assert [e["nom"] for e in r.json()["items"]] == ["Imprimante RDC"]


def test_statistiques(client, equipement_exemple):
    creer(client, equipement_exemple)
    creer(client, equipement_exemple, numero_serie="SN-2", type="serveur", prix_achat="5000.10")
    s = client.get("/equipements/statistiques").json()
    assert s["total"] == 2
    assert s["par_type"] == {"ordinateur_portable": 1, "serveur": 1}
    assert float(s["valeur_totale"]) == 6250.0


# --- Modification ---------------------------------------------------------

def test_patch_modifie_seulement_les_champs_envoyes(client, equipement_exemple):
    cree = creer(client, equipement_exemple)
    r = client.patch(f"/equipements/{cree['id']}", json={"statut": "en_maintenance"})
    assert r.status_code == 200
    data = r.json()
    assert data["statut"] == "en_maintenance"
    assert data["utilisateur"] == "j.dupont"  # inchangé


def test_put_remplace_l_equipement(client, equipement_exemple):
    cree = creer(client, equipement_exemple)
    nouveau = {**equipement_exemple, "nom": "PC renommé", "localisation": "Paris"}
    r = client.put(f"/equipements/{cree['id']}", json=nouveau)
    assert r.status_code == 200
    assert r.json()["nom"] == "PC renommé" and r.json()["localisation"] == "Paris"


def test_modifier_numero_serie_deja_pris_409(client, equipement_exemple):
    creer(client, equipement_exemple)
    second = creer(client, equipement_exemple, numero_serie="SN-2")
    r = client.patch(f"/equipements/{second['id']}", json={"numero_serie": "SN-DL-0001"})
    assert r.status_code == 409


def test_modifier_inexistant_404(client):
    assert client.patch("/equipements/9999", json={"nom": "X"}).status_code == 404


# --- Suppression ----------------------------------------------------------

def test_supprimer_equipement(client, equipement_exemple):
    cree = creer(client, equipement_exemple)
    assert client.delete(f"/equipements/{cree['id']}").status_code == 204
    assert client.get(f"/equipements/{cree['id']}").status_code == 404


def test_supprimer_inexistant_404(client):
    assert client.delete("/equipements/9999").status_code == 404


# --- Supervision ----------------------------------------------------------

def test_documentation_openapi(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert "/equipements/{equipement_id}" in r.json()["paths"]
