import logging
from datetime import timedelta

SENSOR_TYPES = {
    "gft": ["GFT", "mdi:recycle"],
    "papier": ["Oud Papier", "mdi:recycle"],
    "pbd": ["PBD", "mdi:recycle"],
    "restafval": ["Restafval", "mdi:recycle"],
    "textiel": ["Textiel", "mdi:recycle"],
}

SENSOR_LOCATIONS_TO_URL = {
    "sliedrecht": ["https://sliedrecht.afvalinfo.nl/adres/", "{0}:{1}/"],
    "echtsusteren": [
        "http://echt-susteren.deafvalapp.nl/calendar/kalender_sessie.jsp?land=NL&postcode={0}&straatId=&huisnr={1}/"
    ],
}

SENSOR_LOCATIONS_TO_COMPANY_CODE = {
    "vijfheerenlanden": ["942abcf6-3775-400d-ae5d-7380d728b23c"]
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

CONF_CITY = "city"
CONF_POSTCODE = "postcode"
CONF_STREET_NUMBER = "streetnumber"
CONF_DATE_FORMAT = "dateformat"
SENSOR_PREFIX = "Afvalinfo "
ATTR_LAST_UPDATE = "Last update"
ATTR_HIDDEN = "Hidden"

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)
