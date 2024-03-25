import machine
import time
import network
import urequests as requests  # Bibliothèque pour effectuer des requêtes HTTP
import ure as re  # Bibliothèque pour les expressions régulières

# Configuration des broches UART pour la communication avec le module GPS
uart = machine.UART(1, baudrate=9600, tx=17, rx=16)  # Modifier les broches tx et rx selon le câblage

# Informations sur le réseau Wi-Fi
SSID = 'TECHINFOTR-IOT'
PASSWORD = 'LeSansFil0134$$'

# Paramètres de connexion MySQL
MYSQL_HOST = '172.16.86.209'
MYSQL_USER = 'anthony'
MYSQL_PASSWORD = 'Gatineau50.'
MYSQL_DB = 'BDAlawan'

def connect_wifi():
    # Configuration de la connexion Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Connexion au réseau Wi-Fi
    if not wlan.isconnected():
        print('Connexion au réseau Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connecté au réseau Wi-Fi')
    print('Adresse IP:', wlan.ifconfig()[0])

def read_gps_data():
    while True:
        if uart.any():
            gps_data = uart.readline().decode().strip()
            if gps_data.startswith('$GPGGA'):
                return gps_data
        time.sleep(0.1)

def parse_gps(data):
    match = re.search(r'\$GPGGA,(\d+\.\d+),(\d+\.\d+)', data)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude
    return None, None

def send_gps_to_mysql(latitude, longitude):
    # Construire l'URL pour l'insertion des données GPS dans la base de données MySQL
    url = f'http://{MYSQL_HOST}/insert.php?latitude={latitude}&longitude={longitude}'
    
    # Effectuer la requête HTTP pour insérer les données GPS dans la base de données MySQL
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print('Données GPS envoyées avec succès à la base de données MySQL')
    else:
        print('Échec de l\'envoi des données GPS à la base de données MySQL')

# Connexion au Wi-Fi
connect_wifi()

# Boucle principale
while True:
    gps_data = read_gps_data()
    latitude, longitude = parse_gps(gps_data)
    if latitude is not None and longitude is not None:
       print('Latitude:', latitude)
       print('Longitude:', longitude)
    send_gps_to_mysql(latitude, longitude)
    time.sleep(2.5)  # Attendre 5 secondes avant de lire les prochaines données GPS

