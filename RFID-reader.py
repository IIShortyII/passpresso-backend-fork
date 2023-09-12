import time
import requests
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

# I2C-Initialisierung
i2c = busio.I2C(board.SCL, board.SDA)

# PN532-Initialisierung
reset_pin = DigitalInOut(board.D6)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin)
ic, ver, rev, support = pn532.firmware_version

print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Konfiguration des PN532 nach Bedarf
pn532.SAM_configuration()

uid_to_username = {
    "CBCB3C50": "UID-1 Dennis",
    "A4A29E5B": "UID-2 Felix",
    "CB868650": "UID-3 Raffael",
    "8BFF4F50": "UID-4 Jonas",
    "742B695B": "UID-5 Sebastian",
}

last_uid = None
last_read_time = 0

def uid_to_string(uid):
    return ''.join([format(byte, '02X') for byte in uid])

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    
    if uid is None:
        continue
    
    uid_string = uid_to_string(uid)
    
    # Timeout für selben User (10sec.)
    current_time = time.time()
    if uid_string != last_uid or current_time - last_read_time >= 10:
        last_uid = uid_string
        last_read_time = current_time
        
        if uid_string in uid_to_username:
            username = uid_to_username[uid_string]
            print("Found RFID card for user:", username," - ",uid_string)
            
            # Sende die UID an den Server
            url = f"http://localhost:3000/api/user/{uid_string}/password"
            response = requests.get(url)
            
            if response.status_code == 200:
                print("Server response:", response.text)
            else:
                print("Error sending request to server")
        else:
            print("Unbekannter Mitarbeiter, bitte melden Sie sich beim Kaffeebeauftragten.")