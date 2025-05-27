import os
import sys

from loguru import logger

from nviro_fetch.common.env import env_debug, env_path


def config_log_level(log_level="") -> str:
    logger.remove()  # Remove default logger
    if not log_level:
        log_level = env_debug("log_level")
    return log_level

    # logger.add(sys.stderr, level=log_level)  # Add stderr logger for debug output


def config_logger(log_level: str = "") -> None:
    log_level = config_log_level(log_level)
    logger.add(
        sys.stderr,
        level=log_level,
    )


def config_logfile(filename: str = "nviro_fetch.log") -> None:
    log_path = env_path("log")
    v = os.environ.get("PWD")
    print(v)
    # print(f"Log path: {log_path}")
    # logger.add(
    #     f"{log_path}/{filename}",
    #     rotation="1 MB",
    #     retention="7 days",
    #     level=config_log_level(),
    # )
