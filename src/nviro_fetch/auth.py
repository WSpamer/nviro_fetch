import json
import sys
import time

import dotenv
import requests
from loguru import logger

from env import env_common, env_login

__all__ = ["authenticate"]
dotenv.load_dotenv()
path = env_common(name="log")
logger.add(f"{path}/auth.log")
# logger_auth = logger.bind(name="auth")


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


def fetch_login():
    JWT_ENDPOINT = "https://ant.nvirosense.com/api/v1/login"

    username, password = env_login()

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


def authenticate():

    retries = 0
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    while True:
        try:
            response = fetch_login()
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
