import time

def bh1750_read_raw(bus, addr=0x23):
    bus.write_byte(addr, 0x10)
    time.sleep(0.12)
    data = bus.read_i2c_block_data(addr, 0, 2)
    raw = (data[0] << 8) | data[1]
    return round(raw / 1.2, 1)

def read_sensors(bus):
    try:
        converted_lux = bh1750_read_raw(bus)
        return {
            "light": converted_lux,
            "temperature": 20  # Placeholder, actual temperature reading moved to sensors.py
        }
    except Exception as e:
        print(f"Sensor error: {e}")
        return {
            "light": 1000,
            "temperature": 20
        }