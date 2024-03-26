import sqlite3

class DBtools:
    def __init__(self):
        self.connexion = sqlite3.connect('nom.db')
        self.c = self.connexion.cursor()


    def create_player(self,id,nom,espece,classe,hp,xp,niveau,force,agilite,charisme,dexterite,intelligence,endurance,reputation,monnaie,current_zone,gway):
        #print(f"inserting {values} in {table}")
        self.c.execute(f"""INSERT INTO joueur VALUES ({id},"{nom}","{espece}","{classe}",{hp},{xp},{niveau},{force},{agilite},{charisme},{dexterite},{intelligence},{endurance},{reputation},{monnaie},{current_zone},{gway});""")
        self.connexion.commit()

    def create_zone(self,id,type,nom,nv_rcmd,type_monstre,img_path,v1,v2,v3,v4):
        self.c.execute(f"""INSERT INTO zone VALUES ({id},"{type}","{nom}",{nv_rcmd},"{type_monstre}","{img_path}",{v1},{v2},{v3},{v4});""")
        self.connexion.commit()

    def create_monster(self,id,espece,niveau,hp,force,agilite,charisme,dexterite,intelligence,endurance,type):
        self.c.execute(f"""INSERT INTO monstre VALUES ({id},"{espece}",{niveau},{hp},{force},{agilite},{charisme},{dexterite},{intelligence},{endurance},"{type}")""")
        self.connexion.commit()

    def create_item(self,id,dura,stat,effet,spell,type,valeur_shop,val_vente,img_path):
        self.c.execute(f"""INSERT INTO items VALUES ({id},{dura},"{stat}","{effet}","{spell}","{type}",{valeur_shop},{val_vente},"{img_path}")""")
        self.connexion.commit()

    def add_inv(self,id_j,id_i,qt,eqp):
        self.c.execute(f"""INSERT INTO inventaire VALUES ({id_j},{id_i},{qt},{eqp})""")
        self.connexion.commit()
        
tools = DBtools()
"""
tools.create_zone(0,'village','Carvinghall',0,'None',"./assets/pics_towns/town1.png",1,0,0,0)
tools.create_zone(1,'inside','auberge de Carvinghall',0,'None',"./assets/pics_insides/auberge1.png",0,1,1,1)
tools.create_monster(0,'Gobelin',1,5,2,1,0,4,2,2,'foret')
tools.create_item(0,30,'STR','+1','Slash','epee',5,2,'./assets/textures/wooden_sword.png')#0,30,'STR','+ 1','Slash','épée',5,2,"./assets/textures/wooden_sword.png"
tools.create_player(0,'Val','nain','tank',10,0,1,3,1,1,1,1,3,1,0,0,False)
tools.add_inv(0,0,1,False)
#"""
#tools.create_item(1,30,'INT','+ 1','Fireball','Bâton',5,2,"./assets/textures/wooden_sword.png")
#tools.add_inv(0,1,1,True)
#tools.create_zone(2,'foret','Foret de Carvinghall',1,'foret','./assets/pics_forests/forettemp.png',0,1,2,2)
