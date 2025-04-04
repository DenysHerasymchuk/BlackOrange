import smbus2
import time

class SensorController:
    def __init__(self):
        self.bus = None
        self.bmp280_calib = None
        self.initialized = False
        self.BH1750_ADDR = 0x23
        self.BMP280_ADDR = 0x77
        self.TOO_DARK_LUX = 50
        self.TOO_HOT_TEMP = 35
        self.TEMPERATURE_THRESHOLD = 26

    def setup_sensors(self, bus_number=0):
        try:
            self.bus = smbus2.SMBus(bus_number)
            self._bmp280_init()
            self.initialized = True
            return True
        except Exception as e:
            print(f"Sensor initialization failed: {e}")
            return False

    def _bmp280_init(self):
        calib = self.bus.read_i2c_block_data(self.BMP280_ADDR, 0x88, 24)
        self.bmp280_calib = {
            'T1': calib[0] | (calib[1] << 8),
            'T2': (calib[2] | (calib[3] << 8)) if (calib[2] | (calib[3] << 8)) < 32768 else -((calib[2] | (calib[3] << 8)) - 65536),
            'T3': (calib[4] | (calib[5] << 8)) if (calib[4] | (calib[5] << 8)) < 32768 else -((calib[4] | (calib[5] << 8)) - 65536),
            'P1': calib[6] | (calib[7] << 8),
            'P2': (calib[8] | (calib[9] << 8)) if (calib[8] | (calib[9] << 8)) < 32768 else -((calib[8] | (calib[9] << 8)) - 65536),
            'P3': (calib[10] | (calib[11] << 8)) if (calib[10] | (calib[11] << 8)) < 32768 else -((calib[10] | (calib[11] << 8)) - 65536),
            'P4': (calib[12] | (calib[13] << 8)) if (calib[12] | (calib[13] << 8)) < 32768 else -((calib[12] | (calib[13] << 8)) - 65536),
            'P5': (calib[14] | (calib[15] << 8)) if (calib[14] | (calib[15] << 8)) < 32768 else -((calib[14] | (calib[15] << 8)) - 65536),
            'P6': (calib[16] | (calib[17] << 8)) if (calib[16] | (calib[17] << 8)) < 32768 else -((calib[16] | (calib[17] << 8)) - 65536),
            'P7': (calib[18] | (calib[19] << 8)) if (calib[18] | (calib[19] << 8)) < 32768 else -((calib[18] | (calib[19] << 8)) - 65536),
            'P8': (calib[20] | (calib[21] << 8)) if (calib[20] | (calib[21] << 8)) < 32768 else -((calib[20] | (calib[21] << 8)) - 65536),
            'P9': (calib[22] | (calib[23] << 8)) if (calib[22] | (calib[23] << 8)) < 32768 else -((calib[22] | (calib[23] << 8)) - 65536)
        }
        self.bus.write_byte_data(self.BMP280_ADDR, 0xF4, 0x3F)

    def _bmp280_read(self):
        data = self.bus.read_i2c_block_data(self.BMP280_ADDR, 0xF7, 8)
        adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        
        var1 = (((adc_T >> 3) - (self.bmp280_calib['T1'] << 1)) * self.bmp280_calib['T2']) >> 11
        var2 = (((((adc_T >> 4) - self.bmp280_calib['T1']) * ((adc_T >> 4) - self.bmp280_calib['T1'])) >> 12) * self.bmp280_calib['T3']) >> 14
        t_fine = var1 + var2
        temp = (t_fine * 5 + 128) >> 8
        
        adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        
        var1 = t_fine - 128000
        var2 = var1 * var1 * self.bmp280_calib['P6']
        var2 = var2 + ((var1 * self.bmp280_calib['P5']) << 17)
        var2 = var2 + (self.bmp280_calib['P4'] << 35)
        var1 = ((var1 * var1 * self.bmp280_calib['P3']) >> 8) + ((var1 * self.bmp280_calib['P2']) << 12)
        var1 = ((1 << 47) + var1) * self.bmp280_calib['P1'] >> 33
        
        if var1 == 0:
            return 0, 0
        
        p = 1048576 - adc_P
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self.bmp280_calib['P9'] * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.bmp280_calib['P8'] * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.bmp280_calib['P7'] << 4)
        
        return temp / 100.0, p / 25600.0

    def read_sensors(self):
        if not self.initialized:
            return {"light": 1000, "temperature": 20, "pressure": 1013}
            
        try:
            # BH1750 Light
            self.bus.write_byte(self.BH1750_ADDR, 0x10)
            time.sleep(0.12)
            light_data = self.bus.read_i2c_block_data(self.BH1750_ADDR, 0, 2)
            light = round((light_data[0] << 8 | light_data[1]) / 1.2, 1)
            
            # BMP280 Temp/Pressure
            temp, pressure = self._bmp280_read()
            
            return {
                "light": light,
                "temperature": temp,
                "pressure": pressure
            }
        except Exception as e:
            print(f"Sensor error: {e}")
            return {"light": 1000, "temperature": 20, "pressure": 1013}

    def check_temperature(self, temperature):
        return temperature > self.TEMPERATURE_THRESHOLD

    def cleanup(self):
        if self.bus:
            self.bus.close()
        self.initialized = False


sensor_controller = SensorController()
