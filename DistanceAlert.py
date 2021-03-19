import ultrasonic_distance
import datetime
import time
import pygame
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(dir_path, "PottyMsg.mp3"))


####Settings Section

#Distance setting in inches
detectionDistance = 24

#Shedule setting True or False (Enables or disabled shutoff schedule)
scheduleEnable = False

#Time setting, when to turn it off in the morning by the hour 24hr format
shutoffTime = 9


    
def doggy_detected():
	import ultrasonic_distance
	import pygame

    	x=0
    	totalDistance = 0
    	averageDistance = 0
    
    	while x < 50:
        	x=x+1
        	time.sleep(.01)
        	totalDistance = ultrasonic_distance.distance() + totalDistance
        
    	averageDistance = totalDistance / x
    	inchesDistance = averageDistance / 2.54


    	if inchesDistance < detectionDistance:
       		pygame.mixer.music.play()
        	while pygame.mixer.music.get_busy() == True:
            		continue

	print(averageDistance)
    	print(inchesDistance)

	
if scheduleEnable == True:
	while datetime.datetime.now().hour < shutoffTime:
        	doggy_detected()

if scheduleEnable == False:
    try:
        while True:
            doggy_detected()
    except KeyboardInterrupt:
        pass
        print("\nPeace Out")
