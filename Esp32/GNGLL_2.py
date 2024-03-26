import machine
import time
import urequests as requests
import _thread
import network  # Ajout de l'importation manquante

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)
BLUE_LED_PIN = 2
BLUE_LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)
# Variable globale pour indiquer si les threads doivent continuer à s'exécuter
running = True

SSID = 'TECHINFOTR-IOT'
PASSWORD = 'LeSansFil0134$$'

MYSQL_HOST = '172.16.86.209'
MYSQL_USER = 'anthony'
MYSQL_PASSWORD = 'Gatineau50.'
MYSQL_DB = 'BDAlawan'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connexion au réseau Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
        print('Connecté au réseau Wi-Fi')
        ip_address = wlan.ifconfig()[0]
        print('Adresse IP:', ip_address)
        return True
    else:
        print('Déjà connecté au réseau Wi-Fi')
        ip_address = wlan.ifconfig()[0]
        print('Adresse IP:', ip_address)
        return False
    
    
def send_gps_to_server(latitude, longitude):
    url = 'http://{}/insert.php?latitude={}&longitude={}'.format(MYSQL_HOST, latitude, longitude)
    response = requests.get(url)
    if response.status_code == 200:
        print('Données GPS envoyées avec succès au serveur')
    else:
        print('Échec de l\'envoi des données GPS au serveur')

def lire_trames_gps():
    global running
    start_time = time.time()
    while running and time.time() - start_time < 30:  # Exécuter pendant 3 minutes (180 secondes)
        try:
            if uart.any():
                trame_gps = uart.readline()
                print("Trame GPS brute:", trame_gps)
                if trame_gps.startswith(b'$GNGLL'):  # Filtrer les trames GNGLL
                    # Séparation des données
                    trame_split = trame_gps.split(b',')
                    if len(trame_split) >= 5:
                        latitude = trame_split[1]
                        longitude = trame_split[3]
                        print("Latitude:", latitude)
                        print("Longitude:", longitude)
                        # Écriture dans le fichier
                        with open("gps.txt", 'a') as fichier:
                            fichier.write("Latitude: {}\tLongitude: {}\n".format(latitude.decode('utf-8', 'ignore'), longitude.decode('utf-8', 'ignore')))
        except Exception as e:
            print("Erreur lors de la lecture des données GPS:", e)
        time.sleep(0.1)
    
    # Une fois la lecture terminée, connectez-vous au WiFi et clignotez la LED bleue
    if connect_wifi():
        blink_blue_led()  # Clignoter la LED bleue après la connexion Wi-Fi réussie

def blink_blue_led():
    for _ in range(3):
        BLUE_LED.on()
        time.sleep(0.5)
        BLUE_LED.off()
        time.sleep(0.5)

def main():
    _thread.start_new_thread(lire_trames_gps, ())
    # Exécuter pendant 3 minutes (180 secondes)
    time.sleep(30)
    # Arrêter les threads
    print("Arrêt des threads...")
    global running
    running = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Arrêt des threads...")
        running = False


