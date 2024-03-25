import machine
import time
import urequests as requests
import _thread

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)
BLUE_LED_PIN = 2
BLUE_LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)
# Variable globale pour indiquer si les threads doivent continuer à s'exécuter
running = True

def read_gps_data_thread():
    global running
    while running:
        try:
            if uart.any():
                gps_line = uart.readline()
                print("Ligne GPS brute:", gps_line)
                # Vous pouvez ajouter le traitement supplémentaire des données GPS ici si nécessaire
        except Exception as e:
            print("Erreur lors de la lecture des données GPS:", e)
        time.sleep(0.1)

def write_to_txt_file_thread():
    global running
    while running:
        try:
            with open("gps.txt", 'a') as file:  # Mode 'a' pour ajouter à la fin du fichier
                if uart.any():
                    gps_line = uart.readline()
                    print("Ligne GPS brute:", gps_line)
                    file.write(gps_line.decode('utf-8', 'ignore'))
                    print("Données GPS écrites dans 'gps.txt' avec succès.")
        except Exception as e:
            print("Erreur lors de l'écriture dans le fichier:", e)
        time.sleep(0.1)

def blink_blue_led():
    for _ in range(3):
        BLUE_LED.on()
        time.sleep(0.5)
        BLUE_LED.off()
        time.sleep(0.5)

def main():
    _thread.start_new_thread(read_gps_data_thread, ())
    _thread.start_new_thread(write_to_txt_file_thread, ())
    blink_blue_led()
    # Exécuter pendant au moins 30 secondes
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

