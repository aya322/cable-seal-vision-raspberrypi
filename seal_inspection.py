import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
LED_VERTE = 17
LED_ROUGE = 27
GPIO.setup(LED_VERTE, GPIO.OUT)
GPIO.setup(LED_ROUGE, GPIO.OUT)

# Couleur de reference du joint (espace HSV - couleur bleue)
couleur_min = np.array([100, 80, 50])
couleur_max = np.array([130, 255, 255])

# Initialisation de la camera
camera = cv2.VideoCapture(0)

while True:
    # Etape 1 : capturer une image
    ret, image = camera.read()

    # Etape 2 : reduire le bruit avec un filtre gaussien
    image_floue = cv2.GaussianBlur(image, (5, 5), 0)

    # Etape 3 : convertir en HSV
    image_hsv = cv2.cvtColor(image_floue, cv2.COLOR_BGR2HSV)

    # Etape 4 : isoler la couleur du joint
    masque = cv2.inRange(image_hsv, couleur_min, couleur_max)
    pixels = cv2.countNonZero(masque)

    # Etape 5 : analyser la forme du joint
    contours, _ = cv2.findContours(masque,
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    resultat = 'NOK'

    if len(contours) > 0 and pixels > 500:
        c = max(contours, key=cv2.contourArea)
        aire = cv2.contourArea(c)
        perimetre = cv2.arcLength(c, True)
        circularite = (4 * 3.14 * aire) / (perimetre ** 2)

        # Etape 6 : decision
        if aire > 3000 and circularite > 0.80:
            resultat = 'OK'

    # Etape 7 : allumer la bonne LED
    if resultat == 'OK':
        GPIO.output(LED_VERTE, GPIO.HIGH)
        GPIO.output(LED_ROUGE, GPIO.LOW)
    else:
        GPIO.output(LED_VERTE, GPIO.LOW)
        GPIO.output(LED_ROUGE, GPIO.HIGH)

    # Afficher le resultat sur l'ecran
    cv2.putText(image, resultat, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if resultat == 'OK' else (0, 0, 255), 2)
    cv2.imshow('Controle Joint', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
GPIO.cleanup()
