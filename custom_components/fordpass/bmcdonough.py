#!/usr/bin/env python3
import asyncio
import logging
import logging.handlers
import os
from pdb import set_trace as bp

from dotenv import load_dotenv

from config_flow import ConfigFlow
from fordpass_new import Vehicle

import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant import config_entries, core, exceptions

from const import DOMAIN

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

def print_form_values(hass: core.HomeAssistant, form_entity_id):
    """Prints all values in a Home Assistant form entity.

    Args:
        hass (homeassistant.core.HomeAssistant): The Home Assistant instance.
        form_entity_id (str): The entity ID of the form entity.
    """

    entity_registry = er.EntityRegistry(hass)
    form = entity_registry.async_get(form_entity_id)

    if form is None:
        print(f"Entity not found: {form_entity_id}")
        return

    # Access form data based on its schema
    schema = form.schema
    values = hass.data.get(form_entity_id)

    # Iterate through schema fields and print values
    for field_name, field_data in schema.get('schema', {}).items():
        field_value = values.get(field_name)
        print(f"{field_name}: {field_value}")

def log_step_status(self):
    if type(self).__name__ == 'dict':
        _LOGGER.debug(f"found dictionary: {type(self).__name__}")
        for key, value in self.items():
            _LOGGER.debug("---")
            _LOGGER.debug(f"self key:{key}, value:{value} value_type:{type(value)}")
            if 'data_schema' in key:
                _LOGGER.debug("--- ---")
                _LOGGER.debug(f"found data schema: {self[key]}")
                _LOGGER.debug(f"dir data schema: {dir(self[key])}")
                for key2, value2 in self[key].schema.items():
                    _LOGGER.debug("--- --- ---")
                    _LOGGER.debug(f"self['{key}'].schema, key2:{key2} value2:{value2} value2_type:{type(value2)}")
                    _LOGGER.debug(f"found data schema in schema: {key2}")
                    _LOGGER.debug(f"dir data schema in schema: {dir(key2)}")
                    bp()
                    for key3, value3 in value2.schema.items():
                        _LOGGER.debug("--- --- --- ---")
                        _LOGGER.debug(f"key3.schema, key3:{key3} value3:{value3} value3_type:{type(value3)}")
            if hasattr(key, 'schema'):
                _LOGGER.debug(f"schema in key: {self[key]}")
    return None


async def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
            fc_username = os.environ.get('FORDCONNECT_USERNAME')
            fc_region = os.environ.get('FORDCONNECT_REGION')
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

                print(f"\n###")
#                print_form_values(hass, step_status)
                print(f"###\n")
                log_step_status(step_status)

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
