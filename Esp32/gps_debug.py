import machine
import time
import network

uart = machine.UART(1, baudrate=9600, tx=machine.Pin(17), rx=machine.Pin(16))

SSID = 'TECHINFOTR-IOT'
PASSWORD = 'LeSansFil0134$$'

def print_pin_info(pin):
    print(f"Broche {pin}: État = {pin.value()}")

def read_gps_data():
    gps_data = []
    while True:
        if uart.any():
            line = uart.readline().decode().strip()
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                gps_data.append(line)
        time.sleep(1.0)
        if len(gps_data) >= 2:
            return gps_data

def write_to_txt_file(data, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write('\n'.join(data))
            print(f"Données GPS écrites dans '{output_file}' avec succès.")
    except IOError:
        print("Erreur lors de l'écriture dans le fichier.")

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connecté au réseau Wi-Fi')
    print('Adresse IP:', wlan.ifconfig()[0])

def main():
    output_txt_file = "gps_data.txt"
    gps_data = read_gps_data()
    gps_data = read_gps_data()
    write_to_txt_file(gps_data, output_txt_file)
    
    connect_wifi()
    
    print_pin_info(machine.Pin(17))
    print_pin_info(machine.Pin(16))

    try:
        with open(output_txt_file, 'r') as file:
            file_content = file.read()
            print("Contenu du fichier GPS:")
            print(file_content)
    except FileNotFoundError:
        print("Le fichier GPS n'a pas été trouvé.")

if __name__ == "__main__":
    main()

