#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

Version: 0.0.1  20200112 - Initial Release
Version: 0.0.2  20200203 - Changed restafval to pbd
Version: 0.0.3  20200205 - Added locations in Vijfheerenlanden
Version: 0.1.0  20200208 - Bug fix vijfheerenlanden + preperation for Echt-Susteren
Version: 0.1.1  20200209 - Added locations in Echt-Susteren
Version: 0.1.2  20200210 - Added locations for Twente Milieu
Version: 0.1.3  20200212 - Added option to limit the days to look into the future
Version: 0.1.4  20200213 - Small refactoring of some code + preperation for Westland
Version: 0.1.5  20200213 - Added locations for Westland

Description:
- Home Assistant sensor for Afvalinfo

Currently supported cities:

--Echt-Susteren                     (does not support: textiel, papier)
- dieteren
- echt
- koningsbosch
- maria hoop
- nieuwstadt
- pey
- roosteren
- sint joost
- susteren

--Sliedrecht                        (does not support: restafval)
- sliedrecht

--Twente Milieu                     (does not support: textiel)
- almelo
- borne
- enschede
- haaksbergen
- hengelo
- hof van twente
- losser
- oldenzaal
- wierden

--Vijfheerenlanden
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
- tienhoven aan de lek
- vianen
- zijderveld

--Westland                          (does not support: pbd, textiel)
- de lier
- s-gravenzande
- honselersdijk
- kwintsheul
- maasdijk
- monster
- naaldwijk
- poeldijk
- ter heijde
- wateringen

resources options:
- gft                               (Groente, Fruit en Tuinafval)
- papier
- pbd                               (Plastic, Blik en Drinkpakken)
- restafval
- textiel


Example config:
Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:                       (at least 1 required)
        - pbd
      city: sliedrecht                 (required, default = sliedrecht)
      postcode: 33361AB                (required, default = 3361AB)
      streetnumber: 1                  (required, default = 1)
      dateformat: '%d-%m-%Y'           (optional, default = %d-%m-%Y) day-month-year
      timespanindays: 365              (optional, default = 365) number of days to look into the future
"""

import voluptuous as vol
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import urllib.error
from .const.const import (
    MIN_TIME_BETWEEN_UPDATES,
    _LOGGER,
    CONF_CITY,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_DATE_FORMAT,
    CONF_TIMESPAN_IN_DAYS,
    SENSOR_PREFIX,
    ATTR_LAST_UPDATE,
    ATTR_HIDDEN,
    SENSOR_TYPES,
)

from .location.sliedrecht import SliedrechtAfval
from .location.vijfheerenlanden import VijfheerenlandenAfval
from .location.echtsusteren import EchtSusterenAfval
from .location.twentemilieu import TwentemilieuAfval
from .location.westland import WestlandAfval

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
        vol.Optional(CONF_DATE_FORMAT, default = "%d-%m-%Y"): cv.string,
        vol.Optional(CONF_TIMESPAN_IN_DAYS, default = "365"): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup Afvalinfo sensor")

    city = config.get(CONF_CITY).lower()
    postcode = config.get(CONF_POSTCODE)
    street_number = config.get(CONF_STREET_NUMBER)
    date_format = config.get(CONF_DATE_FORMAT)
    timespan_in_days = config.get(CONF_TIMESPAN_IN_DAYS)

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

        entities.append(AfvalinfoSensor(data, sensor_type, date_format, timespan_in_days))

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
        if (
            self.city == "almelo"
            or self.city == "borne"
            or self.city == "enschede"
            or self.city == "haaksbergen"
            or self.city == "hengelo"
            or self.city == "hof van twente"
            or self.city == "losser"
            or self.city == "oldenzaal"
            or self.city == "wierden"
        ):
            self.data = TwentemilieuAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        if (
            self.city == "de lier"
            or self.city == "s-gravenzande"
            or self.city == "honselersdijk"
            or self.city == "kwintsheul"
            or self.city == "maasdijk"
            or self.city == "monster"
            or self.city == "naaldwijk"
            or self.city == "poeldijk"
            or self.city == "ter heijde"
            or self.city == "wateringen"
        ):
            self.data = WestlandAfval().get_data(
                self.city, self.postcode, self.street_number
            )

            # _LOGGER.warning("self.data")
            # _LOGGER.warning(self.data)


class AfvalinfoSensor(Entity):
    def __init__(self, data, sensor_type, date_format, timespan_in_days):
        self.data = data
        self.type = sensor_type
        self.date_format = date_format
        self.timespan_in_days = timespan_in_days
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
                    today = date.today()

                    collection_date = datetime.strptime(
                        waste_data[self.type], "%Y-%m-%d"
                    ).date()

                    if collection_date:
                        # Set the values of the sensor
                        self._last_update = today.strftime("%d-%m-%Y %H:%M")

                        # Only show the value if the date is lesser than or equal to (today + timespan_in_days)
                        if collection_date <= today + relativedelta(days=int(self.timespan_in_days)):
                            self._state = collection_date.strftime(self.date_format)
                        else:
                            self._hidden = True
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
        except ValueError:
            self._state = None
            self._hidden = True
