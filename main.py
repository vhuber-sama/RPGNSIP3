
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

    def __init__(self,width,height):
        """
        A class for the different elements that keep the game running
        """            
        #screen related stuff
        self.w = width
        self.h = height
        self.halfline = height//2
        self.screen = pg.display.set_mode((self.w,self.h),vsync=1) #creates the screen object
        
        self.clock = pg.time.Clock()

        #So that the font changes wether you are on Windows or on a Linux distro 
        if os.name == "nt":
            self.font = pg.font.SysFont("Times New Roman",32)
            self.ttl_font = pg.font.SysFont("MV Boli", 48)
        elif os.name == "posix":
            self.font = pg.font.SysFont("Times New Roman",32)
            self.ttl_font = pg.font.SysFont("Z003",68)


        self.player = None
        
        #UI related stuff
        
        #Main page UI
        self.new_save_btn = Button(self.screen,self.w//2-125,self.halfline + 125,256,40,text="New save",textColour=(255,255,255),inactiveColour = (120,0,0),onClick= lambda:self.launch_new_win(self.ns_widgets,self.new_save_ui()))
        self.load_save_btn = Button(self.screen,self.w//2-125,self.halfline + 240, 256, 40,text="Load save",textColour=(255,255,255),inactiveColour = (0,0,0),onClick= lambda: self.launch_new_win(self.ls_widgets,self.load_save_ui()))
        
        #Character creation UI
        self.stats = []
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
        self.stat_btn = Button(self.screen,self.halfline-40,775,175,40,colour=(200,20,20),name= "Confirm stats",textColour = (255,255,255),onClick= lambda:self.choose_stats())
        self.create_btn = Button(self.screen,self.halfline-40,900,175,40,colour=(175,35,35),text="Create Character",textColour=(255,255,255),onClick= lambda: self.create_char())
        #Load save UI
        
        self.save1_btn = Button(self.screen,25,100,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),borderThickness = 5,borderColour= (255,255,255),text= None ,onClick= lambda: self.start_save(0))
        self.save2_btn = Button(self.screen,25,225,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),text= None,borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.start_save(1))
        self.save3_btn = Button(self.screen,25,350,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),text= None,borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.start_save(2))
        self.save4_btn = Button(self.screen,25,475,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),text= None,borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.start_save(3))
        self.save5_btn = Button(self.screen,25,600,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),text= None,borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.start_save(4))
        self.save6_btn = Button(self.screen,25,725,920,100,inactiveColour = (20,20,20), hoverColour = (70,70,70),textColour= (255,255,255),text= None,borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.start_save(5))
        self.next_saves_btn = Button(self.screen,810,890,150,70,inactiveColour = (20,20,20), hoverColour = (70,70,70),text="Next",textColour=(255,255,255))
        self.saves_list = []
        #Text UI

        #Main UI
        self.change_zone_btn = Button(self.screen,50,550,400,100,text="Change zone",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.cz_widgets,self.change_zone_ui()))
        self.combat_btn = Button(self.screen,510,550,400,100,text="Combat",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.combat_widgets,self.combat_ui()))
        self.interact_btn = Button(self.screen,50,750,400,100,text="Interact",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.i_widgets,self.interact_ui()))
        self.inventory_btn = Button(self.screen,510,750,400,100,text="Inventory",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.in_widgets,self.inventory_ui()))
       
        #Combat UI
        self.attack_btn = Button(self.screen,50,550,400,100,text="Attack",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda: self.launch_new_win(self.atk_widgets,self.atk_ui([])))
        self.interact2_btn = Button(self.screen,510,550,400,100,text="Interact",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick=lambda:self.launch_new_win(self.text_list,self.text_ui('text')))
        self.inventory2_btn = Button(self.screen,50,750,400,100,text="Inventory",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255))
        self.flee_btn = Button(self.screen,510,750,400,100,text="Flee",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255))
        
        #Change zone UI
        self.zone1_btn = Button(self.screen,50,550,400,100,text='',textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda: print('new zone'))
        self.zone2_btn = Button(self.screen,510,550,400,100,text="Zone2",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:print('new zone'))
        self.zone3_btn = Button(self.screen,50,750,400,100,text="Zone3",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:print('new zone'))
        self.zone4_btn = Button(self.screen,510,750,400,100,text="Zone4",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:print('new zone'))
        self.confirm_btn = Button(self.screen,425,880,150,70,text="Confirm",textColour=(255,255,255),inactiveColour=(190,0,0),onClick= lambda: self.launch_new_win(self.main_widgets,self.main_ui()))

        #Attack UI
        self.attack1_btn = Button(self.screen,50,550,400,100,text="Attack1",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.a1_widgets,self.attack1_ui()))
        self.attack2_btn = Button(self.screen,510,550,400,100,text="Attack2",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.a2_widgets,self.attack2_ui()))
        self.attack3_btn = Button(self.screen,50,750,400,100,text="Attack3",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.a3_widgets,self.attack3_ui()))
        self.attack4_btn = Button(self.screen,510,750,400,100,text="Attack4",textColour=(255,255,255),inactiveColour = (0,0,0),borderThickness = 5,borderColour= (255,255,255),onClick= lambda:self.launch_new_win(self.a4_widgets,self.attack4_ui()))
        

        #Hiding the widgets so that they are only displayed if they should
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
        
        
        self.save1_btn.hide()
        self.save2_btn.hide()
        self.save3_btn.hide()
        self.save4_btn.hide()
        self.save5_btn.hide()
        self.save6_btn.hide()
        self.next_saves_btn.hide()

        self.change_zone_btn.hide()
        self.combat_btn.hide()
        self.interact_btn.hide()
        self.inventory_btn.hide()  

        self.attack_btn.hide()
        self.interact2_btn.hide()
        self.inventory2_btn.hide()
        self.flee_btn.hide()

        self.zone1_btn.hide()
        self.zone2_btn.hide()
        self.zone3_btn.hide()
        self.zone4_btn.hide()
        self.confirm_btn.hide()

        self.attack1_btn.hide()
        self.attack2_btn.hide()
        self.attack3_btn.hide()
        self.attack4_btn.hide()

        self.args = ['']
        self.menu_widgets = [self.new_save_btn,self.load_save_btn]
        self.ns_widgets = [self.chara_name,self.espece,self.classe,self.spec_btn,self.cla_btn,self.create_btn,self.cla_btn,self.str_txt,self.agi_txt,self.cha_txt,self.dex_txt,self.int_txt,self.end_txt,self.stat_btn]
        self.ls_widgets = [self.save1_btn,self.save2_btn,self.save3_btn,self.save4_btn,self.save5_btn,self.save6_btn]
        self.text_list = []
        self.main_widgets = [self.change_zone_btn,self.combat_btn,self.interact_btn,self.inventory_btn]
        self.combat_widgets = [self.attack_btn,self.interact2_btn,self.inventory2_btn,self.flee_btn]
        self.cz_widgets = [self.zone1_btn,self.zone2_btn,self.zone3_btn,self.zone4_btn,self.confirm_btn]
        self.atk_widgets = [self.attack1_btn,self.attack2_btn,self.attack3_btn,self.attack4_btn]

        self.uis_list = [self.menu_widgets,self.ls_widgets,self.ns_widgets,self.main_widgets,self.combat_widgets,self.cz_widgets,self.atk_widgets]

        self.ui = self.menu_ui()
        #self.quit_btn = Button(">Quit", 10, 890, 150, 70,self.screen)
        self.devmod_actions_list = ['K_UP','K_UP','K_DOWN','K_DOWN','K_LEFT','K_RIGHT','K_LEFT','K_RIGHT','K_b','K_a']
            

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
        self.args[0] = var 

    def confirm_choice(self,drop):
        print(f'added{drop.getSelected()} to {self.args}')
        self.args.append(drop.getSelected())
    
    def create_char(self):
        update_db.tools.create_player((Gameobjects.Toolbox.get_last_id('joueur')+1),self.args[0],self.args[1],self.args[2],10,0,1,self.stats[0],self.stats[1],self.stats[2],self.stats[3],self.stats[4],self.stats[5],0,0,0,False)
        self.player = Gameobjects.Joueur(Gameobjects.Toolbox.get_last_id('joueur'))
        self.launch_new_win(self.main_widgets,self.main_ui())

    def launch_new_win(self,launched_list,launched):
        for l in self.uis_list:
            if l == launched_list:
                pass
            else:
                for e in l:
                    e.hide()
                    #print(f"hid {e}")
        self.ui = launched

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

    def load_save_ui(self):
        """
        Une fonction qui permet de charger une partie existant déjà
        Pour l'instant crée une liste avec les noms des différents personnages.
        """
        pg.font.init()
        self.screen.fill((0,0,0))
        self.next_saves_btn.show()
        
        saves_num = Gameobjects.Toolbox.get_last_id('joueur')
        print(saves_num)
        for i in range(saves_num+1):
            print(saves_num,saves_num-i)
            e = Gameobjects.Toolbox.get('nom','joueur','id_joueur',saves_num-i)[0][0]
            print(e)
            self.saves_list.append(e)
        self.saves_list.reverse()
        for i in range(-1,len(self.ls_widgets)):
            self.ls_widgets[i].show()
            self.ls_widgets[i].setText(self.saves_list[i] if i < len(self.saves_list)else "")
            print(self.ls_widgets[i].get('text'))
        print(self.saves_list)

    def start_save(self,btn_id):
        #self.player = Gameobjects.Joueur(Gameobjects.Toolbox.get('id','joueur','joueur.nom',btn.text))
        #print(self.player)
        #self.launch_new_win(self.text_list,self.text_ui())
        self.player = Gameobjects.Joueur(btn_id)
        self.player.inventaire.get_equipe()
        print(self.player.nom)
        self.next_saves_btn.hide()
        self.launch_new_win(self.main_widgets,self.main_ui())

    def text_ui(self,text):
        #Image part:
        image = pg.image.load(f"./assets/pics_{self.player.zone_infos[1]}s/{self.player.zone_infos[2]}")

        self.screen.blit(image,(0,0))
        current_text  = 0
        for i in range(len(text[current_text])-1):
            text_shown = text.render(text[current_text][i],True,(255,255,255))
            self.screen.blit(text_shown,(15,self.halfline + 25+(i*50))) 

    def main_ui(self):
        pg.font.init()
        
        background=pg.image.load(Gameobjects.Toolbox.get('img_path','zone','id',self.player.zone.id)[0][0])
        self.screen.blit(background,(0,0))
        print(self.player.zone_infos)
        pg.draw.rect(self.screen,(0,0,0),(2,self.halfline+2,self.w-4,self.halfline-4))
        pg.draw.rect(self.screen,(255,255,255),(0,self.halfline,self.w,self.halfline),width=2)

        for e in self.main_widgets:
            e.show()

    def combat_ui(self):
        pg.draw.rect(self.screen,(0,0,0),(2,self.halfline+2,self.w-4,self.halfline-4))
        pg.draw.rect(self.screen,(255,255,255),(0,self.halfline,self.w,self.halfline),width=2)


        enemies = []
        possible_monstres = update_db.tools.c.execute(f"""SELECT id_monstre FROM monstre WHERE type = "{self.player.zone_infos[4]}" """).fetchall()
        print(possible_monstres)
        for _ in range(rd(1,5)):
            enemies.append(Gameobjects.Monstre(possible_monstres[0][rd(0,len(possible_monstres)-1)]))
        
        enemy = pg.image.load("./assets/textures/Gobelin.png")
        self.screen.blit(enemy,(0,-32))

        for e in self.combat_widgets:
            e.show()
        
        self.flee_btn.onClick = lambda: self.player.set_action('flee',enemies)
        self.attack_btn.onClick =lambda: self.launch_new_win(self.atk_widgets,self.atk_ui(enemies))
        
    def change_zone_ui(self):
        for e in self.cz_widgets:
            e.show()

        self.zone1_btn.setText(Gameobjects.Toolbox.get('nom','zone','id',self.player.zone_infos[6])[0][0] if self.player.zone_infos[6] != self.player.zone.id else "")
        self.zone2_btn.setText(Gameobjects.Toolbox.get('nom','zone','id',self.player.zone_infos[7])[0][0] if self.player.zone_infos[7] != self.player.zone.id else "")
        self.zone3_btn.setText(Gameobjects.Toolbox.get('nom','zone','id',self.player.zone_infos[8])[0][0] if self.player.zone_infos[8] != self.player.zone.id else "")
        self.zone4_btn.setText(Gameobjects.Toolbox.get('nom','zone','id',self.player.zone_infos[9])[0][0] if self.player.zone_infos[9] != self.player.zone.id else "")
        
        self.zone1_btn.onClick = lambda: self.player.zone.get_to_neighbour(self.player.zone_infos[6],self.player)
        self.zone2_btn.onClick = lambda: self.player.zone.get_to_neighbour(self.player.zone_infos[7],self.player)
        self.zone3_btn.onClick = lambda: self.player.zone.get_to_neighbour(self.player.zone_infos[8],self.player)
        self.zone4_btn.onClick = lambda: self.player.zone.get_to_neighbour(self.player.zone_infos[9],self.player)
        
    def atk_ui(self,enemies):
        for e in self.atk_widgets:
            e.show()
        self.attack1_btn.onClick = lambda: self.player.set_action('attack',enemies)
        self.attack1_btn.setText(Gameobjects.Item(self.player.inventaire.is_equiped()[0]).spell if len(self.player.inventaire.is_equiped()) >= 1 else "")
        
        self.attack2_btn.onClick = lambda: self.player.set_action('attack',enemies)
        self.attack2_btn.setText(Gameobjects.Item(self.player.inventaire.is_equiped()[1]).spell if len(self.player.inventaire.is_equiped()) >= 2 else "")

        self.attack3_btn.onClick = lambda: self.player.set_action('attack',enemies)
        self.attack3_btn.setText(Gameobjects.Item(self.player.inventaire.is_equiped()[2]).spell if len(self.player.inventaire.is_equiped()) >= 3 else "")

        self.attack4_btn.onClick = lambda: self.player.set_action('attack',enemies)
        self.attack4_btn.setText(Gameobjects.Item(self.player.inventaire.is_equiped()[3]).spell if len(self.player.inventaire.is_equiped()) >= 4 else "")

    def devmod(self):
        """
        An easter egg function
        """
        for e in pg.event.get():
            if e == pg.KEYDOWN:
                if pg.K_UP:
                    if 'K_UP' in self.devmod_actions_list and len(self.devmod_actions_list) == 10 or len(self.devmod_actions_list) == 9: 
                        self.devmod_actions_list.pop(0)
                if pg.K_DOWN:
                    if 'K_DOWN' in self.devmod_actions_list and 'K_UP' not in self.devmod_actions_list and len(self.devmod_actions_list) == 8 or len(self.devmod_actions_list) == 7:
                        self.devmod_actions_list.pop(0)
                if pg.K_LEFT and (self.devmod_actions_list == ['K_LEFT','K_RIGHT','K_LEFT','K_RIGHT','K_b','K_a'] or self.devmod_actions_list == ['K_LEFT','K_RIGHT','K_b','K_a']):
                    self.devmod_actions_list.pop(0)
                if pg.K_RIGHT and (self.devmod_actions_list == ['K_RIGHT','K_LEFT','K_RIGHT','K_b','K_a'] or self.devmod_actions_list == ['K_RIGHT','K_b','K_a']):
                    self.devmod_actions_list.pop(0)
                if pg.K_b and len(self.devmod_actions_list) == 2:
                    self.devmod_actions_list.pop(0)
                if pg.K_a and len(self.devmod_actions_list) == 1:
                    self.devmod_actions_list.pop(0)
                

        if len(self.devmod_actions_list) == 0:
            print("You signed a pact with the devil")
            self.player.hp = 666
            self.player.stats['STR'] = 666


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
                
            if self.current_text >= 1:
                self.cl_type = "inside"

        
            self.clock.tick(60)
                  
            quit_btn = Button(self.screen, 10, 890, 150, 70,text="Quit",textColour=(255,255,255),inactiveColour = (125,0,0),hoverColour= (255,0,0),onClick=lambda: pg.quit())

            pw.update(events)
            #print(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
            if self.player != None:
                self.devmod()
                if self.player.action == 'flee':
                    self.launch_new_win(self.main_widgets,self.main_ui())
                    self.player.action = None
            pg.display.update()


   
#player = Gameobjects.Joueur(0)

jeu = Jeu(960,960)
jeu.run_game()
print('Game terminated')
"""
print(player.zone , player.zone_infos)
player.change_zone(2)
print(player.zone , player.zone_infos)
"""
#print(type(jeu.texte_tuto))
#print(adapte_texte(texte_tuto))
#print(len("abitude quand vous rentrez de mission, vous vous dirigez vers l'auberge, dans laquelle vous entrez."))
