import machine
import time
import network

# Configuration des broches UART pour la communication avec le module GPS Neo-6M
uart = machine.UART(1, baudrate=9600, tx=17, rx=16)  # Modifier les broches tx et rx selon le câblage

# Informations sur le réseau Wi-Fi
SSID = 'TECHINFOTR-IOT'
PASSWORD = 'LeSansFil0134$$'

def read_gps_data():
    gps_data = []
    while True:
        if uart.any():
            line = uart.readline().decode().strip()
            if line.startswith('$GPGGA'):
                gps_data.append(line)
            elif line.startswith('$GPRMC'):
                gps_data.append(line)
        time.sleep(0.1)
        if len(gps_data) >= 2:  # Attendre de recevoir à la fois les lignes GPGGA et GPRMC
            return gps_data

def write_to_txt_file(data, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write('\n'.join(data))
            print(f"Données GPS écrites dans '{output_file}' avec succès.")
    except IOError:
        print("Erreur lors de l'écriture dans le fichier.")

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

def main():
    output_txt_file = "gps_data.txt"  # Chemin vers le fichier de sortie .txt
    
    # Lire les données GPS et les stocker dans un fichier .txt
    gps_data = read_gps_data()
    write_to_txt_file(gps_data, output_txt_file)
    
    # Connexion au Wi-Fi
    connect_wifi()
    
    # Afficher le contenu du fichier .txt
    try:
        with open(output_txt_file, 'r') as file:
            file_content = file.read()
            print("Contenu du fichier GPS:")
            print(file_content)
    except FileNotFoundError:
        print("Le fichier GPS n'a pas été trouvé.")

if __name__ == "__main__":
    main()
