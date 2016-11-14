import pygame,sys,os,random,time
from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((1280,720),FULLSCREEN,32)

#Setting Up the Images.
screen1=['n.jpg','nr.jpg','nrstudios.jpg','harbinger.jpg']
screen2=['Presents.jpg','Black.jpg']
screen3=['NebulaCorps.jpg','Black.jpg'] 
screen4=['vs.jpg','Black.jpg']
screen5=['DarkstarFaction.jpg','Black.jpg']
screen6=['in.jpg','Black.jpg']
screen7=['Project Darkstar Main Menu.jpg','Project Darkstar.jpg']

Icon=pygame.image.load("Mouse_Icon.png").convert_alpha()

#Menu Images
Normal=pygame.image.load('Project Darkstar Main Menu.jpg').convert()
InstructionsGlowing=pygame.image.load('Instructions Button Glowing.jpg').convert()
StoryGlowing=pygame.image.load('Story Button Glowing.jpg').convert()
CreditsGlowing=pygame.image.load('Credits Button Glowing.jpg').convert()
ExitGlowing=pygame.image.load('Exit Button Glowing.jpg').convert()
PlayGlowing=pygame.image.load('Play Button Glowing.jpg').convert()

#Game Images And Sprites
background=pygame.image.load('DarkStar1.jpg').convert()
ship=pygame.image.load('ship.png').convert_alpha()
missilefinal=pygame.image.load('missile.png').convert_alpha()
villain=pygame.image.load('villain.png').convert_alpha()
villain2=pygame.image.load('Enceladus.png').convert_alpha()
villain3=pygame.image.load('Piranha.png').convert_alpha()
EnemyMissile=pygame.image.load('EnemyMissile.png').convert_alpha()

FireBall=pygame.image.load('FireBall1.png').convert_alpha()
HealthImages=['0.png','1.png','2.png','3.png','4.png']
SmallFries=['smallfry1.png','smallfry2.png','smallfry3.png','smallfry4.png']
GameOver='Game Over 3.jpg'
WinScreen='You Win Screen.jpg'
HealthPack=pygame.image.load('healthpack.png').convert_alpha()
AmmoPack=pygame.image.load('ammopack.png').convert_alpha()


#Images corresponding to the Main Menu
Instructions=pygame.image.load('Instructions.jpg').convert()
InstrBackGlowing=pygame.image.load('Instructions Back Glowing.jpg').convert()
Story=pygame.image.load('StoryBack.jpg').convert()
StoryBackGlowing=pygame.image.load('StoryBackGlowing.jpg').convert()
Credits=pygame.image.load('Credits.jpg').convert()
CreditsBackGlowing=pygame.image.load('CreditsBackGlow.jpg').convert()
BackgroundBackGlowing=pygame.image.load('DarkStar1 Back Glowing.jpg').convert()
BackgroundExitGlowing=pygame.image.load('DarkStar1 Exit Glowing.jpg').convert()


GameOverScreen=pygame.image.load(GameOver).convert()
YouWinScreen=pygame.image.load(WinScreen).convert()
PauseScreen=pygame.image.load('PauseScreen.jpg').convert()

#Sound Objects
TWD=pygame.mixer.Sound('Undaunted.ogg')
DayOne=pygame.mixer.Sound('POTE.ogg')
DOChannel=pygame.mixer.Channel(1)
Galaxy=pygame.mixer.Sound('Galaxy.ogg')
GalChannel=pygame.mixer.Channel(2)
a=0


FPS=100

last_time_ms = int(round(time.time() * 1000))

white=(255,255,255)

movex,movey=0,0

twdc=0

#This controls the HUD. 
def ShowAmmo(AmmoLeft):
    HUDx=50
    HUDy=350
    for i in range(1,AmmoLeft+1):
        screen.blit(missilefinal,(HUDx,HUDy))
        HUDx+=12
        if i%10==0:
            HUDx=50
            HUDy=HUDy+20

#--------------------------------------------------------------------------------------------CLASSES----------------------------------------------------------------------------------------------------------------------------------

class ButtonBase:
    
    def __init__(self,x,y,l,b,c,d,image,Secondary_image):
        self.x=x
        self.y=y
        self.l=l
        self.b=b
        self.Secondary_image=Secondary_image
        self.c=c
        self.d=d
        self.image=image
        self.rect=self.image.get_rect()
        
    def Draw(self,screen,constant):
        if self.c > self.x and self.c < self.x + self.l:
            if self.d > self.y and self.d < self.y + self.b:
                screen.blit(self.Secondary_image,(0,0))
                constant=1
                #pygame.display.update()
        if constant==0:
            screen.blit(self.image,(0,0))
                       
    def Verify(self):
        if self.c > self.x and self.c < self.x + self.l:
            if self.d > self.y and self.d < self.y + self.b:
                return True
            
