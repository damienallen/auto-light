from time import time

import micropython
from machine import Pin, Timer

# Allocate memory for intercept exception handling
micropython.alloc_emergency_exception_buf(100)


class AutoLight:
    """
    Class to take advantage of shared memory space for interrupt handlers
    https://docs.micropython.org/en/latest/reference/isr_rules.html#isr-rules
    """

    def __init__(self, timer):
        # Sensing frequency (s)
        frequency = 1 / 2

        # Motion timeout (s)
        self.timeout = 10

        # I/O setup
        self.relay = Pin(22, Pin.OUT)
        self.motion = Pin(21, Pin.IN)

        # Power motion sensor pin
        motion_power = Pin(20, Pin.OUT)
        motion_power.value(1)

        # State
        self.start_time = time()
        self.last_motion = self.start_time - self.timeout
        self.last_powered = False

        # Start timer
        timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self.callback)

    def callback(self, timer):
        """
        Adjust light setting based on motion
        """

        # Read for motion on PIR sensor
        motion_detected = self.motion.value() == 1

        now = time()
        if motion_detected:
            self.last_motion = time()

        # Power light if motion detected within threshold
        since_last_motion = now - self.last_motion
        since_start = now - self.start_time

        light_powered = since_last_motion < self.timeout
        self.relay.value(1 if not light_powered else 0)

        if not light_powered == self.last_powered:
            self.last_powered = light_powered
            print(f"{since_start} seconds elapsed | {light_powered=}")


auto_light = AutoLight(Timer())
