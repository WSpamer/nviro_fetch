from src.nviro_fetch.auth import authenticate
from nviro_fetch.fetch import fetch_devices, fetch_sensor_readings, fetch_device_sensors
from nviro_fetch.data import get_sensor_readings, extract_readings


def run():
    token = authenticate()
    devices = fetch_devices(token)
    SAMPLE_START_DATE = "2025-03-01T00:00:00"  # Start date in ISO8601 format
    SAMPLE_END_DATE = "2025-03-24T23:59:59"

    device = [device for device in devices if device["device_group"] == "Goedhals"][0]
    devEui = device["devEui"]
    readings_data = fetch_sensor_readings(
        token,
        devEui,
        SAMPLE_START_DATE,
        SAMPLE_END_DATE,
    )
    readings = get_sensor_readings(readings_data)
    print(readings[0])


if __name__ == "__main__":
    run()
