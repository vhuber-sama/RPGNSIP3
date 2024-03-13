import sqlite3
import csv


#Connexion
connexion = sqlite3.connect('nom.db')

#Récupération d'un curseur
c = connexion.cursor()

# ------------------------------------------- début SQL ----------------------------------------#

#Création de la table

c.execute("""
    CREATE TABLE IF NOT EXISTS joueur (
    id_joueur INTEGER PRIMARY KEY,
    nom TEXT,
    espece TEXT,
    classe TEXT,
    hp FLOAT,
    xp FLOAT,
    niveau INT,
    force INT,
    agilite INT,
    charisme INT,
    dexterite INT,
    intelligence INT,
    endurance INT,
    reputation INT,
    monnaie INT,
    current_zone INT,
    gway BOOLEAN,
    FOREIGN KEY (current_zone) REFERENCES zone(id_zone)
    );
    """) #dict?

c.execute("""
    CREATE TABLE IF NOT EXISTS zone (
    id INT PRIMARY KEY,
    type TEXT,
	nom TEXT,
	niveau_recommande INT,
	type_monstre TEXT
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS monstre (
    id_monstre INTEGER PRIMARY KEY,
	niveau INT,
	hp INT,
	force INT,
    agilite INT,
    charisme INT,
    dexterite INT,
    intelligence INT,
    endurance INT,
	type TEXT,
	FOREIGN KEY (type) REFERENCES zone (type_monstre)
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS items (
    id_items INTEGER PRIMARY KEY,
    durabilite INT,
    effets TEXT,
    type TEXT,
    valeur_shop INT,
    valeur_vente INT
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS inventaire (
    id_joueur INTEGER,
    id_items INT,
    quantité INT,
    equipe BOOLEAN,
    PRIMARY KEY (id_joueur, id_items),
    FOREIGN KEY (id_joueur) REFERENCES joueur (id_joueur),
    FOREIGN KEY (id_items) REFERENCES items (id_items)
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS pnj (
	id_pnj INT PRIMARY KEY,
	nom TEXT,
	espece TEXT,
	interaction TEXT
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS quete (
    id_quete INTEGER PRIMARY KEY,
	id_pnj INT,
    type_quete TEXT,
    description_quete TEXT,
	FOREIGN KEY (id_pnj) REFERENCES pnj (id_pnj)
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS boutique (
    id_pnj INTEGER,
	id_items INTEGER,
	quantite INTEGER,
	PRIMARY KEY (id_pnj, id_items),
	FOREIGN KEY (id_pnj) REFERENCES pnj (id_pnj),
	FOREIGN KEY (id_items) REFERENCES items (id_items)
    );
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS recompense (
    id_quete INTEGER,
    id_items INT,
	PRIMARY KEY (id_quete, id_items),
	FOREIGN KEY (id_quete) REFERENCES quete (id_quete),
	FOREIGN KEY (id_items) REFERENCES items (id_items)
    );
    """)


# ---------------------------------------------- fin SQL --------------------------------------------#

