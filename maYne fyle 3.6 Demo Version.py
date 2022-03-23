import sys
sys.path.append('N:\Python36\Scripts')
import pygame

import math
from math import sin,cos
from pygame import FULLSCREEN
import sqlite3
from datetime import date
import random
pygame.init()
pygame.font.init()










#window setup
import ctypes
user32 = ctypes.windll.user32
global scr_width
global scr_height
scr_width = user32.GetSystemMetrics(0)
scr_height = user32.GetSystemMetrics(1)
window = pygame.display.set_mode((scr_width,scr_height),FULLSCREEN)
pygame.display.set_caption("sYck gaYme")


       

#=====
class Database:
    def __init__(self, tag):
        self.connection = sqlite3.connect("DatabaYse.db")
        self.cursor = self.connection.cursor()
        self.score = 0
        self.tag = tag
        self.loop = 0

    def Scoring(self):
        TitleFont = pygame.font.SysFont('', 250)
        Score = TitleFont.render(str(self.score), False, (0,0,0))
        window.blit(Score,(0,0))
        self.loop += 1
        if self.loop == 30:
            self.score += progress
            self.loop = 0
        
    def Highscore_write(self):
        today = date.today()
        #CHANGE
        ID = random.randint(0,9999999)
        #Writing to Database
        self.cursor.execute("""INSERT INTO Highscore (ID, Name, Distance, Date)
        VALUES(
        ?,
        ?,
        ?,
        ?
        )""",(ID, self.tag, self.score, today))

        self.connection.commit()
        
    def Highscore_read(self):
        TitleFont = pygame.font.SysFont('', 100)
        DataFont = pygame.font.SysFont('', 40)
        
        #Highscore Title
        HScore = TitleFont.render("Highscores", False, (0,0,0))
        window.blit(HScore,(scr_width/2-250+700,scr_height/2-252.5))

        #Reading from Database and Highscorelist
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250+700,scr_height/2-152.5,400,750))
        self.cursor.execute("SELECT * FROM Highscore ORDER BY Distance DESC")
        data = self.cursor.fetchall()
        for i in range (0, len(data)):
            for x in range (0,3):
                Score = DataFont.render(str(data[i][x+1]), False, (255,255,255))
                window.blit(Score,(scr_width/2-250+700+(130*x),scr_height/2-152.5+(50*i)))        


#=====
class Fuel:
    def __init__(self):
        self.ind = pygame.image.load("fuel wheel.png")
        self.poi = pygame.image.load("fuel pointer.png")
        self.X = scr_width/2 - 50
        self.Y = scr_height/2 - 50
        self.width = self.ind.get_width()
        self.height = self.ind.get_height()
        self.result = pygame.image.load("fuel wheel.png")
        self.fuel = 180
        self.lose = False

    def show(self):
        if self.fuel <= -175:
            self.lose = True
            
        if self.lose == False: 
            self.result = pygame.transform.rotate(self.ind,self.fuel)
            info = self.result.get_rect()
            blitX = self.X - (info.center[0]- self.X)
            blitY = self.Y - (info.center[1]- self.Y)
            window.blit(self.result, (blitX, blitY))
            window.blit(self.poi,(scr_width - 125, scr_height - 225))
            self.fuel -= .25
        else:
            Font = pygame.font.SysFont('', 90)
            Lose = Font.render('YOU LOSE', False, (255,0,0))
            window.blit(Lose,(scr_width - 350, scr_height - 50))

      

