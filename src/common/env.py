import os
import pathlib

import dotenv

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
    username = os.environ.get("NVIRO_USERNAME")
    password = os.environ.get("NVIRO_PASSWORD")
    # ans = {
    #     "username": username,
    #     "password": password,
    # }

    return username, password


def testing():
    path = env_path("logs")
    print(f"path: {path}")
