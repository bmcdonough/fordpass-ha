#!/usr/bin/env python3
import asyncio
import logging
import logging.handlers
import os

from dotenv import load_dotenv

from config_flow import ConfigFlow
from fordpass_new import Vehicle

import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant import config_entries, core, exceptions
from homeassistant.core import HomeAssistant
from const import DOMAIN


def config_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s[%(process)d] - [%(name)s:%(lineno)d] :: (%(funcName)s) %(levelname)s - %(message)s",
        handlers=[logging.handlers.SysLogHandler(address="/dev/log", facility="user")],
    )
    return(logging.getLogger(__name__))

async def my_step_status():
    # initialize async_step_user
    step_status = await cf.async_step_user(None)
    _LOGGER.debug(f"step_status1   {step_status}")
    if step_status["step_id"] == "user":
        _LOGGER.debug(f"At step_id: {step_status['step_id']}")
        user_input = {'username': fp_username, 'region': fp_region}
        _LOGGER.info("sending username and region")
        step_status = await cf.async_step_user(user_input)
        _LOGGER.debug(f"step_status2   {step_status}")
    elif step_status["step_id"] == "token":
        _LOGGER.debug(f"At step_id: {step_status['step_id']}")
        step_status = await cf.async_step_token(None)
        _LOGGER.debug(f"step_status3   {step_status}")
        _LOGGER.debug(f"dir-step_status   {dir(step_status)}")
    else:
        _LOGGER.debug("found else")
    return 0  # Indicate successful execution

async def my_call_to_fpn(url1):
    results = {}
    fpn = Vehicle(username=os.environ.get('FORDPASS_USERNAME'), password=os.environ.get('FORDPASS_PASSWORD'), vin=os.environ.get('FORDPASS_VIN'), region=os.environ.get('FORDPASS_REGION'), config_location=os.environ.get('HOME')+"/.fordpass_token")
    results = await(hass.async_add_executor_job(fpn.bmcd_auth(url1)))
    return(results)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the FordPass component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
            fp_username = os.environ.get('FORDPASS_USERNAME')
            fp_region = os.environ.get('FORDPASS_REGION')
            if (fp_username or fp_region) is None:
                _LOGGER.warning(f"if either fp_username:[{fp_username}] or fp_region:[{fp_region}] is None, stop")
                return 1
            await async_setup(HomeAssistant, None)
            # initialize ConfigFlow
            cf = ConfigFlow()
#            _LOGGER.debug(f"url from ConfigFlow.generate_url(region): {cf.generate_url(region=os.environ.get('FORDPASS_REGION'))}")
            fordpass_login_url = cf.generate_url(region=os.environ.get('FORDPASS_REGION'))

            what_happened = await my_call_to_fpn(fordpass_login_url)
            print(f"what happened: {vars(what_happened)}")
            return 0
        else:
            _LOGGER.warning("unable to load .env")
            print("unable to load .env")
            return 1

    except Exception as e:
        _LOGGER.error(f"Error condition: {e}")
        return 1  # Indicate error


if __name__ == "__main__":
    _LOGGER = config_logging()
    exit_code = asyncio.run(main())
    if exit_code == 0:
        _LOGGER.info("Completed successfully.")
        print("Completed Successfully.")
    else:
        _LOGGER.warning("Failed to complete.")
        print("Failed to complete.")