class Ship:

    def __init__(self,x,y,image,screen1,health,HealthVar,score):

        self.x=x
        self.y=y
        self.image=image
        self.screen1=screen1
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.health=health
        self.HealthVar=HealthVar
        self.score=score
        
    def Draw(self):
        self.screen1.blit(self.image,(self.x,self.y))

    def Collision(self,Destroyer1):
            
        if (self.x+30 >=Destroyer1.x) and (self.x+30<= Destroyer1.x+233):
            if (self.y<=Destroyer1.y+341) and (self.y>=Destroyer1.y):
                return True
        if (self.x+95>Destroyer1.x) and (self.x+95<Destroyer1.x+233):
            if (self.y+165<=Destroyer1.y+341) and (self.y+165>=Destroyer1.y+341):
                return True
        if (self.x+95>Destroyer1.x) and (self.x+95<Destroyer1.x+233):
            if (self.y<=Destroyer1.y+341) and (self.y>=Destroyer1.y):
                return True
        if (self.x >=Destroyer1.x) and (self.x <= Destroyer1.x+233):
            if (self.y+165<=Destroyer1.y+341) and (self.y+165>=Destroyer1.y+341):
                return True

class SmallFry:

    def __init__(self,x,y,image,screen1,speed,SFConstant):

        self.x=x
        self.y=y
        self.image=image
        self.screen1=screen1
        self.speed=speed
        self.SFConstant=SFConstant
        
    def Draw(self):
        self.screen1.blit(self.image,(self.x,self.y))

    def Movement(self):
        self.y = self.y + self.speed
        if self.y>720:
            self.SFConstant=1

    def Collision(self,Ship,ChumpList):
            
        if (Ship.x+30 >=self.x) and (Ship.x+30<= self.x+81):
            if (Ship.y<=self.y+86) and (Ship.y>=self.y):
                return True
        if (Ship.x+95>self.x) and (Ship.x+95<self.x+81):
            if (Ship.y+165<=self.y+86) and (Ship.y+165>=self.y+86):
                return True
        if (Ship.x+95>self.x) and (Ship.x+95<self.x+81):
            if (Ship.y<=self.y+86) and (Ship.y>=self.y):
                return True
        if (Ship.x >=self.x) and (Ship.x <= self.x+81):
            if (Ship.y+165<=self.y+86) and (Ship.y+165>=self.y+86):
                return True

class Destroyer1:

    def __init__(self,x,y,image,screen1,speed,dmovex,destvar,dm,health=100):

        self.x=x
        self.y=y
        self.image=image
        self.screen1=screen1
        self.speed=speed
        self.dmovex=dmovex
        self.destvar=destvar
        self.dm=dm
        self.rect=self.image.get_rect()
        self.health=health
        
        
    def Draw(self):
        
        self.screen1.blit(self.image,(self.x,self.y))
       
    def Movement(self):
        
        if self.destvar==0:
            self.dmovex=self.dmovex+self.speed
            
        if self.destvar==1:
            self.dm=1
            self.dmovex=self.dmovex-self.speed

        self.x = self.x + self.dmovex

        if self.x+233>1280:
                self.destvar=1
                self.dmovex=0
        if self.x<266:
                self.dmovex=0
                self.destvar=0

class Missile():
    
    def __init__(self,a,b,k,speed,image,Ship,encelvar):
        
        self.a=a
        self.b=b
        self.k=k
        self.mx=Ship.x+self.a
        self.my=Ship.y +self.k*self.b
        self.speed=speed
        self.image=image
        self.rect=self.image.get_rect()
        self.encelvar=encelvar
        
    def Movement(self):
        
        self.my=self.my+ (self.k*self.speed)
        
        if Missile.Collision1(self,Destroyer,finish,Nebula,level)==True:
            if level==1:                
                if finish==0:
                    Nebula.score=Nebula.score+200
                    Destroyer.health=Destroyer.health-5
                    if Destroyer.health>0:
                        self.mx=2000
                        self.my=2000
 
        if Missile.Collision2(self,Nebula)==True:
            Nebula.health=Nebula.health-20
            Nebula.HealthVar += 1
            if Nebula.health>0:
                self.mx=2000
                self.my=2000

        if Missile.Collision4(self,Enceladus,finish,Nebula,level)==True:
            if level==2:                
                if finish==0:
                    if self.encelvar==0:                            
                        Nebula.score=Nebula.score+200
                        Enceladus.health=Enceladus.health-5
                        if Enceladus.health>0:
                            self.mx=2000
                            self.my=2000
                            
        if Missile.Collision4(self,Piranha,finish,Nebula,level)==True:
            if level==3:                
                if finish==0:
                    if self.encelvar==0:                            
                        Nebula.score=Nebula.score+200
                        Piranha.health=Piranha.health-5
                        if Piranha.health>0:
                            self.mx=2000
                            self.my=2000

    def Collision1(self,Destroyer1,finish,Ship,level):
        
        if (self.mx >=Destroyer1.x) and (self.mx <= Destroyer1.x+230):
            if (self.my<=Destroyer1.y+340) and (self.my>=Destroyer1.y):
                
                return True

    def Collision2(self,Ship):
        
        if (self.mx >=Ship.x+15) and (self.mx <= Ship.x+95):
            if (self.my<=Ship.y+165) and (self.my>=Ship.y):
                
                return True

    def Collision3(self,SmallFry,MissileList,ChumpList,Ship):
        
        if (self.mx >=SmallFry.x) and (self.mx <= SmallFry.x+81):
            if (self.my<=SmallFry.y+86) and (self.my>=SmallFry.y):

                Nebula.score=Nebula.score+100
                MissileList.remove(self)
                ChumpList.remove(SmallFry)

    def Collision4(self,Destroyer1,finish,Ship,level):
        
        if (self.mx >=Destroyer1.x) and (self.mx <= Destroyer1.x+230):
            if (self.my<=Destroyer1.y+340) and (self.my>=Destroyer1.y):
                
                return True


