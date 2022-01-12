import pygame
import pygame_menu
import pygame_gui
import math
import time

from communicate import Communicate
from authen import AuthenForm
from diaglog import MyAnnounce

pygame.init()



class Arena:
    def __init__(self, screen):
        self.background = pygame.image.load('image/bg.jpg')
        self.screen = screen
        self.manager = pygame_gui.UIManager((800, 600))
        self.communication = Communicate()
        self.announce = MyAnnounce()
        f = open('boundary/account.txt','r')
        self.account = f.readlines()
        f.close()

    def run(self ,list_user):
        running = True
        clock = pygame.time.Clock()
        background = pygame.Surface((800, 600))
        background.fill(pygame.Color('#000000'))
        list_of_buttons=[]

        def handle_button(index):
            if index >0:
                print(list_user[index-1])
                self.communication.request(f'CHAL {self.account} {list_user[index-1]}')
                #  do something

        list_of_buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (80, 25)), text='tro lai', manager=self.manager))
        for i in range(len(list_user)):
            list_of_buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100+150*(i%4), 50+(100*(int(math.floor(i/4))))), (100, 75)), text=list_user[i], manager=self.manager))

        while running:
            time_delta = clock.tick(60)/1000.0
            chall,message = self.communication.checkChallenge()
            if chall:
                k = self.announce.showInvitation(f'co loi moi thach dau tu\n{message[0]}')
                if k.status ==True:
                    self.communication.resChallenge('accept')
                    # do some thing
                else:
                    self.communication.resChallenge('reject')
        
            if False:
                pass
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element in list_of_buttons:
                                index = list_of_buttons.index(event.ui_element)
                                if index==0:
                                    running=False
                                else:
                                    handle_button(index)
                    self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.blit(background, (0, 0))
            self.screen.blit(self.background, (0, 0))

            self.manager.draw_ui(self.screen)

            pygame.display.update()


def display_blood(x,y,blood):
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(x,y,120,10))
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(x,y,blood,10))
    pygame.display.flip()



class MenuGame:
    def __init__(self, screen):
        self.screen = screen
        self.communication = Communicate()
        f = open('boundary/account.txt','r')
        self.account = f.readlines()
        f.close()

    def showListScore(self, myscore, topGamers):
        self.communication.request(f"RANK {self.account}")
        for i in range(40):
            time.sleep(0.1)
            status,values=self.communication.checkRespond()
            if(status==True):
                if(values[0]=='success'):
                    myscore = values[0]
                    topGamers = values[1:]
                break
    
        list_score = pygame_menu.Menu('Ranking', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
        list_score.add.label(f'Thành tích của bạn {myscore}')
        list_score.add.label('TOP RANKING')
        for i in range(len(topGamers)):
            list_score.add.label(f'{i+1} huy {topGamers[i]} ')
        return list_score


    def goArena(self):
        G = Arena(self.screen)
        self.communication.request("LIST")
        # for i in range(40):
        #     for i in range(40):
        #         time.sleep(0.1)
        #         status,values=self.communication.checkRespond()
        #         if(status==True):
        #             G.run(values)
        #             break        

        G.run(['huy','nam','dat','huy1','nam1','dat1','huy2','nam2','dat2'])

    def gameExit(self):
        exit()

    def run(self):
        menu = pygame_menu.Menu('Welcome', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Đến đấu trường', self.goArena)
        menu.add.button('Điểm số',self.showListScore(100,[10,20,30,40,50,60,70,80,90,100]))
        menu.add.button('Thoát Game', self.gameExit)
        menu.mainloop(screen)




authen = AuthenForm()
result = authen.authenticate()
if result:
    screen = pygame.display.set_mode((800,600))
    running = True
    menu = MenuGame(screen)
    menu.run()