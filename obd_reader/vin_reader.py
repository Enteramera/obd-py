"""
==================================================
FILE:        <vin_reader.py>
AUTHOR:      <Raz0rMind>
CREATED:     <30.05.2025>
VERSION:     <1.0.0>

DESCRIPTION: n. A
REQUIRES: obd
==================================================
"""
import obd

class VINReader:
    def __init__(self, connection):
        self.connection = connection

    def get_vin(self):
        """
        Fragt die Fahrzeug-Identifikationsnummer (VIN) ab.
        """
        cmd = obd.commands.VIN  # OBD-II Mode 9 PID 02
        response = self.connection.query(cmd)
        if response.is_null():
            return None
        return response.value