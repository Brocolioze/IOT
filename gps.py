import serial
import pynmea2

def parseGPS(data):
    if data.find(b'GGA') > 0:
        msg = pynmea2.parse(data.decode())
        print("Timestamp: {} -- Lat: {} {} -- Lon: {} {} -- Altitude: {} {}".format(msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    try:
        data = serialPort.readline()
        if data:
            parseGPS(data)
    except Exception as e:
        print("Error:", e)
