import wiringpi
import logging
from utils.mqtt_client import mqtt_client
from hardware.sensors import sensor_controller

# Pin definitions
HIT_PIN = 11
STAND_PIN = 12

# Setup logging
logger = logging.getLogger(__name__)

def setup_buttons():
    """Initialize button pins with proper pull-up/down configuration"""
    try:
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(HIT_PIN, wiringpi.INPUT)
        wiringpi.pullUpDnControl(HIT_PIN, wiringpi.PUD_DOWN)
        wiringpi.pinMode(STAND_PIN, wiringpi.INPUT)
        wiringpi.pullUpDnControl(STAND_PIN, wiringpi.PUD_DOWN)
        logger.info("✅ Buttons initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Button setup failed: {e}")
        return False

def check_buttons():
    """Check button states"""
    try:
        hit_state = wiringpi.digitalRead(HIT_PIN) == 1
        stand_state = wiringpi.digitalRead(STAND_PIN) == 1
        
        sensor_data = sensor_controller.get_sensor_readings() if sensor_controller else None
        
        btn_state = None
        if hit_state:
            btn_state = 'h'
        elif stand_state:
            btn_state = 's'
        
        if mqtt_client and mqtt_client.connected:
            mqtt_client.update_device_state(
                temperature=sensor_data.get('temperature') if sensor_data else None,
                light=sensor_data.get('light') if sensor_data else None
            )
        
        return btn_state
        
    except Exception as e:
        logger.error(f"🛑 Button check failed: {e}")
        return None