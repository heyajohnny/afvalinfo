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
    "deafvalapp": [
        "http://www.deafvalapp.nl/calendar/kalender_sessie.jsp?land=NL&postcode={0}&straatId=&huisnr={1}&huisnrtoev=",
        "http://www.deafvalapp.nl/calendar/kalender_dashboard.jsp",
    ],
    "sliedrecht": ["https://sliedrecht.afvalinfo.nl/adres/", "{0}:{1}/"],
    "twentemilieu": [
        "https://wasteapi.2go-mobile.com/api/FetchAdress",
        "https://wasteapi.2go-mobile.com/api/GetCalendar"
    ],
    "vijfheerenlanden": [
        "https://wasteapi.ximmio.com/api/FetchAdress",
        "https://wasteapi.ximmio.com/api/GetCalendar"
    ],
    "westerkwartier": ["https://www.afvalalert.nl/kalender/{0}/{1}/?web=1"],
    "westland": ["https://huisvuilkalender.gemeentewestland.nl/huisvuilkalender/Huisvuilkalender/get-huisvuilkalender-ajax"]
}

SENSOR_LOCATIONS_TO_COMPANY_CODE = {
    "vijfheerenlanden": ["942abcf6-3775-400d-ae5d-7380d728b23c"],
    "twentemilieu": ["8d97bb56-5afd-4cbc-a651-b4f7314264b4"],
    # ToDo: "hellendoorn": ["24434f5b-7244-412b-9306-3a2bd1e22bc1"],
    # ToDo: "acv": ["f8e2844a-095e-48f9-9f98-71fceb51d2c3"],
    #ACV = Ede, Renkum, Renswoude, Veenendaal, Wageningen
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
    "januari": "01",
    "februari": "02",
    "maart": "03",
    "april": "04",
    "mei": "05",
    "juni": "06",
    "juli": "07",
    "augustus": "08",
    "september": "09",
    "oktober": "10",
    "november": "11",
    "december": "12",
}

CONF_CITY = "city"
CONF_POSTCODE = "postcode"
CONF_STREET_NUMBER = "streetnumber"
CONF_DATE_FORMAT = "dateformat"
CONF_TIMESPAN_IN_DAYS = "timespanindays"
SENSOR_PREFIX = "Afvalinfo "
ATTR_LAST_UPDATE = "last_update"
ATTR_HIDDEN = "hidden"
ATTR_IS_COLLECTION_DATE_TODAY = "is_collection_date_today"
ATTR_DAYS_UNTIL_COLLECTION_DATE = "days_until_collection_date"

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)
