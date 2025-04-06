import wiringpi
import time

MOTOR_PINS = [8, 9, 10, 13]
MOTOR_SEQUENCE = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

def setup_motor():
    wiringpi.wiringPiSetup()
    for pin in MOTOR_PINS:
        wiringpi.pinMode(pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(pin, wiringpi.LOW)

def rotate_motor(steps, delay=0.003):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for phase in MOTOR_SEQUENCE[::direction]:
            for pin, state in zip(MOTOR_PINS, phase):
                wiringpi.digitalWrite(pin, state)
            time.sleep(delay)
    for pin in MOTOR_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)

def dealer_bust_celebration():
    rotate_motor(100, 0.003)
    time.sleep(0.5)
    rotate_motor(-100, 0.003)
    time.sleep(0.5)
    rotate_motor(100, 0.003)

def motor_win_celebration():
    for _ in range(2):
        rotate_motor(50, 0.002)
        rotate_motor(-50, 0.002)
    dealer_bust_celebration()

def motor_short_buzz():
    rotate_motor(20, 0.003)
    rotate_motor(-20, 0.003)

def motor_shuffle_effect():
    for _ in range(3):
        rotate_motor(30, 0.004)
        rotate_motor(-30, 0.004)
        time.sleep(0.1)

def cleanup_motor():
    for pin in MOTOR_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)