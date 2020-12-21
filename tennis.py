import os
import pygame 
import sys
import math
import random
import hashlib
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
pygame.init()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


height=1007
width=691
p=q=bx=dirx=diry=score=Dir=hit=n=i=gameover=player=0;
s=r=300;
by= 895;
start=pause=False;
up=35
left=600
################################################################



################################ W I N D O W ###################################################### 
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
screen = pygame.display.set_mode((1920,1080),pygame.NOFRAME);
###################################################################################################


#Mouse########################################################
pygame.mouse.set_visible(False);
pygame.mouse.set_cursor(*pygame.cursors.diamond)
##############################################################


#Title##########################################################
pygame.display.set_icon(pygame.image.load('tennis.ico'));
pygame.display.set_caption("Tennis");
##############################################################



#Image########################################################
ball=pygame.image.load('ball.png');print(ball)
bat=pygame.image.load('bat1.png');print(bat)
ground=pygame.image.load('ground.jpg');
player1=pygame.image.load('player1.png');
player2=pygame.image.load('player2.png');
loose=pygame.image.load('loose.jpg');
win=pygame.image.load('win.jpg');
cursor=pygame.transform.scale(bat, (50,50))
player1=pygame.transform.scale(player1, (350,450))
player2=pygame.transform.scale(player2, (100, 130))
loose=pygame.transform.scale(loose, (1980, 1080))
#ground=pygame.transform.scale(ground, (880, 1080))

###############################################################



#Music##########################################################
#pygame.mixer.Channel(0).play(pygame.mixer.Sound('music.wav'))
mixer.music.load('loose.wav');
#mixer.music.play(-1)
################################################################



#############################################################
# defining a font 
smallfont = pygame.font.SysFont('Corbel',35)  
single = smallfont.render('Single Player' , True , (255,0,0)) 
double = smallfont.render('Double Player' , True , (255,0,0)) 
############################################################


def RESET():
	global p,bx,diry,dirx,Dir,hit,s,r,by,gameover,start,pause,i;
	p=bx=dirx=diry=Dir=hit=n=0;
	s=r=300;
	by= 895;
	gameover = 0;
	start= False;
	pause=False;
	i=0

def GAMEOVER():

	global gameover,player;
	pygame.mouse.set_visible(False);
	if(gameover==1): 	
		player=0;
		RESET();
		PLAYER_NUMBER();
		#os.system("shutdown /s /t 1")

	elif(gameover==2):      
		screen.fill((0,0,0)); 
		pygame.display.update() 
		pygame.time.delay(3000);
		screen.blit(loose,(0,0));
		pygame.display.update()
		pygame.time.delay(7500);
		player=0;
		RESET();
		PLAYER_NUMBER();
		#pygame.quit(); sys.exit();



def HITPOINT():
	global s
	m=math.floor ( ( by-60) * abs(dirx) / abs ( diry ) )   

	if(m<n): s=bx+((dirx>>32)-( -dirx>>32))*m;
	elif((math.floor ( (m-n) / (660))-(dirx>>32) )%2==0): s=(660)-math.floor ( m-n) % (660);
	else:  s=math.floor( m-n) % (660);

	s-=30; 

def BACKGROUND():
	screen.fill((0,0,0));  
	screen.blit(ground,(left+0,up+0))


def BALL():
	global bx,by,i
	bx+=dirx; by+=diry; 
	if start==False: bx=p;
	i+=1;
	screen.blit(pygame.transform.rotate(ball,i),(left+bx,up+by))

def PLAYER():
	screen.blit(player2,(left+r+50,up-15));
	screen.blit(player1,(left+p-220,up+760));

def PLAYER_NUMBER():
	global player
	while(player==0):

		BACKGROUND();
		mouse = pygame.mouse.get_pos();

		for event in pygame.event.get():

			if event.type == pygame.MOUSEBUTTONDOWN:
				if 830 <= mouse[0] <= 830+260 and 480 <= mouse[1] <= 480+57:
					player=1;
				elif 830 <= mouse[0] <= 830+260 and 590 <= mouse[1] <= 590+57:
					player=2;
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit(); sys.exit(); 

		if 830 <= mouse[0] <= 830+260 and 480 <= mouse[1] <= 480+57:  pygame.draw.rect(screen,(170,170,170),[830,480,260,57]) 		
		else: pygame.draw.rect(screen,(100,100,100),[830,480,260,57]) 
		screen.blit(single , (870,490)) ;


		if 830 <= mouse[0] <= 830+260 and 590 <= mouse[1] <= 590+57:  pygame.draw.rect(screen,(170,170,170),[830,590,260,57]) 		
		else: pygame.draw.rect(screen,(100,100,100),[830,590,260,57]) 
		screen.blit(double , (870,600)) ;
		screen.blit(cursor,(mouse[0],mouse[1]));


		pygame.display.update() 


	pygame.mouse.set_visible(False);
