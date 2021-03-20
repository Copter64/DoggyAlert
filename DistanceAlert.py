import ultrasonic_distance
import datetime
import time
import pygame
import os
import RPi.GPIO as GPIO

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(dir_path, "PottyMsg.mp3"))


####Settings Section

#Distance setting in inches
# detectionDistance = 24

#Shedule setting True or False (Enables or disabled shutoff schedule)
scheduleEnable = False

#Time setting, when schedule is enabled the time below will stop code from running by the hour, in 24hr format
shutoffTime = 9

#Added a calibration function to auto calibrate detection distance after 10 seconds of code starting
def distanceCalibration():
	#GPIO Mode (BOARD / BCM)
	GPIO.setmode(GPIO.BCM)
 
	#set GPIO Pins
	GPIO_CALIBRATE_LED = 17
	
	#set GPIO direction (IN / OUT)
	GPIO.setup(GPIO_CALIBRATE_LED, GPIO.OUT)
	GPIO.output(GPIO_CALIBRATE_LED, True)
	x = 0
	totalDistance = 0
	averageDistance = 0
	time.sleep(10)

	while x < 100:
		x=x+1
		time.sleep(.01)
		totalDistance = ultrasonic_distance.distance() + totalDistance
	
	averageDistance = totalDistance / x
	inchesDistance = averageDistance / 2.54
	detectionDistance = inchesDistance
	GPIO.output(GPIO_CALIBRATE_LED, False)
	return detectionDistance


def doggy_detected():

	x = 0
	totalDistance = 0
	averageDistance = 0
	detectionDistance = distance

	while x < 50:
		x=x+1
		time.sleep(.01)
		totalDistance = ultrasonic_distance.distance() + totalDistance

	averageDistance = totalDistance / x
	inchesDistance = averageDistance / 2.54
	print(inchesDistance)

	if inchesDistance < detectionDistance:
		print("DETECTED: Object Distance is %d inches" % (inchesDistance))
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
				continue
	return inchesDistance

distance = distanceCalibration() - 2
print ("Distance Detected %d Calibrated Distance %d inches" % (distanceCalibration(),distance))

if scheduleEnable:
	while datetime.datetime.now().hour < shutoffTime:
		doggy_detected()

if not scheduleEnable:
    try:
        while True:
            doggy_detected()
    except KeyboardInterrupt:
        pass
        print("\nPeace Out")

