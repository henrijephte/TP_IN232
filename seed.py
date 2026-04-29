import sqlite3

def seed_data():
    conn = sqlite3.connect('database.db')
    donnees = [
        ('Moussa',   'Ibrahim',   '19U442', 'Afriland First Bank', 'Sciences',      'Master',  65000,  'Projet'),
        ('Tchinda',  'Pauline',   '22U331', 'Société Générale',    'Médecine',      'Licence', 15000,  'Dépôt'),
        ('Atangana', 'Luc',       '21U990', 'BICEC',               'Droit',         'Master',  80000,  'Travail'),
        ('Bella',    'Martine',   '23U400', 'Sans Banque',         'Lettres',       'Licence',  2000,  'Difficultés'),
        ('Zra',      'Dieudonné', '20U150', 'Afriland First Bank', 'Polytechnique', 'Doctorat',200000, 'Recherche'),
        ('Ondoua',   'Cyrille',   '22U770', 'UBA Cameroon',        'Sciences',      'Licence', 12000,  'Pocket money'),
        ('Mballa',   'Sonia',     '21U660', 'Société Générale',    'Médecine',      'Master',  95000,  'Économies'),
        ('Ndi',      'Joseph',    '18U120', 'BICEC',               'Droit',         'Doctorat',150000, 'Consultant'),
        ('Simo',     'Hervé',     '23U550', 'Afriland First Bank', 'Sciences',      'Licence', 35000,  'Commerce'),
        ('Biloa',    'Esther',    '22U440', 'Sans Banque',         'Lettres',       'Licence',  8000,  'Aide familiale'),
    ]

    conn.executemany('''INSERT INTO etudiants (nom, prenom, matricule, banque, faculte, niveau, montant, raison)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', donnees)
    conn.commit()
    conn.close()
    print("10 étudiants ajoutés avec succès !")

if __name__ == '__main__':
    seed_data()