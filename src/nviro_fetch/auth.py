import json
import sys
import time

import dotenv
import requests
from loguru import logger

from nviro_fetch.common.env import env_debug, env_endpoints, env_login
from nviro_fetch.common.log import config_logfile

__all__ = ["authenticate"]
dotenv.load_dotenv()


# Logging function (minimal logging)
def log_response(response, action):
    print("----------------------")
    print(f"[LOG] {action} Response: Status {response.status_code}")
    print("----------------------")


def parse_json(response_body):
    try:
        return json.loads(response_body)
    except json.JSONDecodeError:
        print("[ERROR] Response is not valid JSON!")
        sys.exit(1)


def valid_token(devices):
    bad_response = {"login": "", "password": None}  # noqa: F821
    valid = devices == bad_response
    if valid:
        logger.error(f"Token is expired or invalid! Status: {valid}")
        return False
    return True


def fetch_login(username=None, password=None):
    JWT_ENDPOINT = env_endpoints("jwt")

    # Check if username and password are provided
    logger.info("Checking if username and password are provided...")
    login_given = username is not None and password is not None

    # If username and password are not provided, fetch from environment variables
    if not login_given:
        logger.info("Fetching username and password from environment variables...")
        username, password = env_login()
        if not username or not password:
            logger.error("Username or password is not set in environment variables!")
            raise ValueError(
                "Username or password is not set in environment variables!"
            )

    logger.info(f"Authenticating with {JWT_ENDPOINT}...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "user": {
            "login": username,
            "password": password,
        }
    }
    response = requests.post(JWT_ENDPOINT, json=payload, headers=headers)

    return response


def authenticate(username=None, password=None):

    retries = 0
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    while True:
        try:
            response = fetch_login(username=username, password=password)
            if response.status_code == 200:
                json_response = parse_json(response.text)

                jwt_token = json_response.get("token")
                logger.info(json_response)
                if not jwt_token:
                    auth_header = response.headers.get("Authorization")
                    if auth_header:
                        parts = auth_header.split(" ")
                        if len(parts) >= 2:
                            jwt_token = parts[-1]
                            logger.info(f"Token: {jwt_token}")
                if jwt_token:
                    logger.success("Authentication successful! Token received.")
                    return jwt_token
                else:
                    logger.error("Failed to extract token from response!")
                    sys.exit(1)
            else:
                logger.error("Authentication failed! Retrying...")
                raise Exception(f"Auth failed with status {response.status_code}")
        except Exception as e:
            retries += 1
            logger.warning(f"Attempt {retries}/{MAX_RETRIES} failed: {e}")
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                logger.critical(f"Authentication failed after {MAX_RETRIES} attempts.")
                sys.exit(1)


if __name__ == "__main__":
    # Configure logger
    log_level = env_debug("log_level")

    # logger.add(sys.stderr, level=log_level)  # Add stderr logger for debug output
    # Add file logger for authentication logs
    config_logfile("auth.log")
    logger.info("Starting authentication process...")
    jwt_token = authenticate()
    logger.info(f"JWT Token: {jwt_token}")
