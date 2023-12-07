#!/usr/bin/env python3
"""
Config flow component for Afvalinfo
Author: Jasper Slits
"""

from homeassistant.helpers.selector import selector
from homeassistant.helpers import config_validation as cv
from homeassistant import config_entries
from .const.const import (
    _LOGGER,
    DOMAIN,
    SENSOR_TYPES,
    CONF_ENABLED_SENSORS,
    CONF_DISTRICT,
    CONF_LOCATION,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_STREET_NUMBER_SUFFIX,
    CONF_GET_WHOLE_YEAR,
    CONF_DATE_FORMAT,
    CONF_NO_TRASH_TEXT,
    CONF_DIFTAR_CODE,
    CONF_LOCALE,
    CONF_ID
)

import voluptuous as vol

class AfvalWijzerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info):
        if info is not None:

            await self.async_set_unique_id(info["id"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Afvalinfo for " + info["id"],
                data=info
            )

        options = list(SENSOR_TYPES.keys())

        afvalinfo_schema = vol.Schema({
        vol.Required(CONF_ID, default="home"): str,
        vol.Optional(CONF_POSTCODE, default="3361AB"): str,
        vol.Optional(CONF_STREET_NUMBER, default="1"): cv.positive_int,
        vol.Optional(CONF_STREET_NUMBER_SUFFIX, default=""): str,
        vol.Optional(CONF_LOCATION, default=""): str,

        vol.Optional(CONF_DISTRICT, default=""): str,
        vol.Optional(CONF_DATE_FORMAT, default="%d-%m-%Y"): str,
        vol.Optional(CONF_LOCALE, default="nl"): vol.In(["nl","en"]),
        vol.Optional(CONF_NO_TRASH_TEXT, default="geen"): str,
        vol.Optional(CONF_DIFTAR_CODE, default=""): str,
        vol.Optional(CONF_GET_WHOLE_YEAR, default=False): cv.boolean,
        vol.Required(CONF_ENABLED_SENSORS,default=[]): selector({
                "select": {
                    "options": options,
                    "multiple": True,
                    "translation_key": "sensorselect"
                    }
            })


        })

        return self.async_show_form(
              step_id="user", data_schema=afvalinfo_schema)


