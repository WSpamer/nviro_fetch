from loguru import logger

# from nviro_fetch import auth, fetch, data  # noqa: F403
from .auth import authenticate  # noqa: F401
from .data import extract_readings, get_nviro_data, get_sensor_readings  # noqa: F401
from .fetch import (
    fetch_device_sensors,  # noqa: F401
    fetch_devices,  # noqa: F401
    fetch_sensor_readings,  # noqa: F401
)  # noqa: F401

logger.disable("nviro_fetch")  # Disable default logger for nviro-fetch
# logger.remove()  # Remove default logger


def hello() -> str:
    return "Hello from nviro-fetch!"
