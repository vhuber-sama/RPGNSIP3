import pygame as pg 
#import init
import os
from random import randint as rd
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown

import Gameobjects
import update_db

pg.init()
pg.font.init()

class Jeu:

    def __init__(self,player,width,height):
            
        self.w = width
        self.h = height
        self.halfline = height//2
        self.screen = pg.display.set_mode((self.w,self.h),vsync=1) #creates the screen object
        
        self.clock = pg.time.Clock()

        if os.name == "nt":
            self.font = pg.font.SysFont("Times New Roman",32)
            self.ttl_font = pg.font.SysFont("MV Boli", 48)
        elif os.name == "posix":
            self.font = pg.font.SysFont("Times New Roman",32)
            self.ttl_font = pg.font.SysFont("Z003",68)


        self.current_location = player.zone
        self.cl_type = 'village'
        
        self.texte_tuto = f"Bonjour {player.nom}, bienvenue au {self.cl_type} de {self.current_location}! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez.; Une fois accoutumé au changement de lumière et au brouhaha ambiant, vous allez au comptoir, où l'hôtesse vous salue :;'Bonsoir, {player.nom}. Bon retour, vous tombez à pic! Une quête vient juste d'arriver,elle sera parfaite pour vous.';'Bren, l'alchimiste qui vit à l'orée de la forêt veut aller cueillir des plantes médicinales pour ses potions, et il demande que quelqu'un l'escorte';'Il ne se passera probablement rien et au pire des cas, vous avez ce qu'il faut pour défaire les éventuelles menaces';'La récompense est de 50 pièces de bronze et une potion de soin.';change_zone;'Bonjour, vous devez être {player.nom}? Enchanté, je suis Bren. Merci d'avoir accepté de m'accompagner, ne perdons pas plus de temps, allons-y!';change_zone;*Alors que vous vous êtes enfoncé dans la forêt, des gobelins apparaissent*;combat;'Par Médelín, j'ai bien cru que tout cela allait mal se finir! Heureusement que vous étiez là, sinon je n'aurais pas donné cher de ma peau...';'Mais vous êtes blessé! Attendez, si je mélange ces plantes... Tenez, une potion de soin!';*Cliquez sur Inventaire, puis sur un objet utilisable pour l'utiliser*;*Une fois Bren satisfait de sa cueillette, vous le raccompagnez chez lui, puis retournez à la guilde*; Bon retour {player.nom}, on m a informée que vous aviez accompli votre quête avec succès!;Voici votre récompense +50 pièces de bronze, +1 potion de soin mineure"
        self.text_to_show = self.adapte_text_v3(self.texte_tuto,65)
        
        self.stats = []
        
        self.new_save_btn = Button(self.screen,self.w//2-125,self.halfline + 125,256,40,text="New save",textColour=(255,255,255),inactiveColour = (120,0,0),onClick= lambda:self.launch_n_s())
        self.load_save_btn = Button( self.screen,self.w//2-125,self.halfline + 240, 256, 40,text="Load save",textColour=(255,255,255),inactiveColour = (0,0,0))
        
        self.chara_name = TextBox(self.screen,self.w//2-125,215, 500,40,font= self.font,textColour=(0,0,0),colour = (207,160,91))
        self.espece = Dropdown(self.screen,self.w//2-125,325,500,40,name="Select species",choices=['Humain','Elfe','Nain'],colour=(207,160,91),values = ['humain','elfe','nain'])
        self.classe = Dropdown(self.screen,self.w//2-125,425,500,40,name="Select class",choices=['Warrior','Ranger','Tank','Mage'],colour=(207,160,91),values = ['warrior','ranger','tank','mage'])        
        self.spec_btn = Button(self.screen,875,325,75,40,colour = (200,20,20),text="Confirm")
        self.spec_btn.onClick= lambda: self.confirm_choice(self.espece)
        self.cla_btn = Button(self.screen,875,425,75,40,colour = (200,20,20),text="Confirm")
        self.cla_btn.onClick= lambda: self.confirm_choice(self.classe)        
        self.str_txt = TextBox(self.screen,self.w//3,525,60,40,colour=(207,160,91),font=self.font) 
        self.agi_txt = TextBox(self.screen,self.halfline+200,525,60,40,colour=(207,160,91),font=self.font)
        self.cha_txt = TextBox(self.screen,self.w//3,625,60,40,colour=(207,160,91),font=self.font)
        self.dex_txt = TextBox(self.screen,self.halfline+200,625,60,40,colour=(207,160,91),font=self.font)
        self.int_txt = TextBox(self.screen,self.w//3,725,60,40,colour=(207,160,91),font=self.font)
        self.end_txt = TextBox(self.screen,self.halfline+200,725,60,40,colour=(207,160,91),font=self.font)
        self.stat_btn = Button(self.screen,self.halfline-40,775,80,40,colour=(200,20,20),name= "Confirm stats",textColour = (255,255,255),onClick= lambda:self.choose_stats())
        self.create_btn = Button(self.screen,self.halfline-40,900,175,40,colour=(175,35,35),text="Create Character",textColour=(255,255,255),onClick= lambda: update_db.tools.create_player((Gameobjects.Toolbox.get_last_id('joueur')+1),self.args[0],self.args[1],self.args[2],10,0,1,self.stats[0],self.stats[1],self.stats[2],self.stats[3],self.stats[4],self.stats[5],0,0,0,False))



        self.new_save_btn.hide()
        self.load_save_btn.hide()

        self.chara_name.hide()
        self.espece.hide()
        self.classe.hide()
        self.spec_btn.hide()
        self.cla_btn.hide()
        self.str_txt.hide()
        self.agi_txt.hide()
        self.cha_txt.hide()
        self.dex_txt.hide()
        self.int_txt.hide()
        self.end_txt.hide()
        self.stat_btn.hide()
        self.create_btn.hide()
        
        
        self.args = []
        self.menu_widgets = [self.new_save_btn,self.load_save_btn]
        self.ns_widgets = [self.chara_name,self.espece,self.classe,self.spec_btn,self.cla_btn,self.create_btn,self.cla_btn,self.str_txt,self.agi_txt,self.cha_txt,self.dex_txt,self.int_txt,self.end_txt,self.stat_btn]

        self.ui = self.menu_ui()
        #self.quit_btn = Button(">Quit", 10, 890, 150, 70,self.screen)

 
    def adapte_text_v3(self,texte , nchar):
        texte = texte.split(';')
        liste_finale = []
        
        for t in texte:
            mots = t.split()
            ttl_len = 0
            i = 0
            liste_good = []
            len_good = 0

            while len_good < len(t):
                good = ""
                while i < len(mots) and ttl_len < nchar:
                    ttl_len += len(mots[i])+1
                    good += ' '+mots[i]
                    i += 1
                liste_good.append(good)
                len_good += len(good)
                ttl_len = 0   
            liste_finale.append(liste_good)
        print('text_ready')
        return liste_finale

    #print(adapte_text_v3(texte_tuto, 65))
    #adapte_texte_v2(texte_tuto)


    def show_ui(self,text_to_show,cl_type):
    #======================================================#temp stuff for the sole purpose of showcasing idea#===========================================================#    
        if "inside" in cl_type:
            image = pg.image.load("./assets/pics_insides/auberge1.png")
        if "village" in cl_type:
            image = pg.image.load("./assets/pics_towns/town1.png")
        
        pg.font.init()


        self.text = pg.font.SysFont('Times New Roman',32)
        
        halfline = self.height//2 #allows to have the half of whatever the screen size is
        
        self.screen.blit(image,(0,0))
        
        for i in range(len(text_to_show[self.current_text])-1):
            text_shown = self.text.render(text_to_show[self.current_text][i],True,(255,255,255))
            self.screen.blit(text_shown,(15,halfline + 25+(i*50))) 

    def menu_ui(self):
        pg.font.init()

        image = pg.image.load("./assets/menu.png")

        self.screen.blit(image,(0,0))

        title = "Lizard quest"
        shown_ttl = self.ttl_font.render(title,1,(107,9,9))
        self.screen.blit(shown_ttl,(self.halfline-170,215))

        pg.draw.rect(self.screen,(0,0,0),(2,self.halfline+2,self.w-4,self.halfline-4))
        pg.draw.rect(self.screen,(255,255,255),(0,self.halfline,self.w,self.halfline),width=2)

        for e in self.menu_widgets:
            print("drawing ",e)
            e.show()

    def txtbox_to_str(self,textbox,var):
        var = textbox.getText()
        self.args.append(var) 

    def confirm_choice(self,drop):
        print(f'added{drop.getSelected()} to {self.args}')
        self.args.append(drop.getSelected())
    
    def launch_n_s(self):
        for e in self.menu_widgets:
            e.hide()
        self.ui = self.new_save_ui()

    def choose_stats(self):
        strength = int(self.str_txt.getText())
        agi = int(self.agi_txt.getText())
        cha = int(self.cha_txt.getText())
        dex = int(self.dex_txt.getText())
        intel = int(self.int_txt.getText())
        end = int(self.end_txt.getText())
        print(f'Str:{strength} | agi:{agi} | cha:{cha} | dex: {dex} | int:{intel} | end: {end}')
        print('total :',strength+agi+cha+dex+intel+end)
        if strength+agi+cha+dex+intel+end == 10:
            self.stats = [strength,agi,cha,dex,intel,end]
        else:
            err = "Les points attribués doivent être égaux à 10 au total"
            err_msg = self.font.render(err,1,(255,0,0))
            self.screen.blit(err_msg,(50,850))

    def new_save_ui(self):
        
        pg.font.init()

        pg.draw.rect(self.screen,(0,0,0),(0,0,960,960))

        win_ttl= "Charcter Creation"
        shown_win = self.ttl_font.render(win_ttl,1,(255,255,255))
        self.screen.blit(shown_win,(self.halfline-200,30))

        chara = ""

        self.chara_name.onSubmit=lambda: self.txtbox_to_str(self.chara_name,chara)
        
        for e in self.ns_widgets:
            e.show()

        title = "Character name :"
        shown_ttl = self.font.render(title,1,(255,255,255))
        self.screen.blit(shown_ttl,(50,215))

        spec = "Character species :"
        shown_spec = self.font.render(spec,1,(255,255,255))
        self.screen.blit(shown_spec,(50,325))

        cla = "Character class :"
        shown_cla = self.font.render(cla,1,(255,255,255))
        self.screen.blit(shown_cla,(50,425))

        strtxt = "Strength :"
        shown_str = self.font.render(strtxt,1,(255,255,255))
        self.screen.blit(shown_str,(self.w//5-50,525))

        agitxt = "Agility :"
        shown_agi = self.font.render(agitxt,1,(255,255,255))
        self.screen.blit(shown_agi,(self.halfline+40,525))

        chatxt = "Charisma :"
        shown_cha = self.font.render(chatxt,1,(255,255,255))
        self.screen.blit(shown_cha,(self.w//5-50,625))

        dextxt = "Dexterity :"
        shown_dex = self.font.render(dextxt,1,(255,255,255))
        self.screen.blit(shown_dex,(self.halfline+40,625))

        inttxt = "Intelligence :"
        shown_int = self.font.render(inttxt,1,(255,255,255))
        self.screen.blit(shown_int,(self.w//5-50,725))

        endtxt = "Endurance :"
        shown_end = self.font.render(endtxt,1,(255,255,255))
        self.screen.blit(shown_end,(self.halfline+40,725))

        
#============================================================================================================================================================#

    def run_game(self):

        self.running = True
        self.current_text = 0
        
        while self.running:
            events = pg.event.get()
            for event in events:
                    if event.type == pg.QUIT :#if we click on the cross to close the game
                        self.running = False #closes the loop that keeps the game running
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        print(event)
            if self.current_text >= 1:
                self.cl_type = "inside"

        
            self.clock.tick(60)
                  
            quit_btn = Button(self.screen, 10, 890, 150, 70,text="Quit",textColour=(255,255,255),inactiveColour = (125,0,0),hoverColour= (255,0,0),onClick=lambda: pg.quit())
            #quit_btn.draw()

            #print(self.args)
            
            pw.update(events)
#            test_btn = Button("Test",450,890,70,150,self.screen)
#            compteur = test_btn.check_clicked(compteur,1)
#            test_btn.show_button()
#            print(compteur)
            
            #print(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])

            pg.display.update()

   
player = Gameobjects.Joueur(0)

jeu = Jeu(player,960,960)
jeu.run_game()
print('Game terminated')

print(player.zone , player.zone_infos)
player.change_zone(2)
print(player.zone , player.zone_infos)

#print(type(jeu.texte_tuto))
#print(adapte_texte(texte_tuto))
#print(len("abitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez."))
