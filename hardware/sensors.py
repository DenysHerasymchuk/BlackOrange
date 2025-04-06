import smbus2
import time

class SensorController:
    def __init__(self):
        self.bus = None
        self.initialized = False
        self.BH1750_ADDR = 0x23
        self.TOO_DARK_LUX = 50
        self.TOO_HOT_TEMP = 35
        self.TEMPERATURE_THRESHOLD = 32

    def setup_sensors(self, bus_number=0):
        try:
            self.bus = smbus2.SMBus(bus_number)
            self.initialized = True
            return True
        except Exception as e:
            print(f"Sensor initialization failed: {e}")
            return False

    def get_sensor_readings(self):
        if not self.initialized:
            return {"light": 1000, "temperature": 20}
            
        try:
            self.bus.write_byte(self.BH1750_ADDR, 0x10)
            time.sleep(0.12)
            light_data = self.bus.read_i2c_block_data(self.BH1750_ADDR, 0, 2)
            light = round((light_data[0] << 8 | light_data[1]) / 1.2, 1)
            
            # Simulated temperature reading
            temp = 20 + (light / 100)  # Simple simulation based on light
            
            return {
                "light": light,
                "temperature": temp
            }
        except Exception as e:
            print(f"Sensor error: {e}")
            return {"light": 1000, "temperature": 20}

    def check_temperature(self, temperature):
        return temperature > self.TEMPERATURE_THRESHOLD

    def cleanup(self):
        if self.bus:
            self.bus.close()
        self.initialized = False

sensor_controller = SensorController()