#=====
class Player:
    def __init__(self, X, Y):
        self.pl = pygame.image.load("player 5.0.png")
        self.X = X
        self.Y = Y
        self.vel = 0
        self.deg = 0
        self.width = self.pl.get_width()
        self.height = self.pl.get_height()
        self.result = pygame.image.load("player 5.0.png")
        self.rect_width = self.width
        self.rect_height = self.height   
        self.rect = pygame.Rect(self.X,self.Y,self.rect_width,self.rect_height)
        
    def displacement(self):
        self.Y += progress/2
        radians = math.radians(self.deg)
        opp = self.vel * sin(radians)
        adj = self.vel * cos(radians)

        self.result = pygame.transform.rotate(self.pl, self.deg)
        self.X += opp
        self.Y += adj

        #==
        
        
        for i in range(0,1):    
            info = self.result.get_rect()
            blitX = self.X - (info.center[0]- self.X)
            blitY = self.Y - (info.center[1]- self.Y)

            window.blit(self.result, (blitX , blitY))

            #collision==
            if i == 0:
                self.width = self.result.get_width()
                self.height = self.result.get_height()
                rectX = blitX + self.width/2 - self.rect_width/2
                rectY = blitY + self.height/2 - self.rect_height/2
                self.rect = pygame.Rect(rectX,rectY,self.rect_width,self.rect_height)
                P.collision(blitX,blitY,opp,adj)

            
    def collision(self,blitX,blitY,opp,adj):
        for i in range(0,OIP):
            if self.rect.colliderect(O[i].rect):
                if O[i].Type == "enemy":
                    F.fuel -= 75
                    self.vel = 10
                    
        for i in range(0,WIP):
            if self.rect.colliderect(W[i].rect):
                if W[i].placement == "Kill":
                    F.fuel = -175
                elif W[i].state == "Verti":
                    if (blitX + 20 > W[i].X + 3) or (blitX + self.width - 20 < W[i].X ):
                        self.X -= (opp)
                    if W[i].placement == "outer":
                        if (blitY + self.height - 20 < W[i].Y):
                                self.Y -= (adj)
                    else:
                        if (blitY + self.height - 20 < W[i].Y) or (blitY + 20 > W[i].Y + W[i].dim):
                                self.Y -= (adj)
                    
                        
                elif W[i].state == "Hori":
                    if (blitY + 20 > W[i].Y+3) or (blitY + self.height - 20 < W[i].Y):
                        self.Y -= (adj)
                    if (blitX + 20 > W[i].X + W[i].dim) or (blitX + self.width - 20 < W[i].X ):
                        self.X -= (opp)

        if self.rect.colliderect(advance_prog_rect):
            global progress
            progress = 4
        elif self.rect.colliderect(prog_rect):
            progress = 2
        else:
            progress = 1
                    
                    
 

#=====
class Bullet:
    def __init__(self, X, Y, deg):
        self.bl = pygame.image.load("bullet 4.0.png")
        self.width = self.bl.get_width()
        self.height = self.bl.get_height()
        self.X = X
        self.Y = Y
        self.deg = deg
        self.vel = 0
        self.loop = 100
        self.result = pygame.image.load("bullet 4.0.png")
        self.rect = pygame.Rect(self.X,self.Y,self.width,self.height)
        self.IP = False

    def fire(self, targetX, targetY):
        if targetX > 0:
            self.deg -= 90
        else:
            self.deg += 90
        self.result = pygame.transform.rotate(self.bl,self.deg)
        self.loop = 1
        self.IP = True
        
    def displacement(self):
        self.Y+= progress
        if self.loop < 100:
            self.loop += 1
            self.vel = 20 - (self.loop/5)
            
            radians = math.radians(self.deg)
            opp = -(self.vel * sin(radians))
            adj = -(self.vel * cos(radians))
            
            self.X += opp
            self.Y += adj
            
        else:
            self.IP = False
            self.X = -10
            self.Y = -10

        window.blit(self.result,(self.X , self.Y))
        return self.loop

    def collision(self):
        self.width = self.result.get_width()
        self.height = self.result.get_height()
        rect = pygame.Rect(self.X,self.Y,self.width,self.height)
        for i in range(OIP):
            if rect.colliderect(O[i].rect):
                self.loop = 100
                self.X = 0
                self.Y = 0
                D.score += 10
                O[i].collide = True
        for i in range(0,WIP):
            if rect.colliderect(W[i].rect):
                if W[i].state == "Verti":
                   self.deg = -self.deg
                else:
                    self.deg = 180-self.deg
                self.result = pygame.transform.rotate(self.bl,self.deg)
        if rect.colliderect(P.rect) and self.loop > 8:
            self.loop = 100
            self.X = -10
            self.Y = -10
            F.fuel -= 10

