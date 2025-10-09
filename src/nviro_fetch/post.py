import json
from datetime import datetime

import requests
from loguru import logger

from nviro_fetch.auth import log_response, parse_json, valid_token

# region Support functions ...

def controller_link(devEui: str) -> str:
    if not devEui:
        logger.error("Device does not have a valid devEui!")
        return ""
    link_base = f"https://ant.nvirosense.com/api/v1/nss500/devices/{devEui}"
    return link_base


def controller_latch_body(relay: str = "ro1"):
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


def controller_toggle_endpoint(link_base: str, relay: str = "ro1") -> str:

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


def controller_endpoint(
    devEui: str, relay: str = "ro1", signal_type: str = "toggle"
) -> str:
    link_base = controller_link(devEui)
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
# endregion


# msg=""
#     link_base = controller_link(devEui)
#     endpoint = controller_endpoint(link_base, relay=relay, signal_type=signal_type)
#     headers = {
#         "Authorization": f"Bearer {jwt_token}",
#         "Content-Type": "application/json",
#     }
#     logger.info(f"Activating controller {devEui}...")
#     body = controller_latch_body(relay=relay) if signal_type == "toggle" else {}
#     logger.info(f"body {body}")

# region Main functions ...


# TODO: Adapt this to turn on/off relays for the controller
# relay options: r01 | ro2
# Type options: toggle | latch
def post_controller(
    
    jwt_token: str,
    devEui: str,
    signal_type: str = "toggle",
    relay: str = "ro1",
    safety_on: bool = True,
    is_print: bool = False,
) -> dict:
    """
    post_controller - Posts a request to the controller to toggle or latch a relay.
    This function sends a POST request to a controller device to either toggle or latch a specified relay.
    It handles authentication via JWT token, constructs the appropriate endpoint and request body,
    and processes the response to determine success or failure. Safety checks can be enabled to prevent
    accidental posting.

    Args:
        jwt_token (str): JWT authentication token for the controller API.
        devEui (str): Device EUI (unique identifier) of the controller.
        signal_type (str, optional): Type of signal to send to the relay ("toggle" or other). Defaults to "toggle".
        relay (str, optional): Relay identifier to control (e.g., "ro1"). Defaults to "ro1".
        safety_on (bool, optional): If True, disables posting for safety. Defaults to True.
        is_print (bool, optional): If True, prints the fetched data to stdout. Defaults to False.

    Returns:
        dict: A dictionary containing:
            - "msg" (str): Status or error message.
            - "data" (dict): Data returned from the controller, if any.
            - "status" (str): "success" or "error" indicating the result of the operation.
    """
    # devEui = device["devEui"]
    # Response Details
    msg=""
    endpoint = controller_endpoint(devEui, relay=relay, signal_type=signal_type)
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    logger.info(f"Activating controller {devEui}...")
    body = controller_latch_body(relay=relay) if signal_type == "toggle" else {}
    logger.info(f"body {body}")

    if safety_on:
        msg = "Posting disabled: Please set safety_on to False to enable posting."
        ans = {"msg": msg, "data": {}, "status": "success"}
        print(msg)
        return ans

    response = requests.post(endpoint, headers=headers, json=body)
    activation_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Posting: Status {response.status_code}")
    if response.status_code == 202:
        data = parse_json(response.text)
        valid = valid_token(data)

        if not valid:
            msg = "Invalid token! Returning empty list."
            logger.debug(msg)
            ans = {"msg": msg, "data": {}, "status": "error"}
            return ans
        msg = "Data fetched successfully!"
        logger.success(msg)
        if is_print:
            print("[Data] \n -------------------")
            print(json.dumps(data, indent=4))

        ans = {
            "msg": msg, 
            "data": data,
            "status": "success",
            "activation_timestamp": activation_timestamp,
        }
        return ans
    else:
        msg = f"Failed to fetch devices! Status: {response.status_code}"
        logger.error(msg)
        logger.debug("Fetching failed! Returning empty list.")
        ans = {"msg": msg, "data": {}, "status": "success"}
        return ans

# endregion
