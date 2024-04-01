#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    print("Approchez votre tag pour lire")

    time.sleep(2)  # Attendre 2 secondes avant de lire

    id, data_read = reader.read()  # Extraire l'ID et les données textuelles

    print("Lecture réussie")

    # Diviser les données en fonction des séparateurs
    name, picture, birth, research = data_read.split(':')

    # Afficher les données lues
    print("Nom:", name.strip())  # Utiliser strip() pour enlever les espaces blancs éventuels
    print("Photo:", picture.strip())
    print("Année de naissance:", birth.strip())
    print("Recherche:", research.strip())

finally:
    GPIO.cleanup()

