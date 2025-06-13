import os
import pathlib

import dotenv
from loguru import logger

dotenv.load_dotenv()

DEBUG = True


def env_path(name="root"):
    path_main = pathlib.Path(__file__).parent.parent.resolve()
    path_logs = pathlib.Path(f"{path_main}/logs").resolve()
    ans = {
        "root": path_main,
        "log": path_logs,
    }

    return ans[name]


def env_debug(name="debug"):
    debug = os.environ.get("DEBUG", False)
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    ans = {
        "debug": debug,
        "log_level": log_level,
    }

    return ans[name]


def env_login():

    """
    Returns the username and password for authentication.
    """
    logger.info("Loading environment variables for login...")
    username = os.environ.get("NVIRO_USERNAME")
    password = os.environ.get("NVIRO_PASSWORD")
    login_given = username is not None and password is not None
    if login_given:
        return username, password
    else:
        logger.info("Username and password environment variables not set")
        return None, None
    


def env_endpoints(name="jwt"):
    JWT_ENDPOINT = "https://ant.nvirosense.com/api/v1/login"
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"

    ans = {
        "jwt": JWT_ENDPOINT,
        "devices": DEVICES_ENDPOINT,
    }

    return ans[name]


def env_global():
    """
    Returns global settings for the application.
    """
    # Example global settings, can be extended as needed
    ans = {
        "start_date": "2025-05-01 00:00:00",
    }

    return ans


def testing():
    path = env_path("logs")
    print(f"path: {path}")
