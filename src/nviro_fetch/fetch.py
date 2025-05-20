import requests
import json
from nviro_fetch.auth import log_response, parse_json


# Function to fetch devices using JWT token
def fetch_devices(jwt_token, is_print=False):
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    if is_print:
        print(f"[INFO] Fetching devices from {DEVICES_ENDPOINT}...")
    response = requests.get(DEVICES_ENDPOINT, headers=headers)
    if is_print:
        log_response(response, "Fetch Devices")
    if response.status_code == 200:
        devices = parse_json(response.text)
        if is_print:
            print("[SUCCESS] Devices fetched successfully!")
        if is_print:
            print(json.dumps(devices, indent=4))
        return devices
    else:
        print(f"[ERROR] Failed to fetch devices! Status: {response.status_code}")
        return []


def fetch_device_sensors(jwt_token, devEui, is_print=False):
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    url_endpoint = f"{DEVICES_ENDPOINT}/{devEui}/sensors"
    if is_print:
        print(f"[INFO] Fetching devices from {url_endpoint}...")
    response = requests.get(url_endpoint, headers=headers)
    if is_print:
        log_response(response, "Fetch Devices")
    if response.status_code == 200:
        devices = parse_json(response.text)
        if is_print:
            print("[SUCCESS] Devices fetched successfully!")
        if is_print:
            print(json.dumps(devices, indent=4))
        return devices["sensors"]
    else:
        print(f"[ERROR] Failed to fetch devices! Status: {response.status_code}")
        return {}


def fetch_sensor_readings(
    jwt_token, devEui, start_date, end_date, limit=1000000000000, page=1, is_print=False
):
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"
    sensor_readings_endpoint = f"{DEVICES_ENDPOINT}/{devEui}/sensor_readings"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "page": page,
    }
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    if is_print:
        print(
            f"[INFO] Fetching sensor readings from {sensor_readings_endpoint} with params {params}..."
        )
    response = requests.get(sensor_readings_endpoint, headers=headers, params=params)
    if is_print:
        log_response(response, "Sensor Readings Fetch")
    if response.status_code == 200:
        readings_data = parse_json(response.text)
        if is_print:
            print("[SUCCESS] Sensor readings fetched successfully!")
            print(json.dumps(readings_data, indent=4))
        readings = readings_data["sensor_readings"]

        for reading in readings:
            reading["devEui"] = devEui
        return readings
        # return readings_data
    else:
        print(
            f"[ERROR] Failed to fetch sensor readings! Status: {response.status_code}"
        )
        return {}
