import os
import sys
import time

import RPi.GPIO as gpio

relay_pin = 8
motion_pin = 10


def main():
    # Set mode to board pin numbering
    gpio.setmode(gpio.BOARD)

    # Initialize I/O channels
    gpio.setup(relay_pin, gpio.OUT)
    gpio.setup(motion_pin, gpio.IN)

    while True:
        motion = gpio.input(motion_pin)
        print(f"Motion: {motion}")

        light_powered = motion == 0
        gpio.output(relay_pin, light_powered)

        time.sleep(1)


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
