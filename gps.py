import serial
import pynmea2

def parseGPS(data):
    if data.find(b'GGA') > 0:
        msg = pynmea2.parse(data.decode())
        return "{},{},{},{},{}".format(msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir)

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

with open("gps_data.txt", "w") as file:
    while True:
        try:
            data = serialPort.readline()
            if data:
                gps_data = parseGPS(data)
                if gps_data:
                    file.write(gps_data + "\n")
                    print(gps_data)  
        except Exception as e:
            print("Error:", e)