#=====
class Turret:
    def __init__ (self):
        self.tu = pygame.image.load("turret 2.0.png")
        self.deg = 0
        self.width = self.tu.get_width()
        self.height = self.tu.get_height()
        self.X = 0
        self.Y = 0
        self.result = pygame.image.load("turret 2.0.png")
        
    def update(self):
        try:
            info = self.result.get_rect()
            self.X = P.X - (info.center[0]- P.X) 
            self.Y = P.Y - (info.center[1]- P.Y)
            targetX = C.X - T.X
            targetY = C.Y - T.Y
            self.deg = math.degrees (math.atan(-targetY /targetX ))
            if targetX > 0:
                self.deg -= 90
            else:
                self.deg += 90
            self.result = pygame.transform.rotate(self.tu, self.deg)
        except:
            ZeroDivisionError

        window.blit(self.result, (self.X, self.Y))
    

#=====
class Crosshair:
    def __init__(self):
        self.cr = pygame.image.load("crosshair.png")
        self.width = self.cr.get_width()
        self.height = self.cr.get_height()
        self.X = 0
        self.Y = 0
        
    def update(self, M_x, M_y):
        self.X = M_x - self.width/2
        self.Y = M_y - self.height/2
        window.blit(self.cr, (self.X, self.Y))







#=====
class Wall:
    def __init__(self, column, row, state, placement):
        self.placement = placement
        self.dim = scr_height/6
        self.state = state
        if self.placement == "inner":
            self.Y = (row-1)*self.dim
        else:
            self.Y = (row)*self.dim 
        if self.state == "Hori":
            self.X = (scr_width/2-(5/2*self.dim))+ ((column-1)*self.dim)
            if self.placement == "inner":
                self.details = (self.X,self.Y,self.dim,3)
            else:
                self.details = (self.X,self.Y,self.dim*5,3)
        else:
            self.X = (scr_width/2-(3/2*self.dim))+ ((column-1)*self.dim)
            if self.placement == "inner":
                self.details = (self.X,self.Y,3,self.dim)
            else:
                self.details = (self.X,self.Y,3,self.dim*6)
        self.rect = pygame.Rect(self.details)

    def show(self):
        if self.placement == "inner":
            self.Y+= progress
            if self.state == "Hori":
                self.details = (self.X,self.Y,self.dim,3)
            else:
                self.details = (self.X,self.Y,3,self.dim)
            
        self.rect = pygame.draw.rect(window,(0,0,0),self.details)



#=====
class Obstacle:
    def __init__(self, column, Type):
        self.Type = Type
        if self.Type == "silo":
            self.ob = pygame.image.load("silo.png")
        else:
            self.ob = pygame.image.load("enemy.png")
        self.width = self.ob.get_width()
        self.height = self.ob.get_height()
        self.X = (scr_width/2-(5/2*W[0].dim))+ ((column-1)*W[0].dim)+ (W[0].dim - self.width)/2
        self.Y = (-1*W[0].dim) + (W[0].dim - self.height)/2
        self.rect = pygame.Rect(self.X,self.Y,self.width,self.height)
        self.collide = False

    def show(self):
        self.Y+= progress
        if self.collide:
            self.X,self.Y = scr_width,scr_height
            self.collide = False
            #silo
            if self.Type == "silo":
                if F.lose == False:
                    if F.fuel + 35 >= 175:
                        F.fuel = 180
                    else:
                        F.fuel += 35
        self.rect = pygame.Rect(self.X,self.Y,self.width,self.height)
        window.blit(self.ob, (self.X, self.Y))


       

