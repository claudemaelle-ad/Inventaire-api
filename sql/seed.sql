-- Jeu de données de démonstration
INSERT INTO equipements (nom, type, marque, modele, numero_serie, statut, localisation, utilisateur, date_achat, prix_achat) VALUES
  ('PC Portable Dev 01', 'ordinateur_portable', 'Dell',    'Latitude 5440',     'SN-DL-0001', 'en_service',     'Marseille - Bureau 204', 'j.dupont',  '2025-03-15', 1249.90),
  ('PC Portable Dev 02', 'ordinateur_portable', 'Lenovo',  'ThinkPad T14',      'SN-LN-0002', 'en_stock',       'Marseille - Stock',      NULL,        '2025-06-02', 1180.00),
  ('Serveur Appli 01',   'serveur',             'HPE',     'ProLiant DL380',    'SN-HP-1001', 'en_service',     'Datacenter - Baie A3',   NULL,        '2024-11-20', 8450.00),
  ('Switch Étage 2',     'reseau',              'Cisco',   'Catalyst 9200',     'SN-CS-2001', 'en_service',     'Marseille - Local tech', NULL,        '2024-09-10', 2300.00),
  ('Écran 27"',          'ecran',               'Dell',    'P2723QE',           'SN-DL-3001', 'en_service',     'Marseille - Bureau 204', 'j.dupont',  '2025-03-15',  429.00),
  ('Imprimante RDC',     'imprimante',          'HP',      'LaserJet M480',     'SN-HP-4001', 'en_maintenance', 'Marseille - RDC',        NULL,        '2023-02-01',  690.00);
