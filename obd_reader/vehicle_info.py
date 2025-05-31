"""
==================================================
FILE:        <vehicle_info.py>
AUTHOR:      <Raz0rMind>
CREATED:     <31.05.2025>
VERSION:     <1.0.0>

DESCRIPTION: n.A
==================================================
"""
# obd_reader/vehicle_info.py
import requests
import json
import os

class VehicleInfo:
    @staticmethod
    def from_vin(vin: str, use_api=True) -> str:
        if not vin or len(vin) < 10:
            return "❌ Ungültige VIN"

        vin = vin.strip().upper()

        # 1. Lokale WMI-Zuordnung
        manufacturer = VehicleInfo.lookup_manufacturer(vin[:3])
        year = VehicleInfo.estimate_year(vin[9])
        result = f"{manufacturer} (ca. Baujahr {year})"

        # 2. Optional: NHTSA API für Details
        if use_api:
            api_data = VehicleInfo.query_nhtsa_api(vin)
            if api_data:
                make = api_data.get("Make", manufacturer)
                model = api_data.get("Model", "")
                year_api = api_data.get("ModelYear", year)
                result = f"{make} {model} ({year_api})"

        return result

    @staticmethod
    def lookup_manufacturer(wmi: str) -> str:
        try:
            path = os.path.join(os.path.dirname(__file__), "wmi_codes.json")
            with open(path, "r") as f:
                data = json.load(f)
            return data.get(wmi.upper(), "Unbekannter Hersteller")
        except Exception:
            return "Unbekannt"

    @staticmethod
    def estimate_year(code: str) -> str:
        year_map = {
            "S": "1995", "T": "1996", "V": "1997", "W": "1998", "X": "1999",
            "Y": "2000", "1": "2001", "2": "2002", "3": "2003", "4": "2004",
            "5": "2005", "6": "2006", "7": "2007", "8": "2008", "9": "2009",
            "A": "2010", "B": "2011", "C": "2012", "D": "2013", "E": "2014",
            "F": "2015", "G": "2016", "H": "2017", "J": "2018", "K": "2019",
            "L": "2020", "M": "2021", "N": "2022", "P": "2023", "R": "2024", "S": "2025"
        }
        return year_map.get(code.upper(), "?")

    @staticmethod
    def query_nhtsa_api(vin: str) -> dict:
        try:
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
            response = requests.get(url, timeout=5)
            data = response.json()

            results = {item["Variable"]: item["Value"] for item in data.get("Results", []) if item["Value"]}
            return {
                "Make": results.get("Make"),
                "Model": results.get("Model"),
                "ModelYear": results.get("Model Year"),
                "VehicleType": results.get("Vehicle Type")
            }
        except Exception as e:
            print(f"[VIN-API Fehler]: {e}")
            return {}
