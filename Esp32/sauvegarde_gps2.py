import machine
import time
import network
import urequests as requests

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

SSID = 'TECHINFOTR-WF'
PASSWORD = 'LeSansFil0134$$'

MYSQL_HOST = '172.16.86.209'
MYSQL_USER = 'anthony'
MYSQL_PASSWORD = 'Gatineau50.'
MYSQL_DB = 'BDAlawan'

BLUE_LED_PIN = 2  
BLUE_LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)

def read_gps_data():
    gps_data = b""
    start_time = time.time()
    while time.time() - start_time < 10:
        if uart.any():
            gps_line = uart.readline()
            print("Ligne GPS brute:", gps_line)  
            if gps_line.startswith(b'$GPGGA'):
                gps_data += gps_line
                print("Données GPS mises à jour:", gps_data)
        time.sleep(0.1)
    return gps_data.decode('utf-8', 'ignore')


def write_to_txt_file(data, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(data)
            print("Données GPS écrites dans '{}' avec succès.".format(output_file))
            print("Contenu du fichier:")
            file.seek(0)  # Revenir au début du fichier
            print(file.read())  # Lire et afficher le contenu du fichier
            blink_blue_led()
    except Exception as e:
        print("Erreur lors de l'écriture dans le fichier:", e)

def blink_blue_led():
    for _ in range(3):  
        BLUE_LED.on()
        time.sleep(0.5)
        BLUE_LED.off()
        time.sleep(0.5)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connexion au réseau Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connecté au réseau Wi-Fi')
    print('Adresse IP:', wlan.ifconfig()[0])
    blink_blue_led()
    return True

def send_gps_to_server(latitude, longitude):
    url = 'http://{}/insert.php?latitude={}&longitude={}'.format(MYSQL_HOST, latitude, longitude)
    response = requests.get(url)
    if response.status_code == 200:
        print('Données GPS envoyées avec succès au serveur')
    else:
        print('Échec de l\'envoi des données GPS au serveur')

def main():
    gps_data = read_gps_data()
    print("Données GPS lues:", gps_data)
    write_to_txt_file(gps_data, "gps.txt")
    
    if connect_wifi():
        with open("gps.txt", 'r') as file:
           print("Contenu du fichier:")
           print(file.read())
           # for gps_line in gps_lines:
            #    latitude, longitude = gps_line.strip().split(',')
             #   send_gps_to_server(latitude, longitude)

if __name__ == "__main__":
    main()

