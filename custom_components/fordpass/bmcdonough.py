#!/usr/bin/env python3
import asyncio
import logging
import logging.handlers
import os
from pdb import set_trace as bp

from dotenv import load_dotenv

from config_flow import ConfigFlow
from fordpass_new import Vehicle

# from const import (
#    CONF_DISTANCE_UNIT,
#    CONF_PRESSURE_UNIT,
#    COORDINATOR,
#    DEFAULT_DISTANCE_UNIT,
#    DEFAULT_PRESSURE_UNIT,
#    DOMAIN,
#    MANUFACTURER,
#    REGION,
#    UPDATE_INTERVAL,
#    UPDATE_INTERVAL_DEFAULT,
#    VEHICLE,
#    VIN,
# )


_LOGGER = logging.getLogger(__name__)
# verbose = True
verbose = False
debug = True
# debug = False


def config_logging():
    syslog_fmt = "%(filename)s[%(process)d] - [%(name)s:%(lineno)d] :: (%(funcName)s) %(levelname)s - %(message)s"
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


async def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
            fc_username = os.environ.get('FORDCONNECT_USERNAME')
            fc_region = os.environ.get('FORDCONNECT_REGION')
            _LOGGER.debug(globals())
            # initialize ConfigFlow
            cf = ConfigFlow()
            _LOGGER.debug(f"dir(cf)   {dir(cf)}")
            # initialize async_step_user
            step_status = await cf.async_step_user(None)
            _LOGGER.debug(f"step_status1   {step_status}")

            if step_status["step_id"] == "user":
                _LOGGER.debug(f"At step_id: {step_status['step_id']}")
                user_input = {'username': fc_username, 'region': fc_region}
                _LOGGER.info("sending username and region")
                step_status = await cf.async_step_user(user_input)
                _LOGGER.debug(f"step_status2   {step_status}")
                inferred_schema = {}
                for key, value in step_status['data_schema'].schema.items():
                    inferred_schema[key] = type(value)
                print(f"inferred_schema: {inferred_schema}")
            else:
                _LOGGER.debug("found else")

            if step_status["step_id"] == "token":
                _LOGGER.debug(f"At step_id: {step_status['step_id']}")

                schema_from_library = step_status['data_schema']
                print(f"schema: {schema_from_library}")
                print(f"dir-schema: {dir(schema_from_library)}")
                print(f"vars-schema: {vars(schema_from_library)}")
                print(f"schema.schema: {schema_from_library.schema}")
                print(f"dir-schema.schema: {dir(schema_from_library.schema)}")
#                print(f"vars-schema.schema: {vars(schema_from_library.schema)}")

                inferred_schema = {}
                for key, value in schema_from_library.items():
                    inferred_schema[key] = type(value)
                print(f"inferred_schema: {inferred_schema}")
#                my_data = {}
#                validated_data = schema_from_library(my_data)
#                print(f"validated_data: {validated_data}")

                step_status = await cf.async_step_token(None)
                _LOGGER.debug(f"step_status3   {step_status}")
                _LOGGER.debug(f"dir-step_status   {dir(step_status)}")
            else:
                _LOGGER.debug("found else")
        return 0  # Indicate successful execution
    except Exception as e:
        _LOGGER.error(f"Error condition: {e}")
        return 1  # Indicate error


if __name__ == "__main__":
    config_logging()
    exit_code = asyncio.run(main())
    if exit_code == 0:
        _LOGGER.info("Completed successfully.")
        print("Completed Successfully.")
    else:
        _LOGGER.warning("Failed to complete.")
        print("Failed to complete.")
