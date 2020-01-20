#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser
Current Version: 0.0.1  20200112 - Initial Release

Description:
- Home Assistant sensor for Afvalinfo

Currently supported cities:
- sliedrecht

resources options:
- gft       (afvalstroom 3)
- textiel   (afvalstroom 7)
- papier    (afvalstroom 87)
- restafval (afvalstroom 92)

Example config:
Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:                       (at least 1 required)
        - restafval
      city: sliedrecht                 (required)
      postcode: 33361AB                (required)
      streetnumber: 1                  (required)
      dateformat: '%d-%m-%Y'           (optional)
"""

import voluptuous as vol
import logging
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ["BeautifulSoup4==4.7.0"]

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)

CONF_CITY = "city"
CONF_POSTCODE = "postcode"
CONF_STREET_NUMBER = "streetnumber"
CONF_DATE_FORMAT = "dateformat"
SENSOR_PREFIX = "Afvalinfo "
ATTR_LAST_UPDATE = "Last update"
ATTR_HIDDEN = "Hidden"

SENSOR_TYPES = {
    "restafval": ["Restafval", "mdi:recycle"],
    "papier": ["Oud Papier", "mdi:recycle"],
    "gft": ["GFT", "mdi:recycle"],
    "textiel": ["Textiel", "mdi:recycle"],
}

SENSOR_CITIES_TO_URL = {
    "sliedrecht": ["https://sliedrecht.afvalinfo.nl/adres/", "{0}:{1}/"]
}

MONTH_TO_NUMBER = {
    "jan": "01",
    "feb": "02",
    "mrt": "03",
    "apr": "04",
    "mei": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "okt": "10",
    "nov": "11",
    "dec": "12",
}

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

    city = config.get(CONF_CITY)
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

    def get_date_from_afvalstroom(self, ophaaldata, afvalstroom):
        html = ophaaldata.find(href="/afvalstroom/" + str(afvalstroom))
        date = html.i.string[3:]
        day = date.split(" ")[0]
        month = MONTH_TO_NUMBER[date.split(" ")[1]]
        year = str(
            datetime.today().year
            if datetime.today().month <= int(month)
            else datetime.today().year + 1
        )
        return year + "-" + month + "-" + day

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            suffix_url = SENSOR_CITIES_TO_URL[self.city][1].format(
                self.postcode, self.street_number
            )
            url = SENSOR_CITIES_TO_URL[self.city][0] + suffix_url
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            # Specific for Sliedrecht ToDo: split into seperate class for the specific city
            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find(id="ophaaldata")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find afvalstroom/3 = gft
            waste_dict["gft"] = self.get_date_from_afvalstroom(ophaaldata, 3)
            # find afvalstroom/7 = textiel
            waste_dict["textiel"] = self.get_date_from_afvalstroom(ophaaldata, 7)
            # find afvalstroom/87 = papier
            waste_dict["papier"] = self.get_date_from_afvalstroom(ophaaldata, 87)
            # find afvalstroom/92 = restafval
            waste_dict["restafval"] = self.get_date_from_afvalstroom(ophaaldata, 92)

            self.data = waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            self.data = None
            return False


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

        """_LOGGER.warning("waste_data")
        _LOGGER.warning(waste_data)
        _LOGGER.warning("self.type")
        _LOGGER.warning(self.type)"""

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
