import wiringpi
import time
from hardware.sensors import sensor_controller
from utils.thingspeak import update_thingspeak

# Pin definitions
R_PIN = 14
G_PIN = 15
B_PIN = 16
LED_PINS = [3, 4, 6]

def setup_leds():
    wiringpi.wiringPiSetup()
    wiringpi.softPwmCreate(R_PIN, 0, 255)
    wiringpi.softPwmCreate(G_PIN, 0, 255)
    wiringpi.softPwmCreate(B_PIN, 0, 255)
    for pin in LED_PINS:
        wiringpi.pinMode(pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(pin, wiringpi.LOW)

def set_color(r, g, b):
    wiringpi.softPwmWrite(R_PIN, r)
    wiringpi.softPwmWrite(G_PIN, g)
    wiringpi.softPwmWrite(B_PIN, b)
    sensor_data = sensor_controller.read_sensors()
    update_thingspeak(
        field1=int(r > 0 or g > 0 or b > 0),
        field2=sensor_data['light'],
        field3=sensor_data['temperature'],
        field4=sensor_data['pressure']
    )

def run_led_chaser():
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    
    sensor_data = sensor_controller.read_sensors()
    update_thingspeak(field1=0, field2=sensor_data['light'], 
                     field3=sensor_data['temperature'], field4=sensor_data['pressure'])
    
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        update_thingspeak(field1=1, field2=sensor_data['light'],
                         field3=sensor_data['temperature'], field4=sensor_data['pressure'])
        time.sleep(0.1)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        update_thingspeak(field1=0, field2=sensor_data['light'],
                         field3=sensor_data['temperature'], field4=sensor_data['pressure'])
    
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
    update_thingspeak(field1=1, field2=sensor_data['light'],
                     field3=sensor_data['temperature'], field4=sensor_data['pressure'])
    time.sleep(0.1)
    
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    update_thingspeak(field1=0, field2=sensor_data['light'],
                     field3=sensor_data['temperature'], field4=sensor_data['pressure'])

def fancy_led_pattern():
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    
    for _ in range(2):
        for pin in LED_PINS:
            wiringpi.digitalWrite(pin, wiringpi.HIGH)
            time.sleep(0.1)
            wiringpi.digitalWrite(pin, wiringpi.LOW)
        
        for pin in reversed(LED_PINS):
            wiringpi.digitalWrite(pin, wiringpi.HIGH)
            time.sleep(0.1)
            wiringpi.digitalWrite(pin, wiringpi.LOW)
    
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
    time.sleep(0.2)
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)

def victory_light_show():
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
        (255, 0, 255)   # Magenta
    ]
    
    run_led_chaser()
    
    for _ in range(6):
        for r, g, b in colors:
            set_color(r, g, b)
            time.sleep(0.2)
            
            for i, pin in enumerate(LED_PINS):
                wiringpi.digitalWrite(pin, wiringpi.HIGH)
                time.sleep(0.1)
                if i > 0:
                    wiringpi.digitalWrite(LED_PINS[i-1], wiringpi.LOW)
            
            wiringpi.digitalWrite(LED_PINS[-1], wiringpi.LOW)

def cleanup_leds():
    set_color(0, 0, 0)
    for pin in LED_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)