#=====
def maze_generation(overide):
    #walls
    HoriCheck = []
    VertiCheck = []
    for i in range(0,walls):
        if random.randint(0,1) == 1:
            state = "Hori"
            col = random.randint(1,5)
            while col in HoriCheck:
                col = random.randint(1,5)
            HoriCheck.append(col)
            W.append(Wall(col,0,state,"inner"))
        else:
            state = "Verti"
            col = random.randint(1,4)
            while col in VertiCheck:
                col = random.randint(1,4)
            VertiCheck.append(col)
            W.append(Wall(col,0,state,"inner"))

        global WIP
        WIP += 1




    #silo
    global OIP
    if random.randint(1,5) == 1  or overide >= 3:
        O.append(Obstacle(random.randint(1,5),"silo"))
        OIP += 1
        overide = 0
    else:
        overide += 1

    #enemy
    if random.randint(1,4) == 1:
        O.append(Obstacle(random.randint(1,5),"enemy"))
        OIP += 1

    return overide
        

#=====
def Lose():
    TitleFont = pygame.font.SysFont('', 250)
    ButtonFont = pygame.font.SysFont('', 90)
    loop = True
    while loop:
        window.fill((255,255,255))
        #Title
        Paused = TitleFont.render('YOU LOSE', False, (0,0,0))
        window.blit(Paused,(scr_width/2-330,scr_height/2-350))
        #score
        Resume = ButtonFont.render(('Score: '+str(D.score)), False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2-152.5,500,100))
        window.blit(Resume,(scr_width/2-250,scr_height/2-152.5))
        #Retry
        Options = ButtonFont.render('RETRY', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2-27.5,500,100))
        window.blit(Options,(scr_width/2-250,scr_height/2-27.5))
        #Quit
        Quit = ButtonFont.render('QUIT', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2+97.5,500,100))
        window.blit(Quit,(scr_width/2-250,scr_height/2+97.5))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                M_x, M_y = m.get_pos()
                if M_x > scr_width/2-250 and M_x < scr_width/2-250+500 and M_y > scr_height/2-27.5 and M_y < scr_height/2-27.5+100 :
                    PLAY = True
                    loop = False
                elif M_x > scr_width/2-250 and M_x < scr_width/2-250+500 and M_y > scr_height/2+97.5 and M_y < scr_height/2+97.5+100 :
                    PLAY = False
                    loop = False

        pygame.display.update()
        
    return PLAY


#=====
def PauseMenu():
    TitleFont = pygame.font.SysFont('', 250)
    ButtonFont = pygame.font.SysFont('', 90)
    loop = True
    while loop:
        window.fill((255,255,255))
        #paused
        Paused = TitleFont.render('PAUSED', False, (0,0,0))
        window.blit(Paused,(scr_width/2-330,scr_height/2-350))
        #top-resume
        Resume = ButtonFont.render('RESUME', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2-152.5,500,100))
        window.blit(Resume,(scr_width/2-250,scr_height/2-152.5))
        #middle-help
        Options = ButtonFont.render('HELP', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2-27.5,500,100))
        window.blit(Options,(scr_width/2-250,scr_height/2-27.5))
        #bottom-quit
        Quit = ButtonFont.render('QUIT', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-250,scr_height/2+97.5,500,100))
        window.blit(Quit,(scr_width/2-250,scr_height/2+97.5))
        #Highscores
        D.Highscore_read()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                M_x, M_y = m.get_pos()
                if M_x > scr_width/2-250 and M_x < scr_width/2-250+500 and M_y > scr_height/2-152.5 and M_y < scr_height/2-152.5+100 :
                    QUIT = False
                    loop = False
                elif M_x > scr_width/2-250 and M_x < scr_width/2-250+500 and M_y > scr_height/2-27.5 and M_y < scr_height/2-27.5+100 :
                    Help_screen()
                elif M_x > scr_width/2-250 and M_x < scr_width/2-250+500 and M_y > scr_height/2+97.5 and M_y < scr_height/2+97.5+100 :
                    QUIT = True
                    loop = False

        pygame.display.update()
    return QUIT


