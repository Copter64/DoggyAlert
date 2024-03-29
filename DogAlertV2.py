#Libraries
import RPi.GPIO as GPIO
import time
from config import SOUND_FILE, SHUTOFF_HOUR, SLEEP_DELAY, SHUTOFF_ENABLED
import datetime
from pathlib import Path
import pathlib
import os
import pygame


#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
gpio_calibrate_led = 17
 

def distance():
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # sensor settle time between triggers
    time.sleep(.05)
    # set Trigger to HIGH
    
    
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    if distance < 5:
        print("Too Low")
    else:
        distance = distance

    return distance

def distance_calibration():
    
    """Calibrate sensor distance

    Returns:
        float: Calibrated distance

    """
    # set GPIO Pins

    
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
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
        total_distance = distance() + total_distance
        # print(distance())

    average_distance = total_distance / x
    final_distance = average_distance - 10
    print(f"The calibrated distance is {average_distance}")
    GPIO.output(gpio_calibrate_led, False)
    print("Calibration Loop Has Ended")
    return final_distance

def doggy_detected(output_distance):
    """Please make a TLDR comment of what is happening here

    Args:
        output_distance:

    Returns:
        float: Average distance

    """
    x = 0
    total_distance = 0
    detection_distance = output_distance

    # Used in order to clean up the noise from the ultrasonic sensor, averages 25 samples
    while x < 25:
        x = x + 1
        time.sleep(SLEEP_DELAY)
        total_distance = distance() + total_distance

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

    Needs fixed, currently broken

    """
    dir_path = Path.cwd()
    sound_path = dir_path.joinpath(SOUND_FILE)
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE)

# Checking to see if any of this is needed
    # pygame.mixer.init()
    # os.path.join(dir_path, "PottyMsg.wav")
    # pygame.mixer.music.load(str(sound_path))

def doggy_detected_loop(output_distance: float):
    """Doggy detection loop helper.

    Args:
        output_distance: Detected output distance

    Returns:

    """
    doggy_detected(output_distance=output_distance)
    time.sleep(SLEEP_DELAY)

def _run():
    print("running main run_ loop")
    """Main loop pulled out from both of file.

    *TODO Make sure to improve the definition of this.

    Returns:

    """
    output_distance = distance_calibration()
    print(f"Detection Distance Set to within {output_distance} cm")

    if SHUTOFF_ENABLED:
        while datetime.datetime.now().hour < SHUTOFF_HOUR:
            doggy_detected_loop(output_distance=output_distance)
        GPIO.cleanup()
        print("Loop Broken at ShutOff Time")
    else:
        try:
            while True:
                doggy_detected_loop(output_distance=output_distance)
                print("Looking for doggos")
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("\nPeace Out")
            pass

def runstart():
    """Runs main program.

    Returns:

    """
    load_sound_and_init_mixer()
    _run()


if __name__ == '__main__':
    runstart()

    # try:
    #     output_distance = distance_calibration()
        
    #     while True:
    #         doggy_detected(output_distance)
    #         time.sleep(1)
 
    #     # Reset by pressing CTRL + C
    # except KeyboardInterrupt:
    #     print("Measurement stopped by User")
    #     GPIO.cleanup()

