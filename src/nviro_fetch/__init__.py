# from nviro_fetch import auth, fetch, data  # noqa: F403
from .auth import authenticate  # noqa: F401
from .fetch import fetch_devices, fetch_device_sensors  # noqa: F401
from .data import get_nviro_data  # noqa: F401


def hello() -> str:
    return "Hello from nviro-fetch!"
