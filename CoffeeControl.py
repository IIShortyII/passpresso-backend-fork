import RPi.GPIO as GPIO
import subprocess
import time

#GPIO Start von Kaffeemaschine
gpio_pin = 17

#Timeout für Skriptlaufzeit
timeout = 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print("Await GPIO 17 HIGH Signal")

#Flankenauswertung Merker
previous_state = GPIO.input(gpio_pin)

try:
    while True:
        current_state = GPIO.input(gpio_pin)

        if current_state == GPIO.HIGH and previous_state == GPIO.LOW:
            process = subprocess.Popen(["python3", "RFID_ReaderwithGUI_QR.py"])
            print("Skript gestartet")

            time.sleep(timeout)
            process.terminate()
            print("Skript gestoppt")

        previous_state = current_state

except KeyboardInterrupt:
    # Wenn das Skript durch eine Tastenunterbrechung (CTRL+C) beendet wird
    pass

finally:
    # Aufräumen und GPIO freigeben
    GPIO.cleanup()