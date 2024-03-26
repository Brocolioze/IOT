import machine
import time
import urequests as requests
import _thread
import network
import os

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)
BLUE_LED_PIN = 2
BLUE_LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)
running = True

SSID = 'TECHINFOTR-IOT'
PASSWORD = 'LeSansFil0134$$'
PHP_SCRIPT_URL = 'https://172.16.86.209/insert.php'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connexion au réseau Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    
    if wlan.isconnected():
        blink_blue_led()
        return True
    return False

def blink_blue_led():
    for _ in range(3):
        BLUE_LED.on()
        time.sleep(0.5)
        BLUE_LED.off()
        time.sleep(0.5)

def check_wifi_and_send_data_thread():
    global running
    while running:
        if connect_wifi():
            envoyer_donnees_gps()
        time.sleep(10)

def lire_trames_gps():
    global running
    while running:
        try:
            if uart.any():
                trame_gps = uart.readline()
                #print("Trame GPS brute:", trame_gps)
                if trame_gps.startswith(b'$GNGLL'):
                    trame_split = trame_gps.split(b',')
                    if len(trame_split) >= 5:
                        latitude = trame_split[1]
                        longitude = trame_split[3]
                        print("Latitude:", latitude)
                        print("Longitude:", longitude)
                        with open("gps.txt", 'a') as fichier:
                            fichier.write("Latitude: {}\tLongitude: {}\n".format(latitude.decode('utf-8', 'ignore'), longitude.decode('utf-8', 'ignore')))
        except Exception as e:
            print("Erreur lors de la lecture des données GPS:", e)
        time.sleep(0.1)


def envoyer_donnees_gps():
    print("DANS ENVOYER DONNÉES GPS")
    try:
        with open("gps.txt", "r+") as fichier:
            ligne = fichier.readline()           
            latitude, longitude = ligne.strip().split('\t')
            
            # Supprimer les tabulations et espaces après le ':'
            lat = latitude.split(":")[1].strip()
            lon = longitude.split(":")[1].strip()
                    
            send_gps_to_server(lat, lon)
        
            fichier.close()
    except Exception as e:
        print("Erreur lors de l'envoi des données GPS:", e)
            
  

def send_gps_to_server(latitude, longitude):
    print("DANS ENVOYER DONNÉES AU SERVEUR")
    try:
        data = {'latitude': latitude, 'longitude': longitude}
        response = requests.post(PHP_SCRIPT_URL, json=data)
        if response.status_code == 200:
            print('Données GPS envoyées avec succès au serveur')
            print(response.text)
        else:
            print('Échec de l\'envoi des données GPS au serveur')
            
        
    except Exception as e:
        print("Erreur lors de l'envoi des données GPS:", e)

def main():
    _thread.start_new_thread(lire_trames_gps, ())
    _thread.start_new_thread(check_wifi_and_send_data_thread, ())
    while running:
        time.sleep(1)  # Boucle principale

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Arrêt des threads...")
        running = False

