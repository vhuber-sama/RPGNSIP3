import sqlite3
connexion = sqlite3.connect('nom.db')
c = connexion.cursor()

class Toolbox:

    @staticmethod
    def get(valtoget,fromwhere,id_to_check,object_id):
        c.execute(f"SELECT {valtoget} FROM {fromwhere} WHERE {id_to_check} = {object_id}")
        result = c.fetchall()
        return result[0][0]
    
    @staticmethod
    def set(valeur_to_upd, new_val, val_cle, val_id):
        c.execute(f"UPDATE joueur SET {valeur_to_upd} = {new_val} WHERE {val_cle} = {val_id}")

    @staticmethod
    def link(table,prim_key,id):
        c.execute(f"SELECT * FROM {table} WHERE {prim_key} = {id}")
        return c.fetchall()

class Joueur(Toolbox):
    def __init__(self,id_joueur):
        self.id_joueur = id_joueur
        self.nom = self.get("nom","joueur","id_joueur",self.id_joueur)
        
        self.hp = self.get("hp","joueur","id_joueur",self.id_joueur)
        self.xp = self.get("xp","joueur","id_joueur",self.id_joueur)
        self.niveau = self.get("niveau","joueur","id_joueur",self.id_joueur)
        self.stats = {'STR' : self.get("force","joueur","id_joueur",self.id_joueur),
                      'AGI' : self.get("agilite","joueur","id_joueur",self.id_joueur),
                      'CHAR' : self.get("charisme","joueur","id_joueur",self.id_joueur),
                      'DEX' : self.get("dexterite","joueur","id_joueur",self.id_joueur),
                      'INT' : self.get("intelligence","joueur","id_joueur",self.id_joueur),
                      'END' : self.get("endurance","joueur","id_joueur",self.id_joueur)}
        self.reputation = self.get("reputation","joueur","id_joueur",self.id_joueur)
        self.monnaie = self.get("monnaie","joueur","id_joueur",self.id_joueur)
        self.gway = False
        self.zone = self.get("current_zone","joueur","id_joueur",self.id_joueur)
        self.zone_infos = self.link("zone","zone.id",self.zone)

    

    def change_zone(self,new_zone):
        self.zone = new_zone
        self.zone_infos = self.link("zone","zone.id",self.zone)

    def set_action(self,action):
        self.action = action

    def combat(self,monsters : list):
        for e in monsters:
            assert type(e) == Monstre

        is_playturn = True
        while self.hp >= 0 and len(monsters)>0:
            if is_playturn and self.action == 'attack':
                monsters[0].hp -= self.stats['STR']%randint(1,20)
                if monsters[0].hp <= 0:
                    monsters.pop(0)
            elif not is_playturn:
                self.hp -= monsters[0].stats['STR']%randint(1,20)




class Monstre(Toolbox):
    def __init__(self,id_monstre):
        self.id_monstre = id_monstre
        self.niveau = self.get("niveau","monstre","id_monstre",self.id_monstre)
        self.hp = self.get("hp","monstre","id_monstre",self.id_monstre)
        self.stats = {'STR' : self.get("force","monstre","id_monstre",self.id_monstre),
                      'AGI' : self.get("agilite","monstre","id_monstre",self.id_monstre),
                      'CHAR' : self.get("charisme","monstre","id_monstre",self.id_monstre),
                      'DEX' : self.get("dexterite","monstre","id_monstre",self.id_monstre),
                      'INT' : self.get("intelligence","monstre","id_monstre",self.id_monstre),
                      'END' : self.get("endurance","monstre","id_monstre",self.id_monstre)}
        self.type = self.get("type","monstre","id_monstre",self.id_monstre)


class Zone(Toolbox):
    def __init__(self,id):
        self.id = id
        self.type = self.get("type","zone","id",self.id)
        self.nom = self.get("nom","zone","id",self.id)
        self.niveau = self.get("niveau_recommande","zone","id",self.id)
        self.type_monstre = self.get("type_monstre","zone","id",self.id)

    

class Item(Toolbox):
    def __init__(self,id_item):
        self.id_item = id_item
        self.durab = self.get("durabilite","items","id_items",self.id_item)
        self.eff = self.get("effet","items","id_items",self.id_item)
        self.type = self.get("type","items","id_items",self.id_item)
        self.val_shop = self.get("val_shop","items","id_items",self.id_item)
        self.val_vente = self.get("val_vente","items","id_items",self.id_item)

    
class Inventaire:
    def __init__(self,id_joueur):
        self.id_joueur = id_joueur
        self.id_items = []
        self.qt = {}
        self.equipe = {}


    def get_items(self):
        c.execute("SELECT id_items FROM items WHERE id_joueur ="+self.id_joueur)
        self.id_items.append(c.fetchall())

    def get_qt(self):
        for i in range(len(self.id_items)):
            c.execute("SELECT quantité FROM items WHERE id_joueur ="+self.id_joueur+" AND id_items="+self.id_items[i])
            self.qt[self.id_items[i]]=c.fetchall()


    def get_equipe(self):
        for i in range(len(self.id_items)):
            c.execute("SELECT equipe FROM items WHERE id_joueur ="+self.id_joueur+" AND id_items="+self.id_items[i])
            self.equipe[self.id_items[i]]=c.fetchall()


class PNJ(Toolbox):
    def __init__(self,id_pnj):
        self.id_pnj = id_pnj
        self.nom = self.get("nom","pnj","id_pnj",self.id_pnj)
        self.espece = self.get("espece","pnj","id_pnj",self.id_pnj)
        self.sexe = self.get("sexe","pnj","id_pnj",self.id_pnj)
        self.interaction = self.get("interaction","pnj","id_pnj",self.id_pnj)


class Quete(Toolbox):
    def __init__(self,id_quete):
        self.id_quete = id_quete
        self.type = self.get("type_quete","quete","id_quete",self.id_quete)
        self.id_pnj = self.get("pnj","quete","id_quete",self.id_quete)
        self.description = self.get("description_quete","quete","id_quete",self.id_quete)

