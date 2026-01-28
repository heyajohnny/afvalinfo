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
    CONF_LOCATION,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_STREET_NUMBER_SUFFIX,
    CONF_GET_WHOLE_YEAR,
    CONF_DATE_FORMAT,
    CONF_NO_TRASH_TEXT,
    CONF_DIFTAR_CODE,
    CONF_LOCALE,
    CONF_ID,
    CONF_CALENDAR_START_TIME,
    CONF_CALENDAR_ALL_DAY,
    CONF_MANUAL_DATES,
    CONF_MANUAL_DATES_ENABLED,
)

import voluptuous as vol

CONF_CALENDAR = "calendar"


class AfvalWijzerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_reconfigure(self, user_input: Mapping[str, Any] | None = None):
        """Handle reconfigure step."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry

        if user_input is not None:
            try:
                # First try to unload the entry
                if not await self.hass.config_entries.async_unload(entry.entry_id):
                    _LOGGER.error("Failed to unload entry")
                    return self.async_abort(reason="cannot_unload")

                # Convert Mapping to dict to make it mutable
                user_input = dict(user_input)

                # Ensure empty strings are preserved for these optional properties
                if CONF_POSTCODE not in user_input:
                    user_input[CONF_POSTCODE] = ""
                if CONF_STREET_NUMBER not in user_input:
                    user_input[CONF_STREET_NUMBER] = ""
                if CONF_STREET_NUMBER_SUFFIX not in user_input:
                    user_input[CONF_STREET_NUMBER_SUFFIX] = ""
                if CONF_LOCATION not in user_input:
                    user_input[CONF_LOCATION] = ""
                if CONF_NO_TRASH_TEXT not in user_input:
                    user_input[CONF_NO_TRASH_TEXT] = ""
                if CONF_DIFTAR_CODE not in user_input:
                    user_input[CONF_DIFTAR_CODE] = ""
                if CONF_CALENDAR_START_TIME not in user_input:
                    user_input[CONF_CALENDAR_START_TIME] = "20:00"
                if CONF_CALENDAR_ALL_DAY not in user_input:
                    user_input[CONF_CALENDAR_ALL_DAY] = False
                if CONF_MANUAL_DATES_ENABLED not in user_input:
                    user_input[CONF_MANUAL_DATES_ENABLED] = False
                if CONF_MANUAL_DATES not in user_input:
                    user_input[CONF_MANUAL_DATES] = "{}"

                # Validate that at least one sensor is selected
                if not user_input.get(CONF_ENABLED_SENSORS) and not user_input.get(
                    CONF_CALENDAR
                ):
                    return await self._redo_configuration(
                        entry.data, errors={"base": "no_sensors_or_calendar_selected"}
                    )

                # Create new data combining old entry data with new user input
                new_data = {**entry.data, **user_input}

                # Then update it with cleaned input
                self.hass.config_entries.async_update_entry(
                    entry,
                    data=new_data,
                )

                # Finally reload it using our custom reload function
                from . import async_reload_entry

                await async_reload_entry(self.hass, entry)
                return self.async_abort(reason="reconfigure_successful")

            except Exception as ex:
                _LOGGER.error("Error reconfiguring entry %s: %s", entry.entry_id, ex)
                return await self._redo_configuration(
                    entry.data, errors={"base": "reconfigure_failed"}
                )

        return await self._redo_configuration(entry.data)

    async def _redo_configuration(self, entry_data: Mapping[str, Any], errors=None):
        afvalinfo_schema = self._get_afvalinfo_schema(entry_data)
        return self.async_show_form(
            step_id="reconfigure", data_schema=afvalinfo_schema, errors=errors
        )

    async def async_step_user(self, info):
        if info is not None:
            # Validate that at least one sensor is selected
            if not info.get(CONF_ENABLED_SENSORS) and not info.get(CONF_CALENDAR):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_afvalinfo_schema(info),
                    errors={"base": "no_sensors_or_calendar_selected"},
                )

            await self.async_set_unique_id(info["id"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Afvalinfo for " + info["id"], data=info
            )

        return self.async_show_form(
            step_id="user", data_schema=self._get_afvalinfo_schema(info)
        )

    def _get_afvalinfo_schema(self, info=None):
        options = list(SENSOR_TYPES.keys())

        # Bepaal of dit een reconfigure is (info is een dict met entry data)
        is_reconfigure = info and isinstance(info, dict) and CONF_ID in info

        if is_reconfigure:
            # Reconfigure schema
            return vol.Schema(
                {
                    vol.Required(CONF_ID, default=info[CONF_ID]): str,
                    vol.Optional(
                        CONF_POSTCODE,
                        description={"suggested_value": info.get(CONF_POSTCODE, "")},
                    ): str,
                    vol.Optional(
                        CONF_STREET_NUMBER,
                        description={
                            "suggested_value": info.get(CONF_STREET_NUMBER, "")
                        },
                    ): cv.positive_int,
                    vol.Optional(
                        CONF_STREET_NUMBER_SUFFIX,
                        description={
                            "suggested_value": info.get(CONF_STREET_NUMBER_SUFFIX, "")
                        },
                    ): str,
                    vol.Optional(
                        CONF_LOCATION,
                        description={"suggested_value": info.get(CONF_LOCATION, "")},
                    ): str,
                    vol.Optional(CONF_DATE_FORMAT, default=info[CONF_DATE_FORMAT]): str,
                    vol.Optional(CONF_LOCALE, default=info[CONF_LOCALE]): vol.In(
                        ["nl", "en"]
                    ),
                    vol.Optional(
                        CONF_NO_TRASH_TEXT,
                        description={
                            "suggested_value": info.get(CONF_NO_TRASH_TEXT, "")
                        },
                    ): str,
                    vol.Optional(
                        CONF_DIFTAR_CODE,
                        description={"suggested_value": info.get(CONF_DIFTAR_CODE, "")},
                    ): str,
                    vol.Required(
                        CONF_ENABLED_SENSORS, default=info[CONF_ENABLED_SENSORS]
                    ): selector(
                        {
                            "select": {
                                "options": options,
                                "multiple": True,
                                "translation_key": "sensorselect",
                            }
                        }
                    ),
                    vol.Optional(
                        CONF_CALENDAR,
                        default=info.get(CONF_CALENDAR, False),
                    ): bool,
                    vol.Optional(
                        CONF_CALENDAR_ALL_DAY,
                        default=info.get(CONF_CALENDAR_ALL_DAY, False),
                    ): bool,
                    vol.Optional(
                        CONF_CALENDAR_START_TIME,
                        default=info.get(CONF_CALENDAR_START_TIME, "20:00"),
                    ): str,
                    vol.Optional(
                        CONF_MANUAL_DATES_ENABLED,
                        default=info.get(CONF_MANUAL_DATES_ENABLED, False),
                    ): bool,
                    vol.Optional(
                        CONF_MANUAL_DATES,
                        default=info.get(CONF_MANUAL_DATES, "{}"),
                    ): str,
                }
            )
        else:
            # Nieuwe entry schema
            return vol.Schema(
                {
                    vol.Required(CONF_ID, default="home"): str,
                    vol.Optional(CONF_POSTCODE, default="3361AB"): str,
                    vol.Optional(CONF_STREET_NUMBER, default="1"): cv.positive_int,
                    vol.Optional(CONF_STREET_NUMBER_SUFFIX, default=""): str,
                    vol.Optional(CONF_LOCATION, default=""): str,
                    vol.Optional(CONF_DATE_FORMAT, default="%d-%m-%Y"): str,
                    vol.Optional(CONF_LOCALE, default="nl"): vol.In(["nl", "en"]),
                    vol.Optional(CONF_NO_TRASH_TEXT, default="geen"): str,
                    vol.Optional(CONF_DIFTAR_CODE, default=""): str,
                    vol.Required(CONF_ENABLED_SENSORS, default=[]): selector(
                        {
                            "select": {
                                "options": options,
                                "multiple": True,
                                "translation_key": "sensorselect",
                            }
                        }
                    ),
                    vol.Optional(
                        CONF_CALENDAR,
                        default=info.get(CONF_CALENDAR, False) if info else False,
                    ): bool,
                    vol.Optional(
                        CONF_CALENDAR_ALL_DAY,
                        default=info.get(CONF_CALENDAR_ALL_DAY, False)
                        if info
                        else False,
                    ): bool,
                    vol.Optional(
                        CONF_CALENDAR_START_TIME,
                        default="20:00",
                    ): str,
                    vol.Optional(
                        CONF_MANUAL_DATES_ENABLED,
                        default=False,
                    ): bool,
                    vol.Optional(
                        CONF_MANUAL_DATES,
                        default="{}",
                    ): str,
                }
            )
