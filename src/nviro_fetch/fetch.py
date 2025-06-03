import json

import requests
from loguru import logger

from nviro_fetch.auth import log_response, parse_json, valid_token
from nviro_fetch.common.env import env_endpoints


def log_failed(name, response):
    logger.error(f"[ERROR] Failed to fetch {name}! Status: {response.status_code}")
    logger.debug("Fetching failed! Returning empty list.")


def fetch_nviro(jwt_token, endpoint, is_print=False):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    logger.info(f"Fetching data from {endpoint}...")
    response = requests.get(endpoint, headers=headers)
    logger.info(f"Fetching: Status {response.status_code}")
    if response.status_code == 200:
        data = parse_json(response.text)
        valid = valid_token(data)
        if not valid:
            logger.debug("Invalid token! Returning empty list.")
            return []
        logger.success("Data fetched successfully!")
        if is_print:
            print("[Data] \n -------------------")
            print(json.dumps(data, indent=4))
        return data
    else:
        logger.error(f"Failed to fetch devices! Status: {response.status_code}")
        logger.debug("Fetching failed! Returning empty list.")
        return []


# Function to fetch devices using JWT token
def fetch_devices(jwt_token, is_print=False):
    DEVICES_ENDPOINT = env_endpoints("devices")
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    logger.info(f"Fetching devices from {DEVICES_ENDPOINT}...")
    response = requests.get(DEVICES_ENDPOINT, headers=headers)
    logger.info(f"Fetching: Status {response.status_code}")
    if response.status_code == 200:
        devices = parse_json(response.text)
        valid = valid_token(devices)
        if not valid:
            logger.debug("Invalid token! Returning empty list.")
            return []
        logger.success("Devices fetched successfully!")
        if is_print:
            print("[Data] \n -------------------")
            print(json.dumps(devices, indent=4))
        return devices
    else:
        logger.error(f"Failed to fetch devices! Status: {response.status_code}")
        logger.debug("Fetching failed! Returning empty list.")
        return []


def fetch_device_sensors(jwt_token, devEui, is_print=False):
    DEVICES_ENDPOINT = env_endpoints("devices")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    url_endpoint = f"{DEVICES_ENDPOINT}/{devEui}/sensors"
    logger.info(f"Fetching devices from {url_endpoint}...")
    response = requests.get(url_endpoint, headers=headers)
    if is_print:
        log_response(response, "Fetch Device Sensors")
    if response.status_code == 200:
        device_sensors = parse_json(response.text)
        valid = valid_token(device_sensors)
        if not valid:
            logger.debug("Invalid token! Returning empty list.")
            return []
        logger.success("Device Sensors fetched successfully!")
        if is_print:
            print("[Data] \n -------------------")
            print(json.dumps(device_sensors, indent=4))
        return device_sensors["sensors"]
    else:
        logger.error(f"Failed to fetch device sensors! Status: {response.status_code}")
        logger.debug("Fetching failed! Returning empty list.")
        return []


def fetch_sensor_readings(
    jwt_token, devEui, start_date, end_date, limit=1000000000000, page=1, is_print=False
):
    DEVICES_ENDPOINT = env_endpoints("devices")
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
    logger.info(
        f"Fetching sensor readings from {sensor_readings_endpoint} with params {params}..."
    )
    response = requests.get(sensor_readings_endpoint, headers=headers, params=params)
    if is_print:
        log_response(response, "Sensor Readings Fetch")
    if response.status_code == 200:
        readings_data = parse_json(response.text)
        valid = valid_token(readings_data)
        if not valid:
            logger.debug("Invalid token! Returning empty list.")
            return []
        logger.success("Sensor readings fetched successfully!")
        if is_print:
            print("[Data] \n -------------------")
            print(json.dumps(readings_data, indent=4))
        readings = readings_data["sensor_readings"]

        for reading in readings:
            reading["devEui"] = devEui
        return readings
        # return readings_data
    else:
        logger.error(f"Failed to fetch sensor readings! Status: {response.status_code}")
        logger.debug("Fetching failed! Returning empty list.")
        return []
