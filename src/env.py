import os
import pathlib

import dotenv

dotenv.load_dotenv()


def env_common(name="root"):
    path_main = pathlib.Path(__file__).parent.parent.resolve()
    path_logs = pathlib.Path(f"{path_main}/logs").resolve()
    ans = {
        "root": path_main,
        "log": path_logs,
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
    path = env_common("logs")
    print(f"path: {path}")
