import pygame as pg 
#import init
import os
from random import randint as rd
import Gameobjects
import pygame_widgets as pw
from pygame_widgets.button import Button

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
        self.chara_name = player.nom

        self.texte_tuto = f"Bonjour {self.chara_name}, bienvenue au {self.cl_type} de {self.current_location}! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez.; Une fois accoutumé au changement de lumière et au brouhaha ambiant, vous allez au comptoir, où l'hôtesse vous salue :;'Bonsoir, {self.chara_name}. Bon retour, vous tombez à pic! Une quête vient juste d'arriver,elle sera parfaite pour vous.';'Bren, l'alchimiste qui vit à l'orée de la forêt veut aller cueillir des plantes médicinales pour ses potions, et il demande que quelqu'un l'escorte';'Il ne se passera probablement rien et au pire des cas, vous avez ce qu'il faut pour défaire les éventuelles menaces';'La récompense est de 50 pièces de bronze et une potion de soin.';change_zone;'Bonjour, vous devez être {self.chara_name}? Enchanté, je suis Bren. Merci d'avoir accepté de m'accompagner, ne perdons pas plus de temps, allons-y!';change_zone;*Alors que vous vous êtes enfoncé dans la forêt, des gobelins apparaissent*;combat;'Par Médelín, j'ai bien cru que tout cela allait mal se finir! Heureusement que vous étiez là, sinon je n'aurais pas donné cher de ma peau...';'Mais vous êtes blessé! Attendez, si je mélange ces plantes... Tenez, une potion de soin!';*Cliquez sur Inventaire, puis sur un objet utilisable pour l'utiliser*;*Une fois Bren satisfait de sa cueillette, vous le raccompagnez chez lui, puis retournez à la guilde*; Bon retour {self.chara_name}, on m a informée que vous aviez accompli votre quête avec succès!;Voici votre récompense +50 pièces de bronze, +1 potion de soin mineure"
        self.text_to_show = self.adapte_text_v3(self.texte_tuto,65)
        #self.ui = UI(960,960)

        
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

        new_save_btn = Button(self.screen,self.w//2-125,self.halfline + 125,256,40,text="New save",textColour=(255,255,255),inactiveColour = (0,0,0))
        new_save_btn.draw()
        
        
        
        load_save_btn = Button( self.screen,self.w//2-125,self.halfline + 240, 256, 40,text="Load save",textColour=(255,255,255),inactiveColour = (0,0,0))
        load_save_btn.draw()

        


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
            self.menu_ui()
            
            quit_btn = Button(self.screen, 10, 890, 150, 70,text="Quit",textColour=(255,255,255),inactiveColour = (125,0,0),hoverColour= (255,0,0),onClick=lambda: pg.quit())
            quit_btn.draw()
            
            pw.update(events)
#            test_btn = Button("Test",450,890,70,150,self.screen)
#            compteur = test_btn.check_clicked(compteur,1)
#            test_btn.show_button()
#            print(compteur)
            
            #print(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])

            pg.display.update()

class UI:
    def __init__(self,width,height):
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

        
        
    def menu_ui(self):
        pg.font.init()

        image = pg.image.load("./assets/menu.png")

        self.screen.blit(image,(0,0))

        title = "Lizard quest"
        shown_ttl = self.ttl_font.render(title,1,(107,9,9))
        self.screen.blit(shown_ttl,(self.halfline-170,215))

        pg.draw.rect(self.screen,(0,0,0),(2,self.halfline+2,self.w-4,self.halfline-4))
        pg.draw.rect(self.screen,(255,255,255),(0,self.halfline,self.w,self.halfline),width=2)

        new_save_btn = Button(self.screen,self.w//2-125,self.halfline + 125,256,40,text="New save",textColour=(255,255,255),inactiveColour = (0,0,0))
        new_save_btn.draw()
        
        
        
        load_save_btn = Button( self.screen,self.w//2-125,self.halfline + 240, 256, 40,text="Load save",textColour=(255,255,255),inactiveColour = (0,0,0))
        load_save_btn.draw()
        
    
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
