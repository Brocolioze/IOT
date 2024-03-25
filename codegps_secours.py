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

def read_and_write_gps_data():
    start_time = time.time()
    while time.time() - start_time < 5:  # Lire pendant 5 secondes
        if uart.any():
            gps_line = uart.readline()
            print("Données GPS brutes:", gps_line)  # Ajout pour le débogage
            if b'$GPGGA' in gps_line:
                write_to_txt_file(gps_line, "gps_data.txt")  # Écrire les données dans le fichier

def write_to_txt_file(data, output_file):
    try:
        with open(output_file, 'a') as file:  # Utiliser le mode 'a' pour ajouter les données à la fin du fichier
            file.write(data.decode())  # Décode les données et les écrit dans le fichier
            file.flush()  # Forcer l'écriture immédiate des données dans le fichier
        print("Données GPS ajoutées dans '{}' avec succès.".format(output_file))  # Indiquer qu'une donnée GPS a été écrite
        blink_blue_led()
    except IOError:
        print("Erreur lors de l'écriture dans le fichier.")

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
    read_and_write_gps_data()
    if connect_wifi():
        # Lire les données GPS depuis le fichier
        with open("gps_data.txt", 'r') as file:
            gps_lines = file.readlines()
            for gps_line in gps_lines:
                # Assurez-vous que les données GPS sont correctement formatées avant de les envoyer au serveur
                if ',' in gps_line:
                    latitude, longitude = gps_line.strip().split(',')
                    send_gps_to_server(latitude, longitude)

if __name__ == "__main__":
    main()

