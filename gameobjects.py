
import sqlite3
from random import randint
connexion = sqlite3.connect('nom.db')
c = connexion.cursor()

class Toolbox:

    @staticmethod
    def get(valtoget,fromwhere,id_to_check,object_id):
        #print(f"SELECT {valtoget} FROM {fromwhere} WHERE {id_to_check} = {object_id}")
        c.execute(f"SELECT {valtoget} FROM {fromwhere} WHERE {id_to_check} = {object_id}")
        result = c.fetchall()
        return result
    
    @staticmethod
    def set(table,valeur_to_upd, new_val, val_cle, val_id):
        print(f"UPDATE {table} SET {valeur_to_upd} = {new_val} WHERE {val_cle} = {val_id}")
        c.execute(f"UPDATE {table} SET {valeur_to_upd} = {new_val} WHERE {val_cle} = {val_id}")
        connexion.commit()
    @staticmethod
    def get_all(table,prim_key,id):
        c.execute(f"SELECT * FROM {table} WHERE {prim_key} = {id}")
        return c.fetchall()
    
    @staticmethod
    def get_last_id(table):
        if table != 'zone':
            c.execute(f"SELECT MAX(id_{table}) FROM {table}")
        else:
            c.execute(f"SELECT MAX(id) FROM {table}")

        ans = c.fetchall()[0]
        if len(ans) == 0:
            return 0
        else:
            return ans[0]

class Joueur(Toolbox):
    def __init__(self,id_joueur):
        self.id_joueur = id_joueur
        self.nom = self.get("nom","joueur","id_joueur",self.id_joueur)[0][0]
        self.classe = self.get('classe','joueur','id_joueur',self.id_joueur)[0][0]
        self.hp = self.get("hp","joueur","id_joueur",self.id_joueur)[0][0]
        self.xp = self.get("xp","joueur","id_joueur",self.id_joueur)[0][0]
        self.niveau = self.get("niveau","joueur","id_joueur",self.id_joueur)[0][0]
        self.stats = {'STR' : self.get("force","joueur","id_joueur",self.id_joueur)[0][0],
                      'AGI' : self.get("agilite","joueur","id_joueur",self.id_joueur)[0][0],
                      'CHAR' : self.get("charisme","joueur","id_joueur",self.id_joueur)[0][0],
                      'DEX' : self.get("dexterite","joueur","id_joueur",self.id_joueur)[0][0],
                      'INT' : self.get("intelligence","joueur","id_joueur",self.id_joueur)[0][0],
                      'END' : self.get("endurance","joueur","id_joueur",self.id_joueur)[0][0]}
        self.reputation = self.get("reputation","joueur","id_joueur",self.id_joueur)[0][0]
        self.monnaie = self.get("monnaie","joueur","id_joueur",self.id_joueur)[0][0]
        self.gway = False
        self.zone = Zone(self.get("current_zone","joueur","id_joueur",self.id_joueur)[0][0])
        self.zone_infos = self.get_all("zone","zone.id",self.zone.id)[0]
        self.inventaire = Inventaire(self.id_joueur)
        self.action = None
        self.is_fighting = True

    def change_zone(self,new_zone):
        self.zone = Zone(new_zone)
        self.zone_infos = self.get_all("zone","zone.id",self.zone.id)[0]
        print(self.zone_infos)

    def set_action(self,action,monsters):
        self.is_fighting = True
        self.action = action
        self.combat_turn(monsters)

    def combat_turn(self,monsters):

        is_playturn = True
        for e in monsters:
            print(e.espece)
        if len(monsters) >0:
            if is_playturn :
                if self.action == 'attack':
                    diceroll = randint(1,20)
                    #Must combine : the appropriate stat + the spell buff. case match ? 
                    monsters[0].hp -= int(self.stats[Item(self.inventaire.is_equiped()[0]).stat]+(eval(Item(self.inventaire.is_equiped()[0]).eff))*(0.1*diceroll))
                    print(f"You rolled a {diceroll}, dealing {int(self.stats[Item(self.inventaire.is_equiped()[0]).stat]+(eval(Item(self.inventaire.is_equiped()[0]).eff))*(0.1*diceroll))} damage to the {monsters[0].espece}, lowering its hp to: {monsters[0].hp}")
                    if monsters[0].hp <= 0:
                        print(f"you killed a {monsters[0].espece}, + {3 * (monsters[0].niveau%5)}xp")
                        self.xp += 3 * (monsters[0].niveau%5)
                        monsters.pop(0)

                    if len(monsters)>0:
                        diceroll = randint(1,20)
                        self.hp -= int(monsters[0].stats['STR']*(0.1*diceroll))
                        print(f"{monsters[0].espece} rolled a {diceroll}, dealing {int(monsters[0].stats['STR']*(0.1*diceroll))} damage to you, lowering your hp to: {self.hp}")
                        if self.hp <= 0:
                            print("You died")
                            exit(0)
                        is_playturn = True
                    else:
                        self.is_fighting = False
                elif self.action == 'interact':
                    diceroll = randint(1,20)
                    self.hp -= int(monsters[0].stats['STR']*(0.1*diceroll))
                    print(f"{monsters[0].espece} rolled a {diceroll}, dealing {int(monsters[0].stats['STR']*(0.1*diceroll))} damage to you, lowering your hp to: {self.hp}")
                    if self.hp <= 0:
                        print("You died")
                    is_playturn = True
                    pass #will come back at that later. CF inventory

                elif self.action == 'inventory':
                ###Must make it access the ui funcs in class Jeu (but can't import it cause of circular import)
                #Make a graphical representation for marko
                    diceroll = randint(1,20)
                    self.hp -= int(monsters[0].stats['STR']*(0.1*diceroll))
                    print(f"{monsters[0].espece} rolled a {diceroll}, dealing {int(monsters[0].stats['STR']*(0.1*diceroll))} damage to you, lowering your hp to: {self.hp}")
                    if self.hp <= 0:
                        print("You died")
                    is_playturn = True

                elif self.action == 'flee':
                    #if you flee, you will loose hp and not get rewards
                    self.hp // 2
                    while len(monsters)>0:
                        monsters.pop()
                    print(f'you fled and lost hp on the way, reducing your health to {self.hp}')
        else:
            self.is_fighting = False
                                



            

