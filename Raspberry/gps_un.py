import random
import time
import machine


uart = machine.UART(1, baudrate=9600, tx=17, rx=16)  
def generate_random_gps_data():

    latitude = random.uniform(-90, 90)

    longitude = random.uniform(-180, 180)
  
    localtime = time.localtime()
    date_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(localtime[0], localtime[1], localtime[2], localtime[3], localtime[4], localtime[5])

    precision = random.uniform(0, 10)

    gps_data = f"$GPGGA,{date_time},{latitude:.6f},N,{longitude:.6f},W,1,8,0.9,{precision:.1f},M,46.9,M,,"
    return gps_data

def main():
  
    for _ in range(10):  
        gps_data = generate_random_gps_data()
        print("Données GPS:", gps_data)

if __name__ == "__main__":
    main()
