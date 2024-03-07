import sqlite3

class DBtools:
    def __init__(self):
        self.connexion = sqlite3.connect('nom.db')
        self.c = self.connexion.cursor()


    def create_player(self,id,nom,espece,classe,hp,xp,niveau,force,agilite,charisme,dexterite,intelligence,endurance,reputation,monnaie,current_zone,gway):
        #print(f"inserting {values} in {table}")
        self.c.execute(f"""INSERT INTO joueur VALUES ({id},"{nom}","{espece}","{classe}",{hp},{xp},{niveau},{force},{agilite},{charisme},{dexterite},{intelligence},{endurance},{reputation},{monnaie},{current_zone},{gway});""")
        self.connexion.commit()

    def create_zone(self,id,type,nom,nv_rcmd,type_monstre):
        self.c.execute(f"""INSERT INTO zone VALUES ({id},"{type}","{nom}",{nv_rcmd},"{type_monstre}");""")
        self.connexion.commit()
        
tools = DBtools()

tools.create_zone(1,'village','Carvinghall',0,'None')
tools.create_player(0,'Val','Elfe','archer',10,0,1,1,3,2,1,2,1,1,0,1,False)