class Monstre(Toolbox):
    def __init__(self,id_monstre):
        self.id_monstre = id_monstre
        self.niveau = self.get("niveau","monstre","id_monstre",self.id_monstre)[0][0]
        self.espece = self.get("espece","monstre","id_monstre",self.id_monstre)[0][0]
        self.hp = self.get("hp","monstre","id_monstre",self.id_monstre)[0][0]
        self.stats = {'STR' : self.get("force","monstre","id_monstre",self.id_monstre)[0][0],
                      'AGI' : self.get("agilite","monstre","id_monstre",self.id_monstre)[0][0],
                      'CHAR' : self.get("charisme","monstre","id_monstre",self.id_monstre)[0][0],
                      'DEX' : self.get("dexterite","monstre","id_monstre",self.id_monstre)[0][0],
                      'INT' : self.get("intelligence","monstre","id_monstre",self.id_monstre)[0][0],
                      'END' : self.get("endurance","monstre","id_monstre",self.id_monstre)[0][0]}
        self.type = self.get("type","monstre","id_monstre",self.id_monstre)[0][0]


class Zone(Toolbox):
    def __init__(self,id):
        self.id = id
        self.type = self.get("type","zone","id",self.id)[0][0]
        self.nom = self.get("nom","zone","id",self.id)[0][0]
        self.niveau = self.get("niveau_recommande","zone","id",self.id)[0][0]
        self.type_monstre = self.get("type_monstre","zone","id",self.id)[0][0]
        self.voisins = [self.get('voisin1',"zone","id",self.id)[0][0],self.get('voisin2',"zone","id",self.id)[0][0],self.get('voisin3',"zone","id",self.id)[0][0],self.get('voisin4',"zone","id",self.id)[0][0]]
        
    def get_to_neighbour(self,v,p: Joueur):
        self.id = v
        self.type = self.get("type","zone","id",self.id)[0][0]
        self.nom = self.get("nom","zone","id",self.id)[0][0]
        self.niveau = self.get("niveau_recommande","zone","id",self.id)[0][0]
        self.type_monstre = self.get("type_monstre","zone","id",self.id)[0][0]
        self.voisins = [self.get('voisin1',"zone","id",self.id)[0][0],self.get('voisin2',"zone","id",self.id)[0][0],self.get('voisin3',"zone","id",self.id)[0][0],self.get('voisin4',"zone","id",self.id)[0][0]]
        p.change_zone(v)
    
