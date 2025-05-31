"""
==================================================
FILE:        <logger.py>
AUTHOR:      <Raz0rMind>
CREATED:     <31.05.2025>
VERSION:     <1.0.0>

DESCRIPTION: Speichert die CSV Datei
    
REQUIRES: obd
==================================================
"""
import csv
import time
import threading
from datetime import datetime

class OBDLogger:
    def __init__(self, connection, filename="obd_log.csv", interval=1.0):
        self.connection = connection
        self.filename = filename
        self.interval = interval  # Sekunden
        self.running = False
        self.thread = None

    def start_logging(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._log_loop, daemon=True)
        self.thread.start()

    def stop_logging(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _log_loop(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "RPM", "Geschwindigkeit (km/h)", "Kühlwassertemperatur (°C)"])

            while self.running:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                rpm = self._get_value("RPM")
                speed = self._get_value("SPEED")
                temp = self._get_value("COOLANT_TEMP")

                writer.writerow([timestamp, rpm, speed, temp])
                print(f"[LOG] {timestamp} RPM={rpm}, SPEED={speed}, TEMP={temp}")
                time.sleep(self.interval)

    def _get_value(self, command_name):
        import obd
        cmd = obd.commands.get(command_name)
        if not cmd:
            return "?"
        response = self.connection.query(cmd)
        return str(response.value) if response and response.value else "?"
