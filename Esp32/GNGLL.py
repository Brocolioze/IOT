import machine
import time
import urequests as requests
import _thread

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)
BLUE_LED_PIN = 2
BLUE_LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)
# Variable globale pour indiquer si les threads doivent continuer à s'exécuter
running = True

def lire_trames_gps():
    global running
    start_time = time.time()
    while running and time.time() - start_time < 600:  # Exécuter pendant 10 minutes (600 secondes)
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

def clignoter_led_bleue():
    for _ in range(3):
        BLUE_LED.on()
        time.sleep(0.5)
        BLUE_LED.off()
        time.sleep(0.5)

def main():
    _thread.start_new_thread(lire_trames_gps, ())
    clignoter_led_bleue()
    # Exécuter pendant au moins 10 minutes (600 secondes)
    time.sleep(300)
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

