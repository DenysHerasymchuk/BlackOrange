import paho.mqtt.client as mqtt
import time
import logging

# Configuration constants
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "channels/2900447/publish"
MQTT_CLIENT_ID = "KDc8DC0lKgMwECMvHyQ1My4"
MQTT_USER = "KDc8DC0lKgMwECMvHyQ1My4"
MQTT_PWD = "30N7E1mtJAqYu1xNfIEP6Q78"

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(MQTT_USER, MQTT_PWD)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.connected = False
        self.logger = logging.getLogger(__name__)

    def _on_connect(self, client, userdata, flags, rc, *extra_args):
        if rc == 0:
            self.logger.info("✅ Connected to ThingSpeak MQTT Broker!")
            self.connected = True
        else:
            self.logger.error(f"❌ Failed to connect, return code {rc}")
            self.connected = False

    def _on_disconnect(self, client, userdata, disconnect_flags, rc, properties=None):
        self.logger.warning(f"⚠️ Disconnected (rc: {rc})")
        self.connected = False
        if rc != 0:
            self.reconnect()

    def _on_publish(self, client, userdata, mid, reason_code, properties):
        if reason_code == 0:
            self.logger.debug(f"📤 Message published (mid: {mid})")
        else:
            self.logger.error(f"❌ Failed to publish (mid: {mid}, reason: {reason_code})")

    def connect(self):
        try:
            self.logger.info("🔗 Connecting to MQTT broker...")
            self.client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
            self.client.loop_start()
        except Exception as e:
            self.logger.error(f"🔥 Connection error: {e}")
            self.reconnect()

    def reconnect(self):
        while not self.connected:
            try:
                self.logger.info("🔄 Attempting to reconnect...")
                self.connect()
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"🔥 Reconnect failed: {e}")
                time.sleep(5)

    def publish_state(self, payload):
        if not self.connected:
            self.logger.warning("⚠️ Not connected, cannot publish")
            return False
            
        try:
            if isinstance(payload, dict):
                payload = '&'.join([f"{k}={v}" for k, v in payload.items()])
            result = self.client.publish(MQTT_TOPIC, payload)
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            self.logger.error(f"📤 Publish error: {e}")
            return False

    def update_device_state(self, temperature=None, light=None):
        """Update device states with only temperature and light fields"""
        payload = {}
        
        # Field 4: Temperature
        if temperature is not None:
            payload['field4'] = temperature
            
        # Field 5: Light sensor
        if light is not None:
            payload['field5'] = light
            
        return self.publish_state(payload)

    def cleanup(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.logger.info("✅ MQTT connection closed cleanly")
        except Exception as e:
            self.logger.error(f"⚠️ Error during cleanup: {e}")

# Initialize MQTT client
mqtt_client = MQTTClient()
mqtt_client.connect()