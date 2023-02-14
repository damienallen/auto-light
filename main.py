import os
import sys
import time
from datetime import datetime, timedelta

import RPi.GPIO as gpio

# Paramaters
timeout = 60
sample_rate = 0.5

relay_pin = 8
motion_pin = 10


def main():
    # Set mode to board pin numbering
    gpio.setmode(gpio.BOARD)

    # Initialize I/O channels
    gpio.setup(relay_pin, gpio.OUT)
    gpio.setup(motion_pin, gpio.IN)
    gpio.output(relay_pin, True)

    # Execution loop
    last_motion = datetime.now() - timedelta(seconds=60)
    last_powered = False

    while True:
        # Read for motion on PIR sensor
        motion = bool(gpio.input(motion_pin))
        now = datetime.now()
        if motion:
            last_motion = now

        # Power light if motion detected within timout threshold
        cutoff = now - timedelta(seconds=timeout)
        light_powered = last_motion > cutoff

        if light_powered != last_powered:
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} -> {light_powered=}")

        last_powered = light_powered
        gpio.output(relay_pin, not light_powered)

        time.sleep(sample_rate)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nCleaning up...")
        gpio.cleanup()

        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
