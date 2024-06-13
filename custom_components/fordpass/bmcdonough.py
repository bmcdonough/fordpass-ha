#!/usr/bin/env python3
import logging
import logging.handlers
import os
from dotenv import load_dotenv
from pdb import set_trace as bp

from const import (
    CONF_DISTANCE_UNIT,
    CONF_PRESSURE_UNIT,
    COORDINATOR,
    DEFAULT_DISTANCE_UNIT,
    DEFAULT_PRESSURE_UNIT,
    DOMAIN,
    MANUFACTURER,
    REGION,
    UPDATE_INTERVAL,
    UPDATE_INTERVAL_DEFAULT,
    VEHICLE,
    VIN,
)
from fordpass_new import Vehicle

_LOGGER = logging.getLogger(__name__)
# verbose = True
verbose = False
debug = True
# debug = False


def config_logging():
    syslog_fmt = "%(filename)s[%(process)d] - [%(name)s] :: (%(funcName)s) : %(levelname)s - %(message)s"
    syslog_handler = logging.handlers.SysLogHandler(address="/dev/log", facility="user")
    syslog_handler.setFormatter(logging.Formatter(syslog_fmt))
    _LOGGER.addHandler(syslog_handler)
    if verbose:
        _LOGGER.setLevel(logging.INFO)
        _LOGGER.info(
            "Effective logging level is {}".format(
                logging.getLevelName(_LOGGER.getEffectiveLevel())
            )
        )
    elif debug:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug(
            "Effective logging level is {}".format(
                logging.getLevelName(_LOGGER.getEffectiveLevel())
            )
        )
    else:
        _LOGGER.setLevel(logging.WARNING)
        _LOGGER.warning(
            "Effective logging level is {}".format(
                logging.getLevelName(_LOGGER.getEffectiveLevel())
            )
        )
    _LOGGER.debug("Completed config_logging")
    return None


def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
            bp()
        return 0  # Indicate successful execution
    except Exception as e:
        _LOGGER.error(f"Error condition: {e}")
        return 1  # Indicate error


if __name__ == "__main__":
    config_logging()
    exit_code = main()
    if exit_code == 0:
        _LOGGER.info("Completed successfully.")
    else:
        _LOGGER.warning("Failed to complete.")