#########################################################################################################################################
def BAT():
	
	screen.blit(pygame.transform.rotate(bat,abs(dirx/2)*10*(hit>0 and hit%2==1)),(left+p-60-((hit>0 and hit%2==1)*abs(dirx/2)*15),up+865-((hit>0 and hit%2==1)*abs(dirx/2)*15))); 
	screen.blit(pygame.transform.rotate(bat,(abs(dirx/2)*10*(hit>0 and hit%2==0))+180),(left+r-5,up+0));




def INPUT():
	global Dir,left,up,start,hit,dirx,diry,p,pause,q;
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN or event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			pause= not pause; 
			    
    #Quit#########################################################################################################
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit(); sys.exit(); 
    ##############################################################################################################


		if(not pause):
    #Start########################################################################################################
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				if start==False:
					start = True; hit=1;
					pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav'))
					diry = random.randint(-4,-2); dirx = random.randint(-7,7);    
    ###############################################################################################################

  #Control#################################################################################
    #Mouse Control
			if(event.type==pygame.MOUSEMOTION): mouse = pygame.mouse.get_pos(); p=mouse[0]; q=mouse[1];
			

    #Keyboard Control
			elif event.type == pygame.KEYDOWN:
				Dir=((event.key == pygame.K_RIGHT)-(event.key == pygame.K_LEFT))*5  
				if event.key == pygame.K_KP4: left-=10;
				elif event.key == pygame.K_KP6: left+=10;
				elif event.key == pygame.K_KP8: up-=10;
				elif event.key == pygame.K_KP2: up+=10;
				elif event.key == pygame.K_KP5: up=35;left=600;

			elif event.type == pygame.KEYUP:
				Dir=0
			


def KEYBOARD_BAT():
	global p,r 
	if(player==1):p+=Dir    
	else:
		if(r+Dir>-60 and r+Dir<630): r+=Dir

	if(p>660): p=660
	elif(p<0): p=0


def DIRECTION():
	global dirx,diry,hit,gameover
	if (diry>0 and by>=890 and by<=950 and bx>=p-30 and bx<=p+80):
		dirx=(((bx-p-25)>>32)-((p+25-bx)>>32))*random.randint(2,7)
		diry=random.randint(-4,-2); hit=1;  		
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav')) 
    
	elif(diry<0 and by<=85 and by>=25 and bx>=r-40 and bx<=r+70):
		dirx=(((r+15-bx)>>32)-((bx-r-15)>>32))*random.randint(2,7)
		diry=random.randint(2,4); hit=2;
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav'))			
 
	elif(n<=0): 
		dirx=-dirx-random.randint(-1,1); 
		diry+=((diry>>32)-(-diry>>32))*random.randint(0,1)	

	elif(diry>0 and by>=height): 
		gameover=2;
		volume.SetMute(0, None);
		volume.SetMasterVolumeLevel(0.0, None);
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('loose.wav'));

	elif(diry<0 and by<=-30): gameover=1  



def AI():
	global r,s
	if(player==1):
		if(diry<0): HITPOINT();			
		if(diry>0 and by%200>=0 and by%200<=4): s=random.randint(50 ,550)
		r+=2 if s-r>1 else (-2) if(r-s>1)  else 0;



def DRAW():
	BACKGROUND();
	PLAYER();	
	BAT();
	BALL();

	
	 

def main():
	global r,s,n,hit
	while(not gameover):
		PLAYER_NUMBER()
		INPUT();
		if(not pause):
			KEYBOARD_BAT()
			n=660-bx if dirx>0 else bx 
			AI();
			if(hit): hit=hit+2 if hit<36 else 0;
			DRAW();
			DIRECTION();
			pygame.display.update();
			GAMEOVER()
			
			
  
main()  

  