#=====
def Login():
    TitleFont = pygame.font.SysFont('', 430)
    ButtonFont = pygame.font.SysFont('', 90)
    SubFont = pygame.font.SysFont('', 45)
    loop = True
    typing = False
    LoginText = ""
    q = 127
    p = 127
    z = 127
    while loop:
        window.fill((255,255,255))
        #sign in
        SignIn = TitleFont.render('TANK GAME', False, (q,p,z))
        window.blit(SignIn,(scr_width/2-900,scr_height/2-350))
        q += random.randint(-1,1)
        p += random.randint(-1,1)
        z += random.randint(-1,1)
        if q > 255 or q < 0:
            q = 127
        if p > 255 or p < 0:
            p = 127
        if z > 255 or z < 0:
            z = 127
        #input box
        if typing == True:
            colour = (255,0,0)
        else:
            colour = (255,255,255)
        pygame.draw.rect(window,(0,0,0),(scr_width/2-500,scr_height/2,1000,50))
        pygame.draw.rect(window,colour,(scr_width/2-487.5,scr_height/2+5,975,40))
        #- login text
        Text = SubFont.render(LoginText, False, (0,0,0))
        window.blit(Text,(scr_width/2-480,scr_height/2+5))
        #login
        Login = SubFont.render('START', False, (255,255,255))
        pygame.draw.rect(window,(0,0,0),(scr_width/2-100,scr_height/2+97.5,100,50))
        window.blit(Login,(scr_width/2-100,scr_height/2+97.5))
        #help
        Help= ButtonFont.render('HELP', False, (0,0,0))
        window.blit(Help,(scr_width/2-120,scr_height/2+300))

        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                M_x, M_y = m.get_pos()
                #click text box
                if M_x > scr_width/2-487.5 and M_x < scr_width/2-487.5+975 and M_y > scr_height/2+5 and M_y < scr_height/2+5+50:
                    typing = True
                #click Login
                elif M_x > scr_width/2-100 and M_x < scr_width/2-100+100 and M_y > scr_height/2+97.5 and M_y < scr_height/2+97.5+50:
                    loop = False
                    QUIT = False
                #help clicked
                elif M_x > scr_width/2-120 and M_x < scr_width/2-120+100 and M_y > scr_height/2+300 and M_y < scr_height/2+300+50:
                    Help_screen()
                #click elsewhere
                else:
                    typing = False
            if typing == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        LoginText = LoginText[:-1]
                    elif event.type == pygame.KEYDOWN:
                        LoginText += event.unicode
                        
        pygame.display.update()
    return QUIT, LoginText


#=====
def Help_screen():
    TitleFont = pygame.font.SysFont('', 250)
    ButtonFont = pygame.font.SysFont('', 90)
    SubFont = pygame.font.SysFont('', 40)
    loop = True
    while loop:
        window.fill((255,255,255))
        #Title
        Paused = TitleFont.render('Tutorial', False, (0,0,0))
        window.blit(Paused,(scr_width/2-330,scr_height/2-350))
        #Help text
        Help = [">A maze will descend and the goal is to survive for as long as possible.",">The longer you live and the enemies you kill will give you points.",">The further you travel upwards the faster you are and the more points you recieve.",">You will lose if your fuel gauge drops to empty.",">You can replenish fuel by shooting fuel silos.",">You also lose if you get hit by the flames chasing you.",">Bullets bounce off walls and can damage you!",">Mouse to aim and shoot, WASD to move.",">Have fun!"]
        pygame.draw.rect(window,(0,0,0),(scr_width/2-800,scr_height/2-152.5,1600,900))
        for i in range (0,len(Help)):
            Help_text = SubFont.render(Help[i], False, (255,255,255))
            window.blit(Help_text,(scr_width/2-800,scr_height/2-152.5+(35*i)))
        #Ok
        Ok= ButtonFont.render('OK', False, (0,0,0))
        pygame.draw.rect(window,(255,255,255),(scr_width/2-100,scr_height/2+300,100,50))
        window.blit(Ok,(scr_width/2-100,scr_height/2+300))

        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                M_x, M_y = m.get_pos()
                #OK clicked
                if M_x > scr_width/2-100 and M_x < scr_width/2-100+100 and M_y > scr_height/2+300 and M_y < scr_height/2+300+50:
                    loop = False
        
        pygame.display.update()

