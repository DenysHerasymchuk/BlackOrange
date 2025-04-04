import time

def bmp280_init(bus, addr=0x77):
    calib = bus.read_i2c_block_data(addr, 0x88, 24)
    dig = {
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
    bus.write_byte_data(addr, 0xF4, 0x3F)
    return dig

def bmp280_read(dig, bus, addr=0x77):
    data = bus.read_i2c_block_data(addr, 0xF7, 8)
    adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    
    var1 = (((adc_T >> 3) - (dig['T1'] << 1)) * dig['T2']) >> 11
    var2 = (((((adc_T >> 4) - dig['T1']) * ((adc_T >> 4) - dig['T1'])) >> 12) * dig['T3']) >> 14
    t_fine = var1 + var2
    temp = (t_fine * 5 + 128) >> 8
    
    adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    
    var1 = t_fine - 128000
    var2 = var1 * var1 * dig['P6']
    var2 = var2 + ((var1 * dig['P5']) << 17)
    var2 = var2 + (dig['P4'] << 35)
    var1 = ((var1 * var1 * dig['P3']) >> 8) + ((var1 * dig['P2']) << 12)
    var1 = ((1 << 47) + var1) * dig['P1'] >> 33
    
    if var1 == 0:
        return 0, 0
    
    p = 1048576 - adc_P
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (dig['P9'] * (p >> 13) * (p >> 13)) >> 25
    var2 = (dig['P8'] * p) >> 19
    p = ((p + var1 + var2) >> 8) + (dig['P7'] << 4)
    
    return temp / 100.0, p / 25600.0  # °C, hPa

def read_sensors(bus):
    try:
        bmp280_calib = bmp280_init(bus)
        converted_lux = bh1750_read_raw(bus)
        temperature, pressure = bmp280_read(bmp280_calib, bus)
        
        return {
            "light": converted_lux,
            "temperature": temperature,
            "pressure": pressure
        }
    except Exception as e:
        print(f"Sensor error: {e}")
        return {
            "light": 1000,
            "temperature": 20,
            "pressure": 1013
        }

def bh1750_read_raw(bus, addr=0x23):
    bus.write_byte(addr, 0x10)
    time.sleep(0.12)
    data = bus.read_i2c_block_data(addr, 0, 2)
    raw = (data[0] << 8) | data[1]
    return round(raw / 1.2, 1)