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

dir_path = os.path.dirname(os.path.realpath(__file__))
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(dir_path, "PottyMsg.mp3"))