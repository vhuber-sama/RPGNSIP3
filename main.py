import pygame as pg 
#import init
import sys
from random import randint as rd


pg.init()
pg.font.init()

class Jeu:

    def __init__(self):
            
        self.width = 960
        self.height = 960
        self.screen = pg.display.set_mode((self.width,self.height),vsync=1) #creates the screen object

        self.current_location = "Mr. Maurice"
        self.cl_type = "village"
        self.chara_name = "Valentin"

        self.texte_tuto = f"Bonjour {self.chara_name}, bienvenue au {self.cl_type} de {self.current_location}! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez.; Une fois accoutumé au changement de lumière et au brouhaha ambiant, vous allez au comptoir, où l'hôtesse vous salue :;'Bonsoir, {self.chara_name}. Bon retour, vous tombez à pic! Une quête vient juste d'arriver,elle sera parfaite pour vous.';'Bren, l'alchimiste qui vit à l'orée de la forêt veut aller cueillir des plantes médicinales pour ses potions, et il demande que quelqu'un l'escorte';'Il ne se passera probablement rien et au pire des cas, vous avez ce qu'il faut pour défaire les éventuelles menaces';'La récompense est de 50 pièces de bronze et une potion de soin.';change_zone;'Bonjour, vous devez être {self.chara_name}? Enchanté, je suis Bren. Merci d'avoir accepté de m'accompagner, ne perdons pas plus de temps, allons-y!';change_zone;*Alors que vous vous êtes enfoncé dans la forêt, des gobelins apparaissent*;combat;'Par Médelín, j'ai bien cru que tout cela allait mal se finir! Heureusement que vous étiez là, sinon je n'aurais pas donné cher de ma peau...';'Mais vous êtes blessé! Attendez, si je mélange ces plantes... Tenez, une potion de soin!';*Cliquez sur Inventaire, puis sur un objet utilisable pour l'utiliser*;*Une fois Bren satisfait de sa cueillette, vous le raccompagnez chez lui, puis retournez à la guilde*; Bon retour {self.chara_name}, on m a informée que vous aviez accompli votre quête avec succès!;Voici votre récompense +50 pièces de bronze, +1 potion de soin mineure"
        self.texte_tuto2 = "Bonjour Valentin, bienvenue au village de Carvinghall! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez.; Une fois accoutumé au changement de lumière et au brouhaha ambiant, vous allez au comptoir, où l'hôtesse vous salue :;'Bonsoir, Valentin. Bon retour, vous tombez à pic! Une quête vient juste d'arriver,elle sera parfaite pour vous.';'Bren, l'alchimiste qui vit à l'orée de la forêt veut aller cueillir des plantes médicinales pour ses potions, et il demande que quelqu'un l'escorte';'Il ne se passera probablement rien et au pire des cas, vous avez ce qu'il faut pour défaire les éventuelles menaces';'La récompense est de 50 pièces de bronze et une potion de soin.';change_zone;'Bonjour, vous devez être Valentin? Enchanté, je suis Bren. Merci d'avoir accepté de m'accompagner, ne perdons pas plus de temps, allons-y!';change_zone;*Alors que vous vous êtes enfoncé dans la forêt, des gobelins apparaissent*;combat;'Par Médelín, j'ai bien cru que tout cela allait mal se finir! Heureusement que vous étiez là, sinon je n'aurais pas donné cher de ma peau...';'Mais vous êtes blessé! Attendez, si je mélange ces plantes... Tenez, une potion de soin!';*Cliquez sur Inventaire, puis sur un objet utilisable pour l'utiliser*;*Une fois Bren satisfait de sa cueillette, vous le raccompagnez chez lui, puis retournez à la guilde*; Bon retour Valentin, on m a informée que vous aviez accompli votre quête avec succès!;Voici votre récompense +50 pièces de bronze, +1 potion de soin mineure"
        self.texst = "Ceci est un long bout de texte qui n'utilise pas de ponctuation et puis bla blal balballa laefoklnd fvnem ofvjhndqs!vh nosqdmlkvbnqmdss"

    def adapte_texte(self,text):
        split_tuto = text.split(';')
        i = 0
        
        while i < len(split_tuto):
            text_tuto = []
            
            if len(split_tuto[i]) > 70:
                
                first_part = split_tuto[i][:70]
                second_part = split_tuto[i][70:]    
                text_tuto.append(first_part)
                text_tuto.append(second_part)
                split_tuto.pop(i)
                split_tuto.insert(i,text_tuto)
            
            else:
                temp = split_tuto.pop(i)
                split_tuto.insert(i,[temp])
                
            i += 1

        return split_tuto

    """
    def adapte_texte_v2(self,text):
        split_text = text.split(";")
        splitted = []
        for i in range(len(split_text)):
            mot=split_text[i].split()
            for j in range(len(mot)):
                splitted.append(mot[j])
                splitted.append(" ")
        new_list = []
        print(splitted)
        e=0

        while len(splitted)-e>75:
            e+=75
            texte=""
            for i in range(e):
                texte+=splitted[i]
            new_list.append(texte)
        texte=""
        for i in range(len(splitted)-e):
            texte+=splitted[i]
        new_list.append(texte)

        print(new_list)
        
    """

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
        box = pg.draw.rect(self.screen,(255,255,255),(0,halfline,self.width,halfline),width=2)
        pg.draw.rect(self.screen,(0,0,0),(2,halfline+2,self.width-4,halfline-4))
        
        for i in range(len(text_to_show[self.current_text])):
            text_shown = self.text.render(text_to_show[self.current_text][i],True,(255,255,255))
            self.screen.blit(text_shown,(15,halfline + 25+(i*50))) 


    #============================================================================================================================================================#

    def run_game(self):

        

        self.running = True
        self.current_text = 0

        while self.running:
            for event in pg.event.get():
                    if event.type == pg.QUIT:#if we click on the cross to close the game
                        self.running = False #closes the loop that keeps the game running
                        pg.quit()
            if self.current_text >= 1:
                self.cl_type = "inside"

            self.show_ui(self.adapte_text_v3(self.texte_tuto,65),self.cl_type)
            
            self.next_btn = Button(">Next",self.width-150,self.height-70,150,70)
            self.current_text = self.next_btn.check_clicked(self.current_text,1)
            self.next_btn.show_button(self.screen)

            self.quit_btn = Button(">Quit",self.width - (self.width -50) , self.height -70, 150, 70)
            self.running = self.quit_btn.check_clicked(self.running,False)
            self.quit_btn.show_button(self.screen)
            pg.display.update()


class Button:

    def __init__(self,text : str,xpos : int,ypos : int,width : int,height: int):
        self.btn_text = text
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    def check_clicked(self,var_to_update,effect):
        for events in pg.event.get():
            if events.type == pg.MOUSEBUTTONDOWN and (pg.mouse.get_pos()[0] >= self.xpos and pg.mouse.get_pos()[0] <= self.xpos + self.width) and (pg.mouse.get_pos()[1] <= self.ypos + self.height and pg.mouse.get_pos()[1] >= self.ypos):
                if type(var_to_update) == int:
                    var_to_update += effect
                else:
                    var_to_update = effect
                print('clicked')
            
        return var_to_update
    
    def show_button(self,surface : pg.display):
        self.text = pg.font.SysFont("Times New Roman",32)
        surface.blit(self.text.render(self.btn_text,1,(255,255,255),(0,0,0)),(self.xpos,self.ypos))

    


jeu = Jeu()
jeu.run_game()
#print(type(jeu.texte_tuto))
#print(adapte_texte(texte_tuto))
#print(len("abitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez."))
