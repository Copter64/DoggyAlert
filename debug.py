import DogAlertV2
import time

while DogAlertV2.distance() > 0:
    print(DogAlertV2.distance())
    time.sleep(.1)