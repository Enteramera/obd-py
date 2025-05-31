"""
==================================================
FILE:        <connector.py>
AUTHOR:      <Raz0rMind>
CREATED:     <30.05.2025>
VERSION:     <1.0.0>

DESCRIPTION: 
    Automatischer Port-Scan
    Optional: Manuelle Portwahl
    Extra Methode list_ports()
    OOP-Struktur
    Logging & Fehlerbehandlung
==================================================
"""
import obd

class OBDConnector:
    def __init__(self, preferred_port=None):
        """
            Initialisiert den Connector.
            :param preferred_port: Optionaler Port, falls bekannt (z. B. 'COM3' oder '/dev/ttyUSB0')
        """
        self.connection = None
        self.preferred_port = preferred_port

    @staticmethod
    def list_ports():
        """
            Gibt alle verfügbaren Ports zurück.
        """
        return obd.scan_serial()

    def connect(self):
        """
            Baut eine Verbindung zum OBD-II Adapter auf.
            Wenn ein bevorzugter Port gesetzt ist, wird dieser zuerst versucht.
            Andernfalls werden alle verfügbaren Ports der Reihe nach getestet.
        """
        ports_to_try = []

        if self.preferred_port:
            ports_to_try.append(self.preferred_port)

        ports_to_try.extend([p for p in self.list_ports() if p != self.preferred_port])

        if not ports_to_try:
            raise ConnectionError("❌ Kein OBD-II Gerät gefunden.")

        print(f"[INFO] Ports werden getestet: {ports_to_try}")

        for port in ports_to_try:
            print(f"[INFO] Versuche Verbindung über {port} ...")
            try:
                connection = obd.OBD(port)
                if connection.is_connected():
                    self.connection = connection
                    print(f"[SUCCESS] Verbunden mit {port}")
                    return
                else:
                    print(f"[WARNUNG] {port} gefunden, aber keine Verbindung möglich.")
            except Exception as e:
                print(f"[FEHLER] Fehler bei Verbindung mit {port}: {e}")

        raise ConnectionError("❌ Verbindung zu keinem Port erfolgreich.")

    def get_connection(self):
        """
            Gibt die bestehende Verbindung zurück, falls vorhanden.
        """
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError("Keine gültige OBD-Verbindung aktiv.")
        return self.connection