##=====
def Flame():
    fl = pygame.image.load("Flame.png")
    for i in range(0,3):
        if progress > 3:
            window.blit(fl,(random.randint(400,800),scr_height-25))
        else:
            window.blit(fl,(random.randint(400,800),scr_height-50))
    


#==========================================   
#start of proto_loop=======================


PLAY = True
while PLAY:
    #declaring
    global walls
    walls = 2
    global WIP
    WIP = 4
    global OIP
    OIP = 0
    global max_bullets
    max_bullets = 6
    global progress
    progress = 1
    m = pygame.mouse
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    M_x, M_y = m.get_pos()
    BIP = []
    W = []
    O = []

    score = 0
    time = 0
    overide = 0
    
    P = Player(scr_width/4,scr_height/4)
    C = Crosshair()
    T = Turret()
    for i in range (0,max_bullets):
        BIP.append(Bullet(0,0,0))

    F = Fuel()
    QUIT, Tag = Login()
    D = Database(Tag)

    #outer wall
    W .append(Wall(0,0,"Verti","outer"))
    W .append(Wall(5,0,"Verti","outer"))
    W .append(Wall(1,0,"Hori","outer"))
    W .append(Wall(1,6,"Hori","Kill"))


    #inner wall
    overide = maze_generation(overide)

    #progress rect
    prog_rect = pygame.Rect((scr_width/2-(5/2*W[0].dim)),0,W[0].dim*5,scr_height/2)
    advance_prog_rect = pygame.Rect((scr_width/2-(5/2*W[0].dim)),0,W[0].dim*5,scr_height/4)
        
    while not QUIT:
        pygame.time.delay(8)
        #clears the screen and updates the location of sprites
        window.fill((255,255,255))
        #movement with acceleration
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            QUIT = PauseMenu()
        if keys[pygame.K_w] and P.vel > -2.5:
            P.vel -= 0.25
        if keys[pygame.K_a]:
            P.deg += 5
        if keys[pygame.K_s] and P.vel < 1:
            P.vel += 0.25
        if keys[pygame.K_d]:
            P.deg -= 5
        if not keys[pygame.K_w] and P.vel < 0:
            P.vel += 0.05
            P.vel = round(P.vel, 2)
        if not keys[pygame.K_s] and P.vel > 0:
            P.vel -= 0.05
            P.vel = round(P.vel, 2)
        

        #trig to find x and y displacement
            #rotates and places player
        P.displacement()

        #code required for the crosshair
        for event in pygame.event.get():
            #quits properly
            if event.type == pygame.QUIT:
                QUIT = True
            #mouse code
            if event.type == pygame.MOUSEMOTION:
                M_x, M_y = m.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #bullet code
                allIP = False
                bip = 0
                while BIP[bip].IP == True and allIP == False:
                    bip += 1
                    if bip == max_bullets-1:
                        allIP = True
                        break
                if allIP == False:
                    info = BIP[bip].result.get_rect()
                    targetY = M_y - (P.Y - (info.center[1]- P.Y))
                    targetX = M_x - (P.X - (info.center[0]- P.X))
                    Bdeg = math.degrees (math.atan(-targetY / targetX ))
                    
                    BIP[bip] = Bullet(P.X - (info.center[0]- P.X), P.Y - (info.center[1]- P.Y),Bdeg)
                    BIP[bip].fire(targetX , targetY)

        #Turret
        T.update()
        
        #WALLS
        time += progress
        if time >= W[0].dim:
            overide = maze_generation(overide)
            time = 0
        for i in range(0,WIP):
            W[i].show()

        #Silo
        for i in range(0,OIP):
            O[i].show()

          
        #Fuel
        F.show()
        
        #Bullet
        for i in range(0, max_bullets):
            BIP[i].displacement()
            BIP[i].collision()

        #Crosshair
        C.update(M_x, M_y)


        #Highscore
        D.Scoring()

        if F.lose:
            QUIT = True

        Flame()

        pygame.display.update()
    D.Highscore_write()
    PLAY = Lose()
pygame.quit()

