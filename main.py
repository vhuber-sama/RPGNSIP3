import pygame as pg 
#import init
import sys
from random import randint as rd


pg.init()
pg.font.init()


width = 960
height = 960
screen = pg.display.set_mode((width,height),vsync=1) #creates the screen object

current_location = "Mr. Maurice"
cl_type = "town"
chara_name = "Valentin"

texte_tuto = f"Bonjour {chara_name}, bienvenue au {cl_type} de {current_location}! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez.; Une fois accoutumé au changement de lumière et au brouhaha ambiant, vous allez au comptoir, où l'hôtesse vous salue :;'Bonsoir, {chara_name}. Bon retour, vous tombez à pic! Une quête vient juste d'arriver,elle sera parfaite pour vous.';'Bren, l'alcimiste qui vit à l'orée de la forêt veut aller cueillir des plantes médicinales pour ses potions, et il demande que quelqu'un l'escorte';'Il ne se passera probablement rien et au pire des cas, vous avez ce qu'il faut pour défaire les éventuelles menaces';'La récompense est de 50 pièces de bronze et une potion de soin.';change_zone;'Bonjour, vous devez être {chara_name}? Enchanté, je suis Bren. Merci d'avoir accepté de m'accompagner, ne perdons pas plus de temps, allons-y!';change_zone;*Alors que vous vous êtes enfoncé dans la forêt, des gobelins apparaissent*;combat;'Par Médelín, j'ai bien cru que tout cela allait mal se finir! Heureusement que vous étiez là, sinon je n'aurais pas donné cher de ma peau...';'Mais vous êtes blessé! Attendez, si je mélange ces plantes... Tenez, une potion de soin!';*Cliquez sur Inventaire, puis sur un objet utilisable pour l'utiliser*;*Une fois Bren satisfait de sa cueillette, vous le raccompagnez chez lui, puis retournez à la guilde*;'Bon retour {chara_name}, on m'a informée que vous aviez accompli votre quête avec succès!';'Voici votre récompense' +50 pièces de bronze, +1 potion de soin mineure"


def adapte_texte(text):
    split_tuto = texte_tuto.split(';')
    i = 0
    #print(len(split_tuto))
    #print(split_tuto)
    while i < len(split_tuto):
        #print(i,len(split_tuto))
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

def adapte_texte_v2(text):
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
    

adapte_texte_v2(texte_tuto)
rnumtown = rd(1,2)
rnumins = rd(1,3)

def show_ui(text_to_show,current_text,cl_type):
#======================================================#temp stuff for the sole purpose of showcasing idea#===========================================================#    
    if "inside" in cl_type:
        image = pg.image.load("./assets/pics_insides/inside"+str(rnumins)+".png")
    if "village" in cl_type:
        image = pg.image.load("./assets/pics_towns/town"+str(rnumtown)+".png")
    
    pg.font.init()


    text = pg.font.SysFont('Times New Roman',32)
    
    halfline = height//2 #allows to have the half of whatever the screen size is
    
    screen.blit(image,(0,0))
    box = pg.draw.rect(screen,(255,255,255),(0,halfline,width,halfline),width=2)
    pg.draw.rect(screen,(0,0,0),(2,halfline+2,width-4,halfline-4))
    
    for i in range(len(text_to_show[current_text])):
        text_shown = text.render(text_to_show[current_text][i],True,(255,255,255))
        screen.blit(text_shown,(15,halfline + 25+(i*50))) 

    text_button = text.render(">Next",True,(255,255,255))   
    screen.blit(text_button,(width - 120,height-50))

#============================================================================================================================================================#

def run_game():

    current_location = "Mr. Maurice"
    cl_type = "village"
    chara_name = "Valentin"

    running = True
    current_text = 0

    while running:
        for event in pg.event.get():
                if event.type == pg.QUIT:#if we click on the cross to close the game
                    running = False #closes the loop that keeps the game running
                    pg.quit()
                elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pos()[0] >= width-150 and pg.mouse.get_pos()[1] >= width-70:
                  current_text += 1
                  cl_type = "inside"

        show_ui(adapte_texte(texte_tuto),current_text,cl_type)
        

        pg.display.update()

#run_game()
        
#print(adapte_texte(texte_tuto))
#print(len(" Bonjour Valentin, bienvenue au town de Mr. Maurice! Comme à votre habitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez."))
