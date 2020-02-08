#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

Version: 0.0.1  20200112 - Initial Release
Version: 0.0.2  20200203 - Changed restafval to pbd
Version: 0.0.3  20200205 - Added cities in Vijfheerenlanden
Version: 0.1.0  20200208 - Bug fix vijfheerenlanden + preperation for echtsusteren

Description:
- Home Assistant sensor for Afvalinfo

Currently supported cities:
- ameide
- everdingen
- hagestein
- hei- en boeicop
- hoef en haag
- kedichem
- leerbroek
- leerdam
- lexmond
- meerkerk
- nieuwland
- oosterwijk
- ossenwaard
- schoonrewoerd
- sliedrecht                        (does not support: restafval)
- tienhoven aan de lek
- vianen
- zijderveld

Almost supported cities (work in progress):
- dieteren                          (does not support: textiel, papier)
- echt                              (does not support: textiel, papier)
- koningsbosch                      (does not support: textiel, papier)
- maria hoop                        (does not support: textiel, papier)
- nieuwstadt                        (does not support: textiel, papier)
- pey                               (does not support: textiel, papier)
- roosteren                         (does not support: textiel, papier)
- sint joost                        (does not support: textiel, papier)
- susteren                          (does not support: textiel, papier)

resources options:
- gft                               (Groente, Fruit en Tuinafval)
- textiel
- papier
- pbd                               (Plastic, Blik en Drinkpakken)
- restafval

Example config:
Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:                       (at least 1 required)
        - pbd
      city: sliedrecht                 (required)
      postcode: 33361AB                (required)
      streetnumber: 1                  (required)
      dateformat: '%d-%m-%Y'           (optional)
"""

import voluptuous as vol
from datetime import datetime
import urllib.error
from .const.const import (
    MIN_TIME_BETWEEN_UPDATES,
    _LOGGER,
    CONF_CITY,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_DATE_FORMAT,
    SENSOR_PREFIX,
    ATTR_LAST_UPDATE,
    ATTR_HIDDEN,
    SENSOR_TYPES,
)

from .location.sliedrecht import SliedrechtAfval
from .location.vijfheerenlanden import VijfheerenlandenAfval
from .location.echtsusteren import EchtSusterenAfval

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ["BeautifulSoup4==4.7.0"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_RESOURCES, default=[]): vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        ),
        vol.Required(CONF_CITY, default="sliedrecht"): cv.string,
        vol.Required(CONF_POSTCODE, default="3361AB"): cv.string,
        vol.Required(CONF_STREET_NUMBER, default="1"): cv.string,
        vol.Optional(CONF_DATE_FORMAT, default="%d-%m-%Y"): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup Afvalinfo sensor")

    city = config.get(CONF_CITY).lower()
    postcode = config.get(CONF_POSTCODE)
    street_number = config.get(CONF_STREET_NUMBER)
    date_format = config.get(CONF_DATE_FORMAT)

    try:
        data = AfvalinfoData(city, postcode, street_number)
    except urllib.error.HTTPError as error:
        _LOGGER.error(error.reason)
        return False

    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        if sensor_type not in SENSOR_TYPES:
            SENSOR_TYPES[sensor_type] = [sensor_type.title(), "", "mdi:recycle"]

        entities.append(AfvalinfoSensor(data, sensor_type, date_format))

    add_entities(entities)


class AfvalinfoData(object):
    def __init__(self, city, postcode, street_number):
        self.data = None
        self.city = city
        self.postcode = postcode
        self.street_number = street_number

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Updating Waste collection dates")

        # try:
        if self.city == "sliedrecht":
            self.data = SliedrechtAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        if (
            self.city == "ameide"
            or self.city == "everdingen"
            or self.city == "hagestein"
            or self.city == "hei- en boeicop"
            or self.city == "hoef en haag"
            or self.city == "kedichem"
            or self.city == "leerbroek"
            or self.city == "leerdam"
            or self.city == "lexmond"
            or self.city == "meerkerk"
            or self.city == "nieuwland"
            or self.city == "oosterwijk"
            or self.city == "ossenwaard"
            or self.city == "schoonrewoerd"
            or self.city == "tienhoven aan de lek"
            or self.city == "vianen"
            or self.city == "zijderveld"
        ):
            self.data = VijfheerenlandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        if (
            self.city == "dieteren"
            or self.city == "echt"
            or self.city == "koningsbosch"
            or self.city == "maria hoop"
            or self.city == "nieuwstadt"
            or self.city == "pey"
            or self.city == "roosteren"
            or self.city == "sint joost"
            or self.city == "susteren"
        ):
            self.data = EchtSusterenAfval().get_data(
                self.city, self.postcode, self.street_number
            )

            # _LOGGER.warning("self.data")
            # _LOGGER.warning(self.data)


class AfvalinfoSensor(Entity):
    def __init__(self, data, sensor_type, date_format):
        self.data = data
        self.date_format = date_format
        self.type = sensor_type
        self._name = SENSOR_PREFIX + SENSOR_TYPES[sensor_type][0]
        self._icon = SENSOR_TYPES[sensor_type][1]
        self._hidden = False
        self._state = None
        self._last_update = None
        self._unit = ""

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {ATTR_LAST_UPDATE: self._last_update, ATTR_HIDDEN: self._hidden}

    @property
    def unit_of_measurement(self):
        return self._unit

    def update(self):
        self.data.update()
        waste_data = self.data.data

        try:
            if waste_data:
                if self.type in waste_data:
                    today = datetime.today()

                    collection_date = datetime.strptime(
                        waste_data[self.type], "%Y-%m-%d"
                    ).date()

                    if collection_date:
                        # Set the values of the sensor
                        self._last_update = today.strftime("%d-%m-%Y %H:%M")
                        self._state = collection_date.strftime(self.date_format)
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
        except ValueError:
            self._state = None
            self._hidden = True
