#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    name = input('Entrez un nom : ')
    picture = input('Entrez une photo : ')
    birth = input('Entrez l\'année de naissance : ')
    research = input('Voulez-vous effectuer une recherche ? (y or n) : ')

    # Concaténer les données avec des séparateurs
    data_to_write = f"{name}:{picture}:{birth}:{research}"

    print("Approchez votre tag pour écrire")

    time.sleep(2)  # Attendre 2 secondes avant d'écrire

    reader.write(data_to_write)

    print("Écriture réussie")

finally:
    GPIO.cleanup()

