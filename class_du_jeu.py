import sqlite3
connexion = sqlite3.connect('nom.db')
c = connexion.cursor()

class Joueur:
    def __init__(self,id_joueur):
        self.nom = nom
        self.id_joueur = id_joueur
        self.hp = self.get_hp()
        self.xp = self.get_xp()
        self.niveau = self.get_niveau()
        self.stats = self.get_stats()
        self.reputation = self.get_reputation()
        self.monnaie = self.get_monnaie()
        self.gway = False

    def get_nom(self):
        return self.nom

    def get_id_joueur(self):
        return self.id_joueur

    def get_hp(self):
        c.execute("SELECT hp FROM joueur WHERE id_joueur ="+self.id_joueur)
        hp = c.fetchall()
        return hp

    def get_xp(self):
        c.execute("SELECT xp FROM joueur WHERE id_joueur ="+self.id_joueur)
        xp = c.fetchall()
        return xp

    def get_niveau(self):
        c.execute("SELECT niveau FROM joueur WHERE id_joueur ="+self.id_joueur)
        nv = c.fetchall()
        return nv

    def get_reputation(self):
        c.execute("SELECT reputation FROM joueur WHERE id_joueur ="+self.id_joueur)
        rep = c.fetchall()
        return rep

    def get_monnaie(self):
        c.execute("SELECT monnaie FROM joueur WHERE id_joueur ="+self.id_joueur)
        mon = c.fetchall()
        return mon

    def get_gway(self):
        c.execute("SELECT gway FROM joueur WHERE id_joueur ="+self.id_joueur)
        gway = c.fetchall()
        return gway

    def set_hp(self,valeur):
        c.execute("UPDATE joueur SET hp ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_xp(self,valeur):
        c.execute("UPDATE joueur SET xp ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_niveau(self,valeur):
        c.execute("UPDATE joueur SET niveau ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_stats(self,valeur):
        c.execute("UPDATE joueur SET stats ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_rep(self,valeur):
        c.execute("UPDATE joueur SET reputation ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_mon(self,valeur):
        c.execute("UPDATE joueur SET monnaie ="+ valeur +"WHERE id_joueur ="+self.id_joueur)

    def set_gway(self,valeur):
        c.execute("UPDATE joueur SET gway ="+ valeur +"WHERE id_joueur ="+self.id_joueur)


class Monstre:
    def __init__(self,id_monstre):
        self.id_monstre = id_monstre
        self.niveau = self.get_niv()
        self.hp = self.get_hp()
        self.stats = self.get_stats()
        self.type = self.get()

    def get_monstre(self):
        return self.id_monstre

    def get_niv(self):
        c.execute("SELECT niveau FROM monstre WHERE id_monstre ="+self.id_monstre)
        niv = c.fetchall()
        return niv

    def get_hp(self):
        c.execute("SELECT hp FROM monstre WHERE id_monstre ="+self.id_monstre)
        hp = c.fetchall()
        return hp

    def get_type(self):
        c.execute("SELECT type FROM monstre WHERE id_monstre ="+self.id_monstre)
        type = c.fetchall()
        return type

    def set_niveau(self,valeur):
        c.execute("UPDATE monstre SET niveau ="+ valeur +"WHERE id_monstre ="+self.id_monstre)

    def set_hp(self,valeur):
        c.execute("UPDATE monstre SET hp ="+ valeur +"WHERE id_monstre ="+self.id_monstre)

    def set_stats(self,valeur):
        c.execute("UPDATE monstre SET stats ="+ valeur +"WHERE id_monstre ="+self.id_monstre)


class Zone:
    def __init__(self,id):
        self.id = id
        self.type = self.get_type()
        self.nom = self.get_nom()
        self.niveau = self.get_niv()
        self.type_monstre = self.get_type_monstre()

    def get_id(self):
        return self.id

    def get_type(self):
        c.execute("SELECT type FROM zone WHERE id_zone ="+self.id)
        type = c.fetchall()
        return type

    def get_nom(self):
        c.execute("SELECT nom FROM zone WHERE id_zone ="+self.id)
        nom = c.fetchall()
        return nom

    def get_niv(self):
        c.execute("SELECT niveau FROM zone WHERE id_zone ="+self.id)
        niv = c.fetchall()
        return niv

    def get_type_monstre(self):
        c.execute("SELECT type_monstre FROM zone WHERE id_zone ="+self.id)
        type_monstre = c.fetchall()
        return type_monstre


class Items:
    def __init__(self,id_items):
        self.id_items = id_items
        self.durab = self.get_durab()
        self.eff = self.get_eff()
        self.type = self.get_type()
        self.val_shop = self.get_val_shop()
        self.val_vente = self.get_val_vente()

    def get_id_items(self):
        return self.id_items

    def get_durab(self):
        c.execute("SELECT durabilite FROM items WHERE id_items ="+self.id_items)
        durab = c.fetchall()
        return durab

    def get_eff(self):
        c.execute("SELECT effets FROM items WHERE id_items ="+self.id_items)
        eff = c.fetchall()
        return eff

    def get_type(self):
        c.execute("SELECT type FROM items WHERE id_items ="+self.id_items)
        type = c.fetchall()
        return type

    def get_val_shop(self):
        c.execute("SELECT valeur_shop FROM items WHERE id_items ="+self.id_items)
        val_shop = c.fetchall()
        return valshop

    def get_val_vente(self):
        c.execute("SELECT valeur_vente FROM items WHERE id_items ="+self.id_items)
        val_vente = c.fetchall()
        return val_vente


class Inventaire:
    def __init__(self,id_joueur):
        self.id_joueur = id_joueur
        self.id_items = []
        self.qt = {}
        self.equipe = {}

    def get_id_joueur(self):
        return self.id_joueur

    def get_items(self):
        c.execute("SELECT id_items FROM items WHERE id_joueur ="+self.id_joueur)
        self.id_items = c.fetchall()

    def get_qt(self):
        for i in range(len(self.id_items)):
            c.execute("SELECT quantité FROM items WHERE id_joueur ="+self.id_joueur+" AND id_items="+self.id_items[i])
            self.qt[self.id_items[i]]=c.fetchall()


    def get_equipe(self):
        for i in range(len(self.id_items)):
            c.execute("SELECT equipe FROM items WHERE id_joueur ="+self.id_joueur+" AND id_items="+self.id_items[i])
            self.equipe[self.id_items[i]]=c.fetchall()


class PNJ:
    def __init__(self,id_pnj):
        self.id_pnj = id_pnj
        self.nom = self.get_nom()
        self.espece = self.get_espece()
        self.sexe = self.get_sx()
        self.interaction = self.get_inter()

    def get_id_pnj(self):
        return self.id_pnj

    def get_nom(self):
        c.execute("SELECT nom FROM pnj WHERE id_pnj ="+self.id_pnj)
        pnj = c.fetchall()
        return pnj

    def get_espece(self):
        c.execute("SELECT espece FROM pnj WHERE id_pnj ="+self.id_pnj)
        esp = c.fetchall()
        return esp

    def get_sx(self):
        c.execute("SELECT sexe FROM pnj WHERE id_pnj ="+self.id_pnj)
        sx = c.fetchall()
        return sx

    def get_inter(self):
        c.execute("SELECT interaction FROM pnj WHERE id_pnj ="+self.id_pnj)
        inter = c.fetchall()
        return inter

class Quete:
    def __init__(self,id_quete):
        self.id_quete = id_quete
        self.id_pnj = self.get_pnj()
        self.description = self.get_descr()

    def get_id_quete(self):
        return self.id_quete

    def get_pnj(self):
        c.execute("SELECT id_pnj FROM quete WHERE id_quete ="+self.id_quete)
        pnj = c.fetchall()
        return pnj

    def get_descr(self):
        c.execute("SELECT description FROM quete WHERE id_quete ="+self.id_quete)
        descr = c.fetchall()
        return descr

def create_joueur(id, hp, xp, nv, stats, reput, monnaie, gway):
    p = "INSERT INTO joueur VALUES ('" + id + "','" + hp + "','" + xp + "','" + nv + "','" + stats + "','" + reput + "','" + monnaie + "','" + gway + "')"
    c.executescript(p)
















