import json

import requests
from loguru import logger

from nviro_fetch.auth import log_response, parse_json, valid_token


def controller_link(devEui):
    if not devEui:
        logger.error("Device does not have a valid devEui!")
        return []
    link_base = f"https://ant.nvirosense.com/api/v1/nss500/devices/{devEui}"
    return link_base


def controller_latch_body(relay="ro1"):
    if relay == "ro1":
        ro1 = "ON"
        ro2 = "no_action"
        logger.info("Setting relay ro1 to ON")
    elif relay == "ro2":
        ro1 = "no_action"
        ro2 = "ON"
        logger.info("Setting relay ro2 to ON")
    else:
        logger.error(f"Invalid relay option: {relay}. Must be 'ro1' or 'ro2'.")
        raise ValueError("Invalid relay option. Must be 'ro1' or 'ro2'.")
        # return []
    body = {"ro1_state": ro1, "ro2_state": ro2}
    return body


def controller_toggle_endpoint(link_base, relay="ro1"):

    if relay == "ro1":
        endpoint = f"{link_base}/toggle_ro1"
        logger.info("Setting relay ro1 to ON")
        return endpoint
    elif relay == "ro2":
        endpoint = f"{link_base}/toggle_ro2"
        logger.info("Setting relay ro2 to ON")
        return endpoint
    else:
        logger.error(f"Invalid relay option: {relay}. Must be 'ro1' or 'ro2'.")
        raise ValueError("Invalid relay option. Must be 'ro1' or 'ro2'.")


def controller_endpoint(link_base, relay="ro1", signal_type="toggle"):

    if signal_type == "toggle":
        endpoint = controller_toggle_endpoint(link_base, relay=relay)
        return endpoint
    elif relay == "latch":
        endpoint = f"{link_base}/relay_control"
        logger.info("Setting relay ro2 to ON")
        return endpoint
    else:
        logger.error(f"Invalid relay option: {relay}. Must be 'ro1' or 'ro2'.")
        raise ValueError("Invalid relay option. Must be 'ro1' or 'ro2'.")


# TODO: Adapt this to turn on/off relays for the controller
# relay options: r01 | ro2
# Type options: toggle | latch
def post_controller(
    jwt_token, devEui, signal_type="toggle", relay="ro1", is_print=False
):
    # devEui = device["devEui"]
    link_base = controller_link(devEui)
    endpoint = controller_endpoint(link_base, relay=relay, signal_type=signal_type)
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    logger.info(f"Activating controller {devEui}...")
    body = controller_latch_body(relay=relay) if signal_type == "toggle" else {}
    logger.info(f"body {body}")
    response = requests.post(endpoint, headers=headers, json=body)
    logger.info(f"Posting: Status {response.status_code}")
    if response.status_code == 202:
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
