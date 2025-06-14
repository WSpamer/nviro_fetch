from nviro_fetch.fetch import fetch_device_sensors, fetch_devices
import pandas as pd


def get_sensors(token, devices: list):
    sensor_list = []
    for device in devices:
        sensors = fetch_device_sensors(token, device)
        for sensor in sensors:
            params = {
                "device_id": device["id"],
                "name": sensor["sensor_name"],
                "unit": sensor["unit"],
            }
            sensor_list.append(params)
    return sensor_list


def add_id(df):
    df.insert(0, "id", range(1, 1 + len(df)))
    return df


def list_to_df(lst):
    return add_id(pd.DataFrame(lst))


def get_nviro_data(token):
    devices = fetch_devices(token, is_print=False)
    device_list = []
    group_list = []
    for device in devices:
        group_params = {
            "name": device["device_group"],
            "description": device["device_group"],
            "department": device["department"],
        }
        device_params = {
            "name": device["device_name"],
            "devEui": device["devEui"],
            "group": device["device_group"],
        }

        device_list.append(device_params)
        if group_params not in group_list:
            group_list.append(group_params)
    df_devices = list_to_df(device_list)
    df_groups = list_to_df(group_list)
    sensor_list = get_sensors(token, df_devices.to_dict("records"))
    df_sensors = list_to_df(sensor_list)

    data = [
        {
            "name": "Devices",
            "data": df_devices,
        },
        {
            "name": "Groups",
            "data": df_groups,
        },
        {
            "name": "Sensors",
            "data": df_sensors,
        },
    ]

    return data


def extract_readings(readings):
    sensor_list = []
    for reading in readings:
        datetime = reading["received_at"]
        devEui = reading["devEui"]
        data = reading["sensor_data"]
        for sensor in data:
            params = {
                "sensor_name": sensor["sensor_name"],
                "unit": sensor["unit"],
                "value": sensor["value"],
                "datetime": datetime,
                "devEui": devEui,
            }
            sensor_list.append(params)
    return sensor_list


def get_sensor_readings(readings):
    readings = extract_readings(readings)
    sensors = [reading["sensor_name"] for reading in readings]
    sensors = list(set(sensors))

    sensor_readings = []
    for sensor in sensors:
        sensor_reading = [
            reading for reading in readings if reading["sensor_name"] == sensor
        ]
        # print(sensor_reading)

        params = {
            "sensor_name": sensor,
            "readings": sensor_reading,
        }
        sensor_readings.append(params)

    return sensor_readings


def correct_reading(reading):
    datetime = reading["received_at"]
    devEui = reading["devEui"]
    data = reading["sensor_data"]
    sensor_readings = []
    for sensor in data:
        sensor["datetime"] = datetime
        sensor["devEui"] = devEui
        # print("Sensor")
        # print(len(sensor))
        # sensor_readings.append(sensor)

    return data
