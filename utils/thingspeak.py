import time
import requests

THINGSPEAK_API_KEY = "DCJ08E9WN9A49VZL"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
last_update = 0
UPDATE_INTERVAL = 15

def update_thingspeak(field1=None, field2=None, field3=None, field4=None):
    global last_update
    current_time = time.time()
    if current_time - last_update < UPDATE_INTERVAL:
        return
    
    last_update = current_time
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': field1 if field1 is not None else 0,
        'field2': field2 if field2 is not None else 0,
        'field3': field3 if field3 is not None else 0,
        'field4': field4 if field4 is not None else 0
    }
    
    try:
        requests.post(THINGSPEAK_URL, data=payload, timeout=5)
    except Exception as e:
        print(f"ThingSpeak update failed: {e}")