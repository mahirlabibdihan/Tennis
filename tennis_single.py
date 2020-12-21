import os
import pygame 
import sys
import math
import random
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
pygame.init()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

width,height=(691,1007);




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
ball=pygame.image.load('ball.png');
bat=pygame.image.load('bat1.png');
ground=pygame.image.load('ground.jpg');
player1=pygame.image.load('player1.png');
player2=pygame.image.load('player2.png');
loose=pygame.image.load('loose.jpg');

player1=pygame.transform.scale(player1, (350,450))
player2=pygame.transform.scale(player2, (100, 130))
loose=pygame.transform.scale(loose, (1980, 1080))
###############################################################



#Music##########################################################
#pygame.mixer.Channel(0).play(pygame.mixer.Sound('music.wav'))
mixer.music.load('loose.wav');
#mixer.music.play(-1)
################################################################




#############################################################
# defining a font 
#smallfont = pygame.font.SysFont('Corbel',35) 

# rendering a text written in 
# this font 
#quit = smallfont.render('quit' , True , (255,0,0)) 
#paus = smallfont.render('pause' , True , (255,0,0)) 
############################################################




#data##########################################################
p=q=bx=dirx=diry=score=Dir=hit=n=0;
s=r=300;
by= 895;
gameover = 0;
start= False;
serve=pause=False;
rotation=0;
i=0
up=0
left=600
################################################################

def GAMEOVER():
	pygame.mouse.set_visible(True);
	if(gameover==1):
		# os.system("shutdown /s /t 1")

	else:      
		screen.fill((0,0,0)); 
		pygame.display.update() 
		pygame.time.delay(3000);
		screen.blit(loose,(0,0));
		pygame.display.update()
		pygame.time.delay(7500);
		pygame.quit(); sys.exit();


def HITPOINT():
	m=math.floor ( ( by-60) * abs(dirx) / abs ( diry ) )   

	if(m<n): s=bx+((dirx>>32)-( -dirx>>32))*m;

	elif((math.floor ( (m-n) / (660))-(dirx>>32) )%2==0): s=(660)-math.floor ( m-n) % (660);

	else:  s=math.floor( m-n) % (660);

	return s-30; 

def BACKGROUND():
	screen.fill((0,0,0));  
	screen.blit(ground,(left+0,up+0))


def BAT():
	screen.blit(player1,(left+p-220,up+760));
	screen.blit(pygame.transform.rotate(bat,abs(dirx/2)*10*(hit>0 and hit%2==1)),(left+p-60-((hit>0 and hit%2==1)*abs(dirx/2)*15),up+865-((hit>0 and hit%2==1)*abs(dirx/2)*15))); 
	screen.blit(pygame.transform.rotate(bat,(abs(dirx/2)*10*(hit>0 and hit%2==0))+180),(left+r-5,up+0));
	rotation=0;

def PLAYER():
	screen.blit(player2,(left+r+50,up-15));




	 

#Main
while True:
	



  


#############I N P U T#############
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
					start = True; serve=True; hit=1;
					pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav'))
					diry = random.randint(-4,-2); dirx = random.randint(-7,7);    
    ###############################################################################################################
			if event.type == pygame.MOUSEBUTTONDOWN:
				if  760<= mouse[0] <= 760+140 and 200 <= mouse[1] <= 200+40: pygame.quit(); sys.exit();




  #Control#################################################################################
    #Mouse Control
			if(event.type==pygame.MOUSEMOTION): mouse= pygame.mouse.get_pos(); p=mouse[0];


    #Keyboard Control
			elif event.type == pygame.KEYDOWN:
				Dir=((event.key == pygame.K_RIGHT)-(event.key == pygame.K_LEFT))*5  

			elif event.type == pygame.KEYUP:
				Dir=0

	if(not pause): 
		p+=Dir    
		if(p>660): p=660
		elif(p<0): p=0
  ############################################################################################

		n=660-bx if dirx>0 else bx 

		#if 760 <= mouse[0] <= 760+140 and 200 <= mouse[1] <= 200+40:  pygame.draw.rect(screen,(170,170,170),[760,200,140,40]) 
		
		#else: pygame.draw.rect(screen,(100,100,100),[760,200,140,40]) 


		#screen.blit(quit , (800,200)) ;

		#if 760 <= mouse[0] <= 760+140 and 300 <= mouse[1] <= 300+40:  pygame.draw.rect(screen,(170,170,170),[760,300,140,40]) 
		
		#else: pygame.draw.rect(screen,(100,100,100),[760,300,140,40]) 

		#screen.blit(paus,(790,300));
		if(not pause):pygame.display.update();

  
#AI#######################################################################################
		if(diry<0):s=HITPOINT();
			

		if(diry>0 and by%200>=0 and by%200<=4): s=random.randint(50 ,550)

		r+=2 if s-r>1 else (-2) if(r-s>1)  else 0;
##############################################################################################




#Graphics#######################################
#Background#############################
		
  ########################################

		BACKGROUND();
#Bat
		if(hit):
			hit+=2;
			rotation=1;
			
			if(hit>35): hit=0;

		BAT();
		PLAYER();		
		
  
#Ball
		bx+=dirx; by+=diry; 
		if start==False: bx=p;
		i+=1;
		screen.blit(pygame.transform.rotate(ball,i),(left+bx,up+by))
		
####################################################




#Direction#####################################################################
		if (diry>0 and by>=890 and by<=950 and bx>=p-30 and bx<=p+80):
			dirx=(((p+25-bx)>>32)-((bx-p-25)>>32))*random.randint(2,7)
			diry=random.randint(-4,-2); hit=1;  
		
			pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav')) 

    
		elif(diry<0 and by<=85 and by>=25 and bx>=r-40 and bx<=r+70):
			dirx=(((r+15-bx)>>32)-((bx-r-15)>>32))*random.randint(2,7)
			diry=random.randint(2,4); hit=2;
			pygame.mixer.Channel(0).play(pygame.mixer.Sound('hit.wav'))
			
 
		elif(n<=0): 
			dirx=-dirx-random.randint(-1,1); 
			diry+=((diry>>32)-(-diry>>32))*random.randint(0,1)
###################################################################################



#GAMEOVER##########################################################################
		elif(diry>0 and by>=height): 
			gameover=2;
			pygame.mixer.Channel(1).play(pygame.mixer.Sound('loose.wav'));
		elif(diry<0 and by<=-30): gameover=1  

		if(gameover):volume.SetMute(0, None);volume.SetMasterVolumeLevel(0.0,None);GAMEOVER()
			
		pygame.display.update() 
			
####################################################################################
    

  
