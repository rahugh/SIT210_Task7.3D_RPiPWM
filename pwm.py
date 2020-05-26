#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

pwm1 = 14
trig = 21
echo = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

p = GPIO.PWM(pwm1, 300)
p.start(0)

TIME_MIN  = 0.00024
TIME_COEF = 45500
TIMEOUT = 1


def main():
    while 1:
        p.ChangeDutyCycle(dc())
        time.sleep(0.1)


def dc():
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(trig, GPIO.LOW)

    start = 0
    stop = 0

    # to avoid an infinite loop
    before = time.time()

    while GPIO.input(echo) == 0:
        start = time.time()
        if (start - before) > TIMEOUT:
            return 0

    while GPIO.input(echo) == 1:
        stop = time.time()
        if (stop - before) > TIMEOUT:
            return 0

    dist = max((stop - start - TIME_MIN) * TIME_COEF, 0)

    return max(100 - dist, 0)

try:
    main()
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

