"""
==================================================
FILE:        <main.py>
AUTHOR:      <Raz0rMind>
CREATED:     <30.05.2025>
VERSION:     <1.0.0>

DESCRIPTION: 

    Die GUI kann:
        ✅ VIN-Auslese
        ✅ Fahrzeuginfo
        ✅ Start/Stop Logging Buttons
        ✅ Logging in obd_log.csv
==================================================
"""
import tkinter as tk
from obd_reader.connector import OBDConnector
from obd_reader.vin_reader import VINReader
from obd_reader.vehicle_info import VehicleInfo
from obd_reader.logger import OBDLogger

class OBDGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 OBD-II Scanner")
        self.root.geometry("400x300")

        self.connector = OBDConnector()

        self.port_label = tk.Label(root, text="Verfügbare Ports:")
        self.port_label.pack(pady=5)

        self.ports = self.connector.list_ports()
        self.port_var = tk.StringVar(value=self.ports[0] if self.ports else "")
        self.port_dropdown = tk.OptionMenu(root, self.port_var, *self.ports)
        self.port_dropdown.pack(pady=5)

        self.connect_button = tk.Button(root, text="🔌 Verbinden & VIN lesen", command=self.read_vin)
        self.connect_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Nicht verbunden", fg="red")
        self.status_label.pack(pady=5)

        self.vin_label = tk.Label(root, text="VIN: -")
        self.vin_label.pack(pady=5)

        self.vehicle_label = tk.Label(root, text="Fahrzeug: -")
        self.vehicle_label.pack(pady=5)

        """
            logger.py
        """
        
        self.logger = None

        self.start_log_button = tk.Button(root, text="▶️ Start Logging", command=self.start_logging)
        self.start_log_button.pack(pady=5)

        self.stop_log_button = tk.Button(root, text="⏹ Stop Logging", command=self.stop_logging, state="disabled")
        self.stop_log_button.pack(pady=5)

        self.log_status = tk.Label(root, text="Logger: inaktiv", fg="gray")
        self.log_status.pack(pady=5)

        def start_logging(self):
            try:
                if not self.connector or not self.connector.get_connection():
                    self.status_label.config(text="❌ Keine Verbindung!", fg="red")
                    return

                self.logger = OBDLogger(self.connector.get_connection())
                self.logger.start_logging()
                self.log_status.config(text="Logger: aktiv ✅", fg="green")
                self.start_log_button.config(state="disabled")
                self.stop_log_button.config(state="normal")
            except Exception as e:
                self.log_status.config(text=f"Logger-Fehler: {e}", fg="red")

        def stop_logging(self):
            if self.logger:
                self.logger.stop_logging()
                self.log_status.config(text="Logger: gestoppt ⏹", fg="gray")
                self.start_log_button.config(state="normal")
                self.stop_log_button.config(state="disabled")


    def read_vin(self):
        try:
            selected_port = self.port_var.get()
            self.connector = OBDConnector(preferred_port=selected_port)
            self.connector.connect()
            self.status_label.config(text="Status: Verbunden ✅", fg="green")

            vin_reader = VINReader(self.connector.get_connection())
            vin = vin_reader.get_vin()
            self.vin_label.config(text=f"VIN: {vin or 'Nicht verfügbar'}")

            if vin:
                info = VehicleInfo.from_vin(vin)
                self.vehicle_label.config(text=f"Fahrzeug: {info}")
            else:
                self.vehicle_label.config(text="Fahrzeug: Nicht erkannt")

        except Exception as e:
            self.status_label.config(text=f"Fehler: {e}", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = OBDGuiApp(root)
    root.mainloop()
