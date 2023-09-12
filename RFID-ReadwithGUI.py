import time
import requests
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import tkinter as tk
from tkinter import ttk  # Für den Fortschrittsbalken
import threading

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

# Funktion zum Aktualisieren der GUI-Anzeige
def update_gui(score, service_url, username, error_message=None):
    if error_message:
        error_label.config(text=error_message)
        error_label.grid(row=0, column=0, columnspan=2)  # Zeige Fehlermeldung
        score_label.grid_forget()
        service_url_label.grid_forget()
        username_label.grid_forget()
        progress.grid_forget()
        if progress['value'] == 0:
            no_card_label.grid(row=0, column=0, columnspan=2)  # Zeige "Mitarbeiter Karte vorhalten"
    else:
        error_label.grid_forget()
        score_label.config(text=f"Score: {score}")
        service_url_label.config(text=f"Service URL: {service_url}")
        username_label.config(text=f"Username: {username}")
        score_label.grid(row=1, column=0, columnspan=2)
        service_url_label.grid(row=2, column=0, columnspan=2)
        username_label.grid(row=3, column=0, columnspan=2)
        progress.grid(row=4, column=0, columnspan=2)
        no_card_label.grid_forget()  # Blende "Mitarbeiter Karte vorhalten" aus

# Funktion zum Anzeigen der Meldung "Mitarbeiter Karte vorzeigen"
def show_no_card_message():
    no_card_label.grid(row=0, column=0, columnspan=2)
    error_label.grid_forget()
    score_label.grid_forget()
    service_url_label.grid_forget()
    username_label.grid_forget()
    progress.grid_forget()

# Funktion zum Aktualisieren des Fortschrittsbalkens
def update_progress():
    current_value = progress['value']
    if current_value > 0:
        progress['value'] = current_value - 10  # Reduziere den Fortschrittsbalken um 10
        root.after(1000, update_progress)  # Aktualisiere den Fortschrittsbalken alle 1 Sekunde
    else:
        show_no_card_message()  # Blende "Mitarbeiter Karte vorhalten" nach Ablauf des Fortschrittsbalkens aus

# Funktion zum Aktualisieren der Anzeige
def update_score():
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        
        if uid is None:
            continue
        
        uid_string = uid_to_string(uid)
        
        # Timeout für selben User (10sec.)
        current_time = time.time()
        
        if "last_read_time" not in globals():
            global last_read_time
            last_read_time = current_time
        
        if current_time - last_read_time >= 10:
            last_read_time = current_time
            
            if uid_string in uid_to_username:
                username = uid_to_username[uid_string]
                print("Found RFID card for user:", username," - ",uid_string)
                
                # Sende die UID an den Server
                url = f"http://localhost:3000/api/user/{uid_string}/password"
                response = requests.get(url)

                if response.status_code == 200:
                    print("Server response:", response.text)
                    #Erhaltene Daten speichern
                    data = response.json().get("data", {})
                    score = data.get("score", 0)
                    service_url = data.get("password", {}).get("serviceUrl", "")
                    username = data.get("password", {}).get("username", "")
                    update_gui(score, service_url, username)  # Aktualisiere die GUI ohne Fehlermeldung
                    progress['value'] = 100  # Setze den Fortschrittsbalken auf 100
                    progress.grid(row=4, column=0, columnspan=2)  # Zeige den Fortschrittsbalken
                    update_progress()  # Starte den Fortschrittsbalken-Abbau
                else:
                    print("Error sending request to server")
                    update_gui(0, "", "", "Fehler beim Senden der Anfrage an den Server")  # Zeige Fehlermeldung
                    progress['value'] = 100  # Setze den Fortschrittsbalken auf 0
                    progress.grid(row=4, column=0, columnspan=2)  # Zeige den Fortschrittsbalken
                    update_progress()  # Starte den Fortschrittsbalken-Abbau
            else:
                print("Unbekannter Mitarbeiter, bitte melden Sie sich beim Kaffeebeauftragten.")
                update_gui(0, "", "", "Unbekannter Mitarbeiter, bitte melden Sie sich beim Kaffeebeauftragten")  # Zeige Fehlermeldung
                progress['value'] = 100 # Setze den Fortschrittsbalken auf 0
                progress.grid(row=4, column=0, columnspan=2)  # Zeige den Fortschrittsbalken
                update_progress()  # Starte den Fortschrittsbalken-Abbau

# Erstelle ein Tkinter-Fenster
root = tk.Tk()
root.title("Passpresso Secure")

# Setze die Größe der GUI auf 800x400
root.geometry("800x400")

# Erstelle ein Frame, um die GUI-Inhalte zu zentrieren
center_frame = tk.Frame(root)
center_frame.pack(expand=True)  # Zentriere horizontal und vertikal

# Erstelle ein Label für "Mitarbeiter Karte vorhalten"
no_card_label = tk.Label(center_frame, text="Mitarbeiter Karte vorhalten", font=("Helvetica", 14))
no_card_label.grid(row=0, column=0, columnspan=2)  # Zentriere horizontal und vertikal

# Erstelle Labels zur Anzeige des Scores und anderer Informationen
score_label = tk.Label(center_frame, text="Score: 0")
service_url_label = tk.Label(center_frame, text="Service URL: ")
username_label = tk.Label(center_frame, text="Username: ")

# Erstelle einen Fortschrittsbalken
progress = ttk.Progressbar(center_frame, length=200, mode='determinate')

# Erstelle ein Label für Fehlermeldungen
error_label = tk.Label(center_frame, text="", fg="red")

# Starte den Thread zur Aktualisierung des RFID-Readers
rfid_thread = threading.Thread(target=update_score)
rfid_thread.daemon = True
rfid_thread.start()

# Starte die Tkinter-Hauptschleife
root.mainloop()
