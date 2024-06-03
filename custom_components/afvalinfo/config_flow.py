#!/usr/bin/env python3
"""
Config flow component for Afvalinfo
Author: Jasper Slits
"""
from typing import Any
from collections.abc import Mapping

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

    async def async_step_reconfigure(self, user_input: Mapping[str, Any] | None = None):
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry
        if user_input:
            return self.async_update_reload_and_abort(entry, data=user_input, reason="reconfigure_successful")

        return await self._redo_configuration(entry.data)

    async def _redo_configuration(self, entry_data: Mapping[str, Any]):

        options = list(SENSOR_TYPES.keys())

        afvalinfo_schema = vol.Schema({
        vol.Required(CONF_ID, default=entry_data[CONF_ID]): str,
        vol.Optional(CONF_POSTCODE, default=entry_data[CONF_POSTCODE] ): str,
        vol.Optional(CONF_STREET_NUMBER, default=entry_data[CONF_STREET_NUMBER] ): cv.positive_int,
        vol.Optional(CONF_STREET_NUMBER_SUFFIX, default=entry_data[CONF_STREET_NUMBER_SUFFIX]): str,
        vol.Optional(CONF_LOCATION, default=entry_data[CONF_LOCATION]): str,

        vol.Optional(CONF_DISTRICT, default=entry_data[CONF_DISTRICT]): str,
        vol.Optional(CONF_DATE_FORMAT, default=entry_data[CONF_DATE_FORMAT]): str,
        vol.Optional(CONF_LOCALE, default=entry_data[CONF_LOCALE]): vol.In(["nl","en"]),
        vol.Optional(CONF_NO_TRASH_TEXT, default=entry_data[CONF_NO_TRASH_TEXT] ): str,
        vol.Optional(CONF_DIFTAR_CODE, default=entry_data[CONF_DIFTAR_CODE]): str,
        vol.Optional(CONF_GET_WHOLE_YEAR, default=entry_data[CONF_GET_WHOLE_YEAR]): cv.boolean,
        vol.Required(CONF_ENABLED_SENSORS,default=entry_data[CONF_ENABLED_SENSORS]): selector({
                "select": {
                    "options": options,
                    "multiple": True,
                    "translation_key": "sensorselect"
                    }
            })
        })
        return self.async_show_form(
                         step_id="reconfigure", data_schema=afvalinfo_schema)


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


