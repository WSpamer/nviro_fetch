import logging

from loguru import logger

from common.log import config_logfile, config_logger


def basic_logger():
    logger = logging.getLogger(__name__)
    # Attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter(
        "%(name)s:%(asctime)s %(levelname)s: %(message)s %(funcName)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler("basic.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    return logger


def logger_advanced():
    pass


testing = {"basic": False, "loguru": True}
if testing["basic"]:
    logger1 = basic_logger()
    logger1.info("This is an info message")

if testing["loguru"]:

    logger.debug("That's it, beautiful and simple logging!")
