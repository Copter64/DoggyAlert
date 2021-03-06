import ultrasonic_distance
import datetime
import time
import pygame
import os
import RPi.GPIO as GPIO
from pathlib import Path
from config import SOUND_FILE, SHUTOFF_HOUR, SLEEP_DELAY


# Schedule setting True or False (Enables or disabled shutoff schedule)
is_enabled = False

# Added a calibration function to auto calibrate detection distance after 10 seconds of code starting


def distance_calibration():
    """Calibrate sensor distance

    Returns:
        float: Calibrated distance

    """
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    # set GPIO Pins
    gpio_calibrate_led = 17

    # set GPIO direction (IN / OUT)
    GPIO.setup(gpio_calibrate_led, GPIO.OUT)
    GPIO.output(gpio_calibrate_led, True)
    x = 0
    total_distance = 0
    time.sleep(5)

    # this while loop runs a sample of distances 100 times and averages them
    while x < 100:
        x += 1
        time.sleep(SLEEP_DELAY)
        total_distance = ultrasonic_distance.distance() + total_distance
        print(ultrasonic_distance.distance())
        print(total_distance)

    average_distance = total_distance / x
    final_distance = average_distance - 10
    GPIO.output(gpio_calibrate_led, False)
    return final_distance


def doggy_detected(output_distance: float) -> float:
    """Please make a TLDR comment of what is happening here

    Args:
        output_distance:

    Returns:
        float: Average distance

    """
    x = 0
    total_distance = 0
    detection_distance = output_distance

    while x < 50:
        x = x + 1
        time.sleep(SLEEP_DELAY)
        total_distance = ultrasonic_distance.distance() + total_distance

    average_distance = total_distance / x

    if average_distance < detection_distance:
        print("DETECTED: Object Distance is %d cm at %dh%dm%ds" % (
            average_distance, datetime.datetime.now().hour, datetime.datetime.now().minute,
            datetime.datetime.now().second))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(SLEEP_DELAY)
            continue
    return average_distance


def load_sound_and_init_mixer():
    """Loads sound and initializes mixer with sound file.

    Returns:

    """
    dir_path = Path.cwd()
    sound_path = dir_path.joinpath(SOUND_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(dir_path, "PottyMsg.wav"))
    pygame.mixer.music.load(str(sound_path))


def doggy_detected_loop(output_distance: float):
    """Doggy detection loop helper.

    Args:
        output_distance: Detected output distance

    Returns:

    """
    doggy_detected(output_distance=output_distance)
    time.sleep(SLEEP_DELAY)


def _run():
    """Main loop pulled out from both of file.

    *TODO Make sure to improve the definition of this.

    Returns:

    """
    output_distance = distance_calibration()
    print(f'Calibrated Distance {output_distance} cm')

    if is_enabled:
        while datetime.datetime.now().hour < SHUTOFF_HOUR:
            doggy_detected_loop(output_distance=output_distance)
        GPIO.cleanup()
    else:
        try:
            while True:
                doggy_detected_loop(output_distance=output_distance)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("\nPeace Out")
            pass


def run():
    """Runs main program.

    Returns:

    """
    load_sound_and_init_mixer()
    _run()


if __name__ == '__main__':
    run()
=======
dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(dir_path, "PottyMsg.mp3"))


####Settings Section

#Distance setting in centimeters
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
	finalDistance = 0
	time.sleep(5)

	#this while loop runs a sample of distances 100 times and averages them
	while x < 100:
		x=x+1
		time.sleep(.05)
		totalDistance = ultrasonic_distance.distance() + totalDistance
		print(ultrasonic_distance.distance())
		print(totalDistance)
	
	averageDistance = totalDistance / x
	finalDistance = averageDistance - 10
	GPIO.output(GPIO_CALIBRATE_LED, False)
	return finalDistance


def doggy_detected():

	x = 0
	totalDistance = 0
	averageDistance = 0
	detectionDistance = outputdistance

	while x < 50:
		x=x+1
		time.sleep(.01)
		totalDistance = ultrasonic_distance.distance() + totalDistance
	averageDistance = totalDistance / x

	if averageDistance < detectionDistance:
		print("DETECTED: Object Distance is %d cm at %dh%dm%ds" % (averageDistance,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second))
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
				continue

	time.sleep(.1)
	return averageDistance

outputdistance = distanceCalibration()
print ("Calibrated Distance %d cm" % (outputdistance))

if scheduleEnable:
	while datetime.datetime.now().hour < shutoffTime:
		doggy_detected()
	GPIO.cleanup()

if not scheduleEnable:
    try:
        while True:
            doggy_detected()
    except KeyboardInterrupt:
		GPIO.cleanup()
		print("\nPeace Out")
		pass