class Collectibles:

    def __init__(self,x,y,c,d,speed,image,screen1,var):
        
        self.x=x
        self.y=y
        self.c=c
        self.d=d
        self.speed=speed
        self.image=image
        self.screen1=screen1
        self.var=var
        

    def Draw(self):
        if Collectibles.Collectible_Collision(self,Nebula) != True:
            if self.var ==0:
                
                self.screen1.blit(self.image,(self.x,self.y))

    def Movement(self):
        self.y = self.y + self.speed

    def Collectible_Collision(self,Nebula):

        if (Nebula.x+30 >=self.x) and (Nebula.x+30<= self.x+self.c):
            if (Nebula.y<=self.y+self.d) and (Nebula.y>=self.y):
                self.var=self.var+1
                return True
        if (Nebula.x+95>self.x) and (Nebula.x+95<self.x+self.c):
            if (Nebula.y+165<=self.y+self.d) and (Nebula.y+165>=self.y+self.d):
                self.var=self.var+1
                return True
        if (Nebula.x+95>self.x) and (Nebula.x+95<self.x+self.c):
            if (Nebula.y<=self.y+self.d) and (Nebula.y>=self.y):
                self.var=self.var+1
                return True
        if (Nebula.x >=self.x) and (Nebula.x <= self.x+self.c):
            if (Nebula.y+165<=self.y+self.d) and (Nebula.y+165>=self.y+self.d):
                self.var=self.var+1
                return True

    def Health_Function(self,Nebula):
        
        if Collectibles.Collectible_Collision(self,Nebula):
            
            if Nebula.health !=100:
                Nebula.health=Nebula.health+20                
                Nebula.HealthVar = Nebula.HealthVar - 1
           
#------------------------------------------------------------------------------------------------------------/CLASSES-------------------------------------------------------------------------------------------------------------------


clock=pygame.time.Clock()
while True:

    pygame.mouse.set_visible(0)
    
    b=random.randint(0,1)
    #Incrementing 'a' such that the program doesn't "hang".
    diff_time_ms = int(round(time.time() * 1000)) - last_time_ms
    if(diff_time_ms >= 2000):
        a += 1            
        last_time_ms = int(round(time.time() * 1000))
        
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
            Intro.stop()
            TWD.stop()
        if event.type==MOUSEBUTTONDOWN:

#-----------InstructionScreen-------------------------------------------------------------------------------
            if InstructionButton.Verify():
                Condition_1=1
                while Condition_1==1:
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type==MOUSEBUTTONDOWN:
                            if InstrBack.Verify():
                                Condition_1=0
                    mouseBx1,mouseBy1= pygame.mouse.get_pos()        
                    InstrBack=ButtonBase(977,614,241,84,mouseBx1,mouseBy1,Instructions,InstrBackGlowing)
                    InstrBack.Draw(screen,0)

                    screen.blit(Icon,(mouseBx1-25,mouseBy1-25))
                    pygame.display.update()
                    clock.tick(FPS)
#-------------------------------------------------------------------------------------------------------------
                    
#-----------StoryScreen---------------------------------------------------------------------------------------
            if StoryButton.Verify():
                Condition_2=1
                while Condition_2==1:
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type==MOUSEBUTTONDOWN:
                            if StoryBack.Verify():
                                Condition_2=0
                    mouseBx2,mouseBy2= pygame.mouse.get_pos()        
                    StoryBack=ButtonBase(482,114,271,86,mouseBx2,mouseBy2,Story,StoryBackGlowing)
                    StoryBack.Draw(screen,0)

                    screen.blit(Icon,(mouseBx2-25,mouseBy2-25))
                    pygame.display.update()
                    clock.tick(FPS)
