#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser
"""

import voluptuous as vol
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.error
from babel import Locale
from babel.dates import format_date, format_datetime, format_time
import re

from .const.const import (
    MIN_TIME_BETWEEN_UPDATES,
    _LOGGER,
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
    CONF_ID,
    SENSOR_PREFIX,
    ATTR_ERROR,
    ATTR_LAST_UPDATE,
    ATTR_DAYS_UNTIL_COLLECTION_DATE,
    ATTR_IS_COLLECTION_DATE_TODAY,
    ATTR_YEAR_MONTH_DAY_DATE,
    ATTR_FRIENDLY_NAME,
    ATTR_LAST_COLLECTION_DATE,
    ATTR_TOTAL_COLLECTIONS_THIS_YEAR,
    ATTR_WHOLE_YEAR_DATES,
    SENSOR_TYPES,
)

from .location.trashapi import TrashApiAfval
from .sensortomorrow import AfvalInfoTomorrowSensor
from .sensortoday import AfvalInfoTodaySensor

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_format_date(hass, collection_date, half_babel_half_date, locale):
    return await hass.async_add_executor_job(
        format_date, collection_date, half_babel_half_date, locale
    )

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    config = config_entry.data

    location = config.get(CONF_LOCATION).lower().strip()
    postcode = config.get(CONF_POSTCODE).strip()
    street_number = config.get(CONF_STREET_NUMBER)
    street_number_suffix = config.get(CONF_STREET_NUMBER_SUFFIX)
    district = config.get(CONF_DISTRICT)
    date_format = config.get(CONF_DATE_FORMAT).strip()
    locale = config.get(CONF_LOCALE)
    id_name = config.get(CONF_ID)
    no_trash_text = config.get(CONF_NO_TRASH_TEXT)
    diftar_code = config.get(CONF_DIFTAR_CODE)
    get_whole_year = config.get(CONF_GET_WHOLE_YEAR)


    resources = config[CONF_ENABLED_SENSORS].copy()

    # filter the types from the dict if it's a dictionary
    if isinstance(resources[0], dict):
            resourcesMinusTodayAndTomorrow = [obj["type"] for obj in resources]
    else:
            resourcesMinusTodayAndTomorrow = resources

    if "trash_type_today" in resourcesMinusTodayAndTomorrow:
            resourcesMinusTodayAndTomorrow.remove("trash_type_today")

    if "trash_type_tomorrow" in resourcesMinusTodayAndTomorrow:
            resourcesMinusTodayAndTomorrow.remove("trash_type_tomorrow")

    if (
            "cleanprofsgft" in resourcesMinusTodayAndTomorrow
            or "cleanprofsrestafval" in resourcesMinusTodayAndTomorrow
        ):
            get_cleanprofs_data = True
    else:
            get_cleanprofs_data = False

    data = AfvalinfoData(
            location,
            postcode,
            street_number,
            street_number_suffix,
            district,
            diftar_code,
            get_whole_year,
            resourcesMinusTodayAndTomorrow,
            get_cleanprofs_data,
        )

    await data.async_update()

    entities = []

    for resource in config[CONF_ENABLED_SENSORS]:
        sensor_type = resource
        if (
            resource != "trash_type_today"
            and resource != "trash_type_tomorrow"
        ):
            entities.append(
                AfvalinfoSensor(
                    data,
                    sensor_type,
                    date_format,
                    locale,
                    id_name,
                    get_whole_year,
                )
            )

        # Add sensor -trash_type_today
        if resource == "trash_type_today":
            today = AfvalInfoTodaySensor(
                hass,
                data,
                sensor_type,
                entities,
                id_name,
                no_trash_text,
            )
            entities.append(today)
        # Add sensor -trash_type_tomorrow
        if resource == "trash_type_tomorrow":
            tomorrow = AfvalInfoTomorrowSensor(
                hass,
                data,
                sensor_type,
                entities,
                id_name,
                no_trash_text,
            )
            entities.append(tomorrow)



    async_add_entities(entities)

class AfvalinfoData(object):
    def __init__(
        self,
        location,
        postcode,
        street_number,
        street_number_suffix,
        district,
        diftar_code,
        get_whole_year,
        resources,
        get_cleanprofs_data,
    ):
        self.data = None
        self.location = location
        self.postcode = postcode
        self.street_number = street_number
        self.street_number_suffix = street_number_suffix
        self.district = district
        self.diftar_code = diftar_code
        self.get_whole_year = get_whole_year
        self.resources = resources
        self.get_cleanprofs_data = get_cleanprofs_data

    # This will make sure that we can't execute it more often
    # than the MIN_TIME_BETWEEN_UPDATES
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        self.data = await TrashApiAfval().get_data(
            self.location,
            self.postcode,
            self.street_number,
            self.street_number_suffix,
            self.district,
            self.diftar_code,
            self.get_whole_year,
            self.resources,
            self.get_cleanprofs_data,
        )


class AfvalinfoSensor(Entity):
    _attr_has_entity_name = True

    def __init__(
        self,
        data,
        sensor_type,
        date_format,
        locale,
        id_name,
        get_whole_year,
    ):
        self.data = data
        self.type = sensor_type
        self.friendly_name = sensor_type

        self.date_format = date_format
        self.locale = locale

        self._get_whole_year = get_whole_year
        self.entity_id = "sensor." + (
            (
                SENSOR_PREFIX
                + (id_name + " " if len(id_name) > 0 else "")
                + sensor_type
            )
            .lower()
            .replace(" ", "_")
        )
        self._attr_unique_id = (
            SENSOR_PREFIX
            + (id_name + " " if len(id_name) > 0 else "")
            + sensor_type
        )

        self._attr_translation_key = "afvalinfo_" + sensor_type
        _LOGGER.debug("Setting translation key to " + self._attr_translation_key)

        self._icon = SENSOR_TYPES[sensor_type][1]
        self._error = False
        self._state = None
        self._last_update = None
        self._days_until_collection_date = None
        self._is_collection_date_today = False
        self._year_month_day_date = None
        self._last_collection_date = None
        self._total_collections_this_year = None
        self._whole_year_dates = None

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            ATTR_ERROR: self._error,
            ATTR_FRIENDLY_NAME: self.friendly_name,
            ATTR_YEAR_MONTH_DAY_DATE: self._year_month_day_date,
            ATTR_LAST_UPDATE: self._last_update,
            ATTR_DAYS_UNTIL_COLLECTION_DATE: self._days_until_collection_date,
            ATTR_IS_COLLECTION_DATE_TODAY: self._is_collection_date_today,
            ATTR_LAST_COLLECTION_DATE: self._last_collection_date,
            ATTR_TOTAL_COLLECTIONS_THIS_YEAR: self._total_collections_this_year,
            ATTR_WHOLE_YEAR_DATES: self._whole_year_dates,
        }

    # Run this every minute
    @Throttle(timedelta(minutes=1))
    async def async_update(self):
        """We are calling this often,
        but the @Throttle on the data.async_update
        will limit the times it will be executed"""
        await self.data.async_update()
        waste_array = self.data.data
        self._error = False

        # Loop through all the dates to put the dates in the whole_year_dates attribute
        if self._get_whole_year == True:
            whole_year_dates = []
            if waste_array:
                for waste_data in waste_array:
                    if self.type in waste_data:
                        whole_year_dates.append(
                            datetime.strptime(waste_data[self.type], "%Y-%m-%d").date()
                        )

                self._whole_year_dates = whole_year_dates

        try:
            if waste_array:
                for waste_data in waste_array:
                    if self.type in waste_data:
                        collection_date = datetime.strptime(
                            waste_data[self.type], "%Y-%m-%d"
                        ).date()

                        # Date in date format "%Y-%m-%d"
                        self._year_month_day_date = str(collection_date)

                        if collection_date:
                            # Set the values of the sensor
                            self._last_update = datetime.today().strftime(
                                "%d-%m-%Y %H:%M"
                            )

                            # Is the collection date today?
                            self._is_collection_date_today = (
                                date.today() == collection_date
                            )

                            # Get the diftar data
                            if self.type == "restafval":
                                for obj in waste_array:
                                    if "restafvaldiftardate" in obj:
                                        self._last_collection_date = str(
                                            datetime.strptime(
                                                obj["restafvaldiftardate"], "%Y-%m-%d"
                                            ).date()
                                        )
                                        break
                                for obj in waste_array:
                                    if "restafvaldiftarcollections" in obj:
                                        self._total_collections_this_year = obj[
                                            "restafvaldiftarcollections"
                                        ]
                                        break

                            # Days until collection date
                            delta = collection_date - date.today()
                            self._days_until_collection_date = delta.days

                            # if the date does not contain a named day or month, return the date as normal
                            if (
                                self.date_format.find("a") == -1
                                and self.date_format.find("A") == -1
                                and self.date_format.find("b") == -1
                                and self.date_format.find("B") == -1
                            ):
                                self._state = collection_date.strftime(self.date_format)
                                break  # we have a result, break the loop
                            # else convert the named values to the locale names
                            else:
                                edited_date_format = self.date_format.replace(
                                    "%a", "EEE"
                                )
                                edited_date_format = edited_date_format.replace(
                                    "%A", "EEEE"
                                )
                                edited_date_format = edited_date_format.replace(
                                    "%b", "MMM"
                                )
                                edited_date_format = edited_date_format.replace(
                                    "%B", "MMMM"
                                )

                                # half babel, half date string... something like EEEE 04-MMMM-2020
                                half_babel_half_date = collection_date.strftime(
                                    edited_date_format
                                )

                                # replace the digits with qquoted digits 01 --> '01'
                                half_babel_half_date = re.sub(
                                    r"(\d+)", r"'\1'", half_babel_half_date
                                )
                                # transform the EEE, EEEE etc... to a real locale date, with babel
                                locale_date = await async_format_date(
                                    self.hass,
                                    collection_date,
                                    half_babel_half_date,
                                    self.locale,
                                )

                                self._state = locale_date
                                break  # we have a result, break the loop
                        else:
                            # collection_date empty
                            raise ValueError()
                    # else:
                    # No matching result data for current waste type, no problem
            else:
                raise ValueError()
        except ValueError:
            self._error = True
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
