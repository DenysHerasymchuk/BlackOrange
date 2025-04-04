import wiringpi

HIT_PIN = 11
STAND_PIN = 12

def setup_buttons():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(HIT_PIN, wiringpi.INPUT)
    wiringpi.pullUpDnControl(HIT_PIN, wiringpi.PUD_DOWN)
    wiringpi.pinMode(STAND_PIN, wiringpi.INPUT)
    wiringpi.pullUpDnControl(STAND_PIN, wiringpi.PUD_DOWN)

def check_buttons():
    if wiringpi.digitalRead(HIT_PIN) == 1:
        return 'h'
    elif wiringpi.digitalRead(STAND_PIN) == 1:
        return 's'
    return None