#--------------------------------------------------------------------------------------------------------------

#-----------CreditsScreen--------------------------------------------------------------------------------------
            if CreditsButton.Verify():
                Condition_3=1
                while Condition_3==1:
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type==MOUSEBUTTONDOWN:
                            if CreditsBack.Verify():
                                Condition_3=0
                    mouseBx3,mouseBy3= pygame.mouse.get_pos()        
                    CreditsBack=ButtonBase(942,614,271,87,mouseBx3,mouseBy3,Credits,CreditsBackGlowing)
                    CreditsBack.Draw(screen,0)

                    screen.blit(Icon,(mouseBx3-25,mouseBy3-25))
                    pygame.display.update()
                    clock.tick(FPS)
#--------------------------------------------------------------------------------------------------------------

            #ExitButton
            if ExitButton.Verify():
                pygame.quit()
                sys.exit()
            #GameScreen
            if PlayButton.Verify():
                Condition_4=1
                TWD.stop()
                
#---------------------------------------------------------------------Actual Game Loop--------------------------------------------------------------------------------------------------------------------------

                Nebula=Ship(685,555,ship,screen,100,0,0)
                Health_Pack=Collectibles(random.randint(300,1000),-100,50,58,0.9,HealthPack,screen,0)
                HPConstant=0

                Ammo_Pack=Collectibles(random.randint(300,1000),-100,50,51,0.9,AmmoPack,screen,0)
                APConstant=0
                
                ChumpList=[]

                ChumpList2=[]

                ChumpList3=[]
                
                for i in range(0,5):
                    SmallFryImage=pygame.image.load(SmallFries[random.randint(0,3)]).convert_alpha()
                    Chump1=SmallFry(random.randint(275,400),-100,SmallFryImage,screen,7/10.0,0)
                    ChumpList.append(Chump1)
                    Chump2=SmallFry(random.randint(480,700),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList.append(Chump2)
                    Chump3=SmallFry(random.randint(780,1000),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList.append(Chump3)
                    Chump4=SmallFry(random.randint(1000,1190),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList.append(Chump4)

                for i in range(0,5):
                    SmallFryImage=pygame.image.load(SmallFries[random.randint(0,3)]).convert_alpha()
                    Chump1=SmallFry(random.randint(275,400),-100,SmallFryImage,screen,7/10.0,0)
                    ChumpList2.append(Chump1)
                    Chump2=SmallFry(random.randint(480,700),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList2.append(Chump2)
                    Chump3=SmallFry(random.randint(780,1000),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList2.append(Chump3)
                    Chump4=SmallFry(random.randint(1000,1190),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList2.append(Chump4)

                for i in range(0,5):
                    SmallFryImage=pygame.image.load(SmallFries[random.randint(0,3)]).convert_alpha()
                    Chump1=SmallFry(random.randint(275,400),-100,SmallFryImage,screen,7/10.0,0)
                    ChumpList3.append(Chump1)
                    Chump2=SmallFry(random.randint(480,700),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList3.append(Chump2)
                    Chump3=SmallFry(random.randint(780,1000),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList3.append(Chump3)
                    Chump4=SmallFry(random.randint(1000,1190),-100,SmallFryImage,screen,random.randint(8,10)/10.0,0)
                    ChumpList3.append(Chump4)
                                  
                Destroyer=Destroyer1(607,10,villain,screen,0.05,0,0,0)
                Enceladus=Destroyer1(607,20,villain2,screen,0.05,0,0,0)
                Piranha=Destroyer1(607,10,villain3,screen,0.05,0,0,0)
                
                MissileList = []
                DestMissileList=[]
                EnceladusMissileList=[]
                PiranhaMissileList=[]
                AmmoLeft=100
                
                MissileStartCondition=0
                AllowFirst =1
                DestroyerAllowFirst=1
                EnceladusAllowFirst=1
                PiranhaAllowFirst=1
                Time1=0


                start=0
                finish=4
                WSConstant=0
                ScoreVarx=1000
                ScoreVary=0

                clock=pygame.time.Clock()
                vary=0
                varys=0
                PauseVary=0
                ShieldVary=0

                gvar=0
                DOChannel.play(DayOne,-1)
                level=1
                while Condition_4==1:
                    twdc=1
                    

                    Condition_Pause=1
                  
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type==MOUSEBUTTONDOWN:

                            if PlayBack.Verify():
                                Condition_4=0
                                
                            if PlayExit.Verify():
                                pygame.quit()
                                sys.exit()

                            if Pause.Verify():
                                while Condition_Pause==1:

                                    for Chump in ChumpList:
                                        Chump.speed=0

                                    if finish==0:
                                        Destroyer.speed=0


                                    for DMissile in DestMissileList:
                                        DMissile.speed=0

                                    PauseScreen.set_alpha(PauseVary)
                                    screen.blit(PauseScreen, (0,0))
                                    if PauseVary<5:
                                        PauseVary=PauseVary+1
                                                
                                    pygame.time.delay(30)
        
                                    for event in pygame.event.get():
                                        if event.type==QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type==MOUSEBUTTONDOWN:
                                            for Chump in ChumpList:
                                                Chump.speed=random.randint(8,10)/10.0
                                            if finish==0:
                                                Destroyer.speed=0.05

                                            for DMissile in DestMissileList:
                                                DMissile.speed=1
                                            Condition_Pause=0
                               
                                    pygame.display.update()

                    
                                
                    mouseBx4,mouseBy4= pygame.mouse.get_pos()

                    PlayBack=ButtonBase(16,612,207,35,mouseBx4,mouseBy4,background,BackgroundBackGlowing)
                    PlayBack.Draw(screen,0)
                    PlayExit=ButtonBase(16,647,207,35,mouseBx4,mouseBy4,background,BackgroundExitGlowing)
                    PlayExit.Draw(screen,0)
                    Pause=ButtonBase(230,632,26,30,mouseBx4,mouseBy4,background,background)
                    Pause.Draw(screen,0)

                    
                          

                
#-------------------Nebula Corps Ship Movement------------------------------
                    if event.type==KEYDOWN:
                        if event.key==K_LEFT:
                            movex=-2.5
                        if Nebula.x<266:
                            movex=0
                        if event.key==K_RIGHT:
                            movex=+2.5
                            if Nebula.x+110>1280:
                                movex=0
                        if event.key==K_UP:
                            movey=-2.5
                            if Nebula.y<0:
                                movey=0
                        if event.key==K_DOWN:
                            movey=+2.5
                            if Nebula.y+165>720:
                                movey=0
                                
                    if event.type==KEYUP:
                        if event.key==K_LEFT:
                            movex=0
                        if event.key==K_RIGHT:
                            movex=0
                        if event.key==K_UP:
                            movey=0
                        if event.key==K_DOWN:
                            movey=0
                    Nebula.x+=movex
                    Nebula.y+=movey
                    if Nebula.x+110>1280:
                        movex=0
                    if Nebula.x<266:
                        movex=0
                    if Nebula.y<0:
                        movey=0
                    if Nebula.y+165>720:
                        movey=0

#-----------------------------------------------------------------------------

                    #Nebula Missile Creation    
                    if event.type==KEYDOWN:
                        if event.key==K_SPACE and (time.time()-Time1>0.5 or AllowFirst) and AmmoLeft>0:
                            
                            MissileA=Missile(49,20,-1,3,missilefinal,Nebula,0)
                            MissileList.append(MissileA)
                            
                            Time1 = time.time()
                            AllowFirst=0
                            AmmoLeft -=1

                    #Killing Chumps Quickly        
                    if event.type==KEYDOWN:
                        if event.key==K_DELETE:
                            level=3

                            finish=0

#------------------------------------------------------------------------------------------------------------------LEVEL 1------------------------------------------------------------------------------------------------------------
                    if level==1:

                        #-------------------ChumpCreator--------------------------------------------------------
                        
                        for i in range(start,finish):
                            if ChumpList != []:
                            
                                if len(ChumpList)<=4:
                                    finish=len(ChumpList)-1
                                    
                                ChumpList[i].Draw()
                         
                                for MissileA in MissileList:
                                    MissileA.Collision3(ChumpList[i],MissileList,ChumpList,Nebula)
                                    
                                            
                                if ChumpList[i].SFConstant==1:
                                    ChumpList.remove(ChumpList[i])
                                
                                if ChumpList[i].Collision(Nebula,ChumpList):
                                    ChumpList.remove(ChumpList[i])
                                    Nebula.health=Nebula.health-20
                                    Nebula.HealthVar=Nebula.HealthVar+1
                                
                                ChumpList[i].Movement()
                                
                            else:
                                pass

                        if ChumpList != []:
                            if len(ChumpList)<=3:                    
                                Health_Pack.Health_Function(Nebula)
                                Health_Pack.Movement()
                                Health_Pack.Draw()

                        if ChumpList != []:
                            if len(ChumpList)<=8:
                                if Ammo_Pack.Collectible_Collision(Nebula):
                                    if APConstant==0:
                                    
                                        AmmoLeft=AmmoLeft+10
                                        APConstant=APConstant+1

                                Ammo_Pack.Movement()
                                Ammo_Pack.Draw()                    

                        #-------------------Chumps Are Dead. The Destroyer Arrives.-------------------------------------
                        if finish==0:                        

                            if Destroyer.health>0:
                                Destroyer.Draw()
                                Destroyer.Movement()
                        
                            if Destroyer.health<=0:
                                Destroyer.dm=0
                                ChumpList=[]

                                for i in DestMissileList:
                                    DestMissileList.remove(i)

                                if event.type==MOUSEBUTTONDOWN:
                                    Condition_4=0
                                
                                if event.type==KEYDOWN:
                                    if event.key==K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()

                                start=0
                                finish=4
                                
                                level=2

                            for i in range(1000):
                                if Destroyer.dm==1:
                                    if DestroyerAllowFirst:
                                        MissileDestroyerL=Missile(62,353,1,1,EnemyMissile,Destroyer,0)
                                        DestMissileList.append(MissileDestroyerL)
                                        MissileDestroyerR=Missile(142,353,1,1,EnemyMissile,Destroyer,0)
                                        DestMissileList.append(MissileDestroyerR)
                                        TimeInit=time.time()
                                        DestroyerAllowFirst=0
                            
                                    if time.time() -TimeInit >0.75:
                                    
                                        TimeInit=time.time()
                                        MissileDestroyerL=Missile(62,353,1,1,EnemyMissile,Destroyer,0)
                                        DestMissileList.append(MissileDestroyerL)
                                        MissileDestroyerR=Missile(142,353,1,1,EnemyMissile,Destroyer,0)
                                        DestMissileList.append(MissileDestroyerR)
                                    
                            for EnemyMissileObj in DestMissileList:
                                EnemyMissileObj.Movement()
                                screen.blit(EnemyMissile,(EnemyMissileObj.mx,EnemyMissileObj.my))

                            if Nebula.Collision(Destroyer):
                                Nebula.health=0
                                Nebula.HealthVar=5
                                
#----------------------------------------------------------------------------------------------------------LEVEL 2-------------------------------------------------------------------------------------------------------------------------
                    if level==2:

                        #-------------------ChumpCreator--------------------------------------------------------
                        
                        for i in range(start,finish):
                            if ChumpList2 != []:
                            
                                if len(ChumpList2)<=4:
                                    finish=len(ChumpList2)-1
                                    
                                ChumpList2[i].Draw()
                         
                                for MissileA in MissileList:
                                    MissileA.Collision3(ChumpList2[i],MissileList,ChumpList2,Nebula)
                                
                                if ChumpList2[i].SFConstant==1:
                                    ChumpList2.remove(ChumpList2[i])
                                
                                if ChumpList2[i].Collision(Nebula,ChumpList2):
                                    ChumpList2.remove(ChumpList2[i])
                                    Nebula.health=Nebula.health-20
                                    Nebula.HealthVar=Nebula.HealthVar+1
                                
                                ChumpList2[i].Movement()
                                
                            else:
                                pass

                        #-------------------Chumps Are Dead. Enceladus Arrives.-------------------------------------

                        if finish==0:
                            t=time.time()
                            
                        if finish==0:
                            
                            if Enceladus.health>0:
                                Enceladus.Draw()
                                Enceladus.Movement()
                        
                            if Enceladus.health<=0:
                                
                                ChumpList2=[]

                                for i in EnceladusMissileList:
                                    EnceladusMissileList.remove(i)

                                if event.type==MOUSEBUTTONDOWN:
                                    Condition_4=0

                                start=0
                                finish=4
                                level=3
                                  
                                if event.type==KEYDOWN:
                                    if event.key==K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()

                            for i in range(1000):
                                if Enceladus.dm==1:
                                    if EnceladusAllowFirst:
                              
                                        MissileEnceladusR=Missile(110,250,1,2,EnemyMissile,Enceladus,1)
                                        EnceladusMissileList.append(MissileEnceladusR)
                                        TimeInit=time.time()
                                        EnceladusAllowFirst=0
                            
                                    if time.time() -TimeInit >1:
                                    
                                        TimeInit=time.time()                                    
                                        MissileEnceladusR=Missile(110,250,1,2,EnemyMissile,Enceladus,1)
                                        EnceladusMissileList.append(MissileEnceladusR)

                            
                            for EnemyMissileObj in EnceladusMissileList:
                                EnemyMissileObj.Movement()
                                screen.blit(FireBall,(EnemyMissileObj.mx-15,EnemyMissileObj.my))

  
                            if Nebula.Collision(Enceladus):
                                Nebula.health=0
                                Nebula.HealthVar=5

#------------------------------------------------------------------------------------------------------------------LEVEL 3------------------------------------------------------------------------------------------------------------
                    if level==3:

                        #-------------------ChumpCreator--------------------------------------------------------
                        
                        for i in range(start,finish):
                            if ChumpList3 != []:
                            
                                if len(ChumpList3)<=4:
                                    finish=len(ChumpList3)-1
                                    
                                ChumpList3[i].Draw()
                         
                                for MissileA in MissileList:
                                    MissileA.Collision3(ChumpList3[i],MissileList,ChumpList3,Nebula)
                                    
                                            
                                if ChumpList3[i].SFConstant==1:
                                    ChumpList3.remove(ChumpList3[i])
                                
                                if ChumpList3[i].Collision(Nebula,ChumpList3):
                                    ChumpList3.remove(ChumpList3[i])
                                    Nebula.health=Nebula.health-20
                                    Nebula.HealthVar=Nebula.HealthVar+1
                                
                                ChumpList3[i].Movement()
                                
                            else:
                                pass

                        if ChumpList3 != []:
                            if len(ChumpList3)<=3:                    
                                Health_Pack.Health_Function(Nebula)
                                Health_Pack.Movement()
                                Health_Pack.Draw()

                        if ChumpList3 != []:
                            if len(ChumpList3)<=8:
                                if Ammo_Pack.Collectible_Collision(Nebula):
                                    if APConstant==0:
                                    
                                        AmmoLeft=AmmoLeft+10
                                        APConstant=APConstant+1

                                Ammo_Pack.Movement()
                                Ammo_Pack.Draw()                    

                        #-------------------Chumps Are Dead. Piranha Arrives.-------------------------------------
                        if finish==0:                        

                            if Piranha.health>0:
                                Piranha.Draw()
                                Piranha.Movement()
                        
                            if Piranha.health<=0:
                                Piranha.dm=0
                                ChumpList3=[]

                                for i in PiranhaMissileList:
                                    PiranhaMissileList.remove(i)                                

                                for i in MissileList:
                                    MissileList.remove(i)
                                AmmoLeft=0

                                Nebula.HealthVar=5

                                YouWinScreen.set_alpha(varys)
                                screen.blit(YouWinScreen, (0,0))

                                if varys<255:
                                    ScoreVarx=2000
                                    ScoreVary=2000
                                    varys=varys+1

                                if varys>=255:
                                    ScoreVarx=700
                                    ScoreVary=475
                                    


                                if event.type==MOUSEBUTTONDOWN:
                                    Condition_4=0
                                
                                if event.type==KEYDOWN:
                                    if event.key==K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()


                            for i in range(1000):
                                if Piranha.dm==1:
                                    if PiranhaAllowFirst:
                                        MissilePiranhaL=Missile(62,353,1,1,EnemyMissile,Piranha,0)
                                        PiranhaMissileList.append(MissilePiranhaL)
                                        MissilePiranhaR=Missile(142,353,1,1,EnemyMissile,Piranha,0)
                                        PiranhaMissileList.append(MissilePiranhaR)
                                        TimeInit=time.time()
                                        PiranhaAllowFirst=0
                            
                                    if time.time() -TimeInit >0.75:
                                    
                                        TimeInit=time.time()
                                        MissilePiranhaL=Missile(62,353,1,1,EnemyMissile,Piranha,0)
                                        PiranhaMissileList.append(MissilePiranhaL)
                                        MissilePiranhaR=Missile(142,353,1,1,EnemyMissile,Piranha,0)
                                        PiranhaMissileList.append(MissilePiranhaR)
                                    
                            for EnemyMissileObj in PiranhaMissileList:
                                EnemyMissileObj.Movement()
                                screen.blit(EnemyMissile,(EnemyMissileObj.mx,EnemyMissileObj.my))

                            if Nebula.Collision(Piranha):
                                Nebula.health=0
                                Nebula.HealthVar=5
                                

#-------------------Death Of Nebula--------------------------
                    if Nebula.health>0:
                        if Piranha.health>0:
                            Nebula.Draw()

                    if Nebula.health<=0:

                        DayOne.stop()

                        if level==1:
                            
                            gvar=gvar+1
                            Galaxy.play()
                        
                            Destroyer.dm=0
                            AmmoLeft=0
                            ChumpList=[]

                            if gvar>=800:
                                Galaxy.stop()
                        
                            for i in DestMissileList:
                                DestMissileList.remove(i)
                            for i in MissileList:
                                MissileList.remove(i)

                            GameOverScreen.set_alpha(vary)
                            screen.blit(GameOverScreen , (0,0))
                            if vary<255:
                                ScoreVarx=2000
                                ScoreVary=2000                            
                                vary=vary+1

                            if vary>=254:
                                ScoreVarx=1000
                                ScoreVary=475
                       
                            if event.type==MOUSEBUTTONDOWN:
                                Condition_5=0
                                Condition_4=0
                                vary=0
                                Galaxy.stop()

                            if event.type==KEYDOWN:
                                if event.key==K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()
                                    
                        if level==2:
                            
                            gvar=gvar+1
                            Galaxy.play()

                            Enceladus.dm=0
                            AmmoLeft=0
                            ChumpList2=[]

                            if gvar>=800:
                                Galaxy.stop()
                        
                            for i in EnceladusMissileList:
                                EnceladusMissileList.remove(i)
                            for i in MissileList:
                                MissileList.remove(i)

                            GameOverScreen.set_alpha(vary)
                            screen.blit(GameOverScreen , (0,0))
                            if vary<255:
                                ScoreVarx=2000
                                ScoreVary=2000                            
                                vary=vary+1

                            if vary>=254:
                                ScoreVarx=1000
                                ScoreVary=475
                       
                            if event.type==MOUSEBUTTONDOWN:
                                Condition_5=0
                                Condition_4=0
                                vary=0
                                Galaxy.stop()

                            if event.type==KEYDOWN:
                                if event.key==K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()

                        if level==3:
                            
                            gvar=gvar+1
                            Galaxy.play()

                            Piranha.dm=0
                            AmmoLeft=0
                            ChumpList3=[]

                            if gvar>=800:
                                Galaxy.stop()
                        
                            for i in PiranhaMissileList:
                                PiranhaMissileList.remove(i)
                            for i in MissileList:
                                MissileList.remove(i)

                            GameOverScreen.set_alpha(vary)
                            screen.blit(GameOverScreen , (0,0))
                            if vary<255:
                                ScoreVarx=2000
                                ScoreVary=2000                            
                                vary=vary+1

                            if vary>=254:
                                ScoreVarx=1000
                                ScoreVary=475
                       
                            if event.type==MOUSEBUTTONDOWN:
                                Condition_5=0
                                Condition_4=0
                                vary=0
                                Galaxy.stop()

                            if event.type==KEYDOWN:
                                if event.key==K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()

#-------------------------------------------------------------                            

                    ShowAmmo(AmmoLeft)

                    #Health Bar Management
                    if Nebula.HealthVar<5:
                        Img=pygame.image.load(HealthImages[Nebula.HealthVar]).convert_alpha()
                        screen.blit(Img,(65,120))

                    #Missile Movement For Nebula Corps Ship
                    for MissileA in MissileList:
                        MissileA.Movement() 
                        screen.blit(missilefinal,(MissileA.mx,MissileA.my))

                    fontobj= pygame.font.Font('BrokenGlass.ttf',80)
                    textsurfaceobj= fontobj.render('Score '+str(Nebula.score),True,white)
                    textrectobj = textsurfaceobj.get_rect()
                    textrectobj.center = (550,700)
                    screen.blit(textsurfaceobj,(ScoreVarx,ScoreVary))

                    screen.blit(Icon,(mouseBx4-25,mouseBy4-25))
                    pygame.display.update()
                    clock.tick(FPS)

                    
    mousex,mousey=pygame.mouse.get_pos()    
        
    InstructionButton=ButtonBase(304,560,317,56,mousex,mousey,Normal,InstructionsGlowing)
    #InstructionButton.Draw(screen,0)
    StoryButton=ButtonBase(687,559,309,56,mousex,mousey,Normal,StoryGlowing)
    #StoryButton.Draw(screen,0)
    CreditsButton=ButtonBase(302,618,321,56,mousex,mousey,Normal,CreditsGlowing)
    #CreditsButton.Draw(screen,0)
    ExitButton=ButtonBase(688,616,312,56,mousex,mousey,Normal,ExitGlowing)
    #ExitButton.Draw(screen,0)
    PlayButton=ButtonBase(630,592,43,48,mousex,mousey,Normal,PlayGlowing)
    #PlayButton.Draw(screen,0)
    L=[InstructionButton,StoryButton,CreditsButton,ExitButton,PlayButton]

    if event.type==KEYDOWN:
        if event.key==K_LSHIFT:
            a=10
    for i in L:
        i.Draw(screen,0)
        
    if a<= 3:
        TWD.play() 
        screen.blit(pygame.image.load(screen1[a]).convert(),(0,0))
      
    if a == 4:
        #Presents
        screen.blit(pygame.image.load(screen2[b]).convert(),(0,0))
    if a==5:
        #NebulaCorps
        screen.blit(pygame.image.load(screen3[b]).convert(),(0,0))
    if a==6:
        #vs
        screen.blit(pygame.image.load(screen4[b]).convert(),(0,0))
    if a==7:
        #DarkstarFaction
        screen.blit(pygame.image.load(screen5[b]).convert(),(0,0))
    if a==8:
        #in
        screen.blit(pygame.image.load(screen6[b]).convert(),(0,0))
    if a==9:
        #PDS
        screen.blit(pygame.image.load(screen7[1]).convert(),(0,0))
    if a==10:
        #MainMenu
        screen.blit(pygame.image.load(screen7[0]).convert(),(0,0))
        
    screen.blit(Icon,(mousex-25,mousey-25))  
    pygame.display.flip()
    clock.tick(FPS)
    
