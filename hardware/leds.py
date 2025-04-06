import wiringpi
import time
import logging
from utils.mqtt_client import mqtt_client
from hardware.sensors import sensor_controller

# Pin definitions
R_PIN = 14
G_PIN = 15
B_PIN = 16
LED_PINS = [3, 4, 6]

logger = logging.getLogger(__name__)

def setup_leds():
    """Initialize all LED hardware components"""
    try:
        wiringpi.wiringPiSetup()
        wiringpi.softPwmCreate(R_PIN, 0, 255)
        wiringpi.softPwmCreate(G_PIN, 0, 255)
        wiringpi.softPwmCreate(B_PIN, 0, 255)
        for pin in LED_PINS:
            wiringpi.pinMode(pin, wiringpi.OUTPUT)
            wiringpi.digitalWrite(pin, wiringpi.LOW)
        logger.info("✅ LEDs initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ LED setup failed: {e}")
        return False

def set_color(r, g, b):
    """Set RGB LED color"""
    try:
        wiringpi.softPwmWrite(R_PIN, r)
        wiringpi.softPwmWrite(G_PIN, g)
        wiringpi.softPwmWrite(B_PIN, b)
        return True
    except Exception as e:
        logger.error(f"🎨 LED color set failed: {e}")
        return False

def set_rgb_state(state):
    """Set RGB LED state (2 for green/win, 1 for yellow/tie, 0 for red/lost)"""
    try:
        if state == 2:  # Green/win
            set_color(0, 255, 0)
        elif state == 1:  # Yellow/tie
            set_color(255, 255, 0)
        else:  # Red/lost (state == 0)
            set_color(255, 0, 0)
        
        sensor_data = sensor_controller.get_sensor_readings() if sensor_controller else None
        
        if mqtt_client and mqtt_client.connected:
            mqtt_client.update_device_state(
                temperature=sensor_data.get('temperature') if sensor_data else None,
                light=sensor_data.get('light') if sensor_data else None
            )
        
        return True
    except Exception as e:
        logger.error(f"🎨 LED state set failed: {e}")
        return False

def set_three_led_state(active):
    """Set 3-LED state (1 when active, 0 otherwise)"""
    try:
        for pin in LED_PINS:
            wiringpi.digitalWrite(pin, wiringpi.HIGH if active else wiringpi.LOW)
        
        sensor_data = sensor_controller.get_sensor_readings() if sensor_controller else None
        
        if mqtt_client and mqtt_client.connected:
            mqtt_client.update_device_state(
                temperature=sensor_data.get('temperature') if sensor_data else None,
                light=sensor_data.get('light') if sensor_data else None
            )
        
        return True
    except Exception as e:
        logger.error(f"💡 3-LED state set failed: {e}")
        return False

def run_led_chaser():
    """Run LED chaser pattern"""
    try:
        for pin in LED_PINS:
            wiringpi.digitalWrite(pin, wiringpi.HIGH)
            time.sleep(0.1)
            wiringpi.digitalWrite(pin, wiringpi.LOW)
        return True
    except Exception as e:
        logger.error(f"🏃 LED chaser failed: {e}")
        return False

def cleanup_leds():
    """Turn off all LEDs and clean up resources"""
    try:
        set_color(0, 0, 0)
        for pin in LED_PINS:
            wiringpi.digitalWrite(pin, wiringpi.LOW)
        logger.info("✅ LEDs cleaned up successfully")
        return True
    except Exception as e:
        logger.error(f"🧹 LED cleanup failed: {e}")
        return False