class Item(Toolbox):
    def __init__(self,id_item):
        self.id_item = id_item
        self.durab = self.get("durabilite","items","id_items",self.id_item)[0][0]
        self.stat = self.get("stat",'items','id_items',self.id_item)[0][0]
        self.eff = self.get("effets","items","id_items",self.id_item)[0][0]
        self.spell = self.get("spell",'items','id_items',self.id_item)[0][0]
        self.type = self.get("type","items","id_items",self.id_item)[0][0]
        self.val_shop = self.get("valeur_shop","items","id_items",self.id_item)[0][0]
        self.val_vente = self.get("valeur_vente","items","id_items",self.id_item)[0][0]

    
class Inventaire(Toolbox):
    def __init__(self,id_joueur):
        self.id_joueur = id_joueur
        self.id_items = self.get('id_items','inventaire','id_joueur',self.id_joueur)
        self.qt = {}
        self.equipe = {}

    def get_qt(self):
        for i in range(len(self.id_items)):
            c.execute(f"SELECT quantité FROM inventaire WHERE id_joueur ={self.id_joueur} AND id_items={self.id_items[i][0]}")
            self.qt[self.id_items[i][0]]=c.fetchall()[0][i-1]


    def get_equipe(self):
        for i in range(len(self.id_items)):
            c.execute(f"SELECT equipe FROM inventaire WHERE id_joueur = {self.id_joueur} AND id_items= {self.id_items[i][0]}")
            #print(c.fetchall())
            self.equipe[self.id_items[i][0]]= True if c.fetchall() == [(1,)] else False
    def is_equiped(self):
        ans = []
        for e in self.equipe.keys():
            if self.equipe[e] == True:
                ans.append(e)
        return ans
    
class PNJ(Toolbox):
    def __init__(self,id_pnj):
        self.id_pnj = id_pnj
        self.nom = self.get("nom","pnj","id_pnj",self.id_pnj)[0][0]
        self.espece = self.get("espece","pnj","id_pnj",self.id_pnj)[0][0]
        self.sexe = self.get("sexe","pnj","id_pnj",self.id_pnj)[0][0]
        self.interaction = self.get("interaction","pnj","id_pnj",self.id_pnj)[0][0]


class Quete(Toolbox):
    def __init__(self,id_quete):
        self.id_quete = id_quete
        self.type = self.get("type_quete","quete","id_quete",self.id_quete)[0][0]
        self.id_pnj = self.get("pnj","quete","id_quete",self.id_quete)[0][0]
        self.description = self.get("description_quete","quete","id_quete",self.id_quete)[0][0]

tool = Toolbox()

#"""

#print(tool.get_last_id("joueur"))
#tool.set('joueur','current_zone',0,'id_joueur',0)

player = Joueur(0)
#player.set_action("attack")
#player.combat([Monstre(0)])
player.inventaire.get_qt()
player.inventaire.get_equipe()
print(player.inventaire.id_items ,' | ', player.inventaire.qt,' | ',player.inventaire.equipe)
print(player.inventaire.is_equiped())


#tool.set('inventaire','equipe',False,'id_items',1)
#tool.set('inventaire','equipe',True,'id_items',0)
#"""
