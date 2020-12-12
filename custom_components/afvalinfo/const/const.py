import logging
from datetime import timedelta

SENSOR_TYPES = {
    "gft": ["GFT", "mdi:recycle"],
    "papier": ["Papier", "mdi:recycle"],
    "pbd": ["PBD", "mdi:recycle"],
    "restafval": ["Restafval", "mdi:recycle"],
    "textiel": ["Textiel", "mdi:recycle"],
    "trash_type_today": ["Today", "mdi:recycle"],
    "trash_type_tomorrow": ["Tomorrow", "mdi:recycle"]
}

SENSOR_LOCATIONS_TO_URL = {
    "defriesemeren": ["https://www.afvalalert.nl/kalender/{0}/{1}/?web=1"],
    "hoekschewaard": ["https://www.radhw.nl/inwoners/ophaalschema?p={0}&h={1}"],
    "katwijk": ["https://afval.katwijk.nl/nc/afvalkalender/?tx_windwastecalendar_pi1%5Baction%5D=search"],
    "middendrenthe": [
        "https://www.middendrenthe.nl/website/!suite86.scherm0325?mPag=6523&mAlle=J",
        "https://www.middendrenthe.nl/website/!ctm_afval.Kalender"],
    "montferland": [
        "https://www.montferland.afvalwijzer.net/",
        "https://www.montferland.afvalwijzer.net/aanmelden.aspx"
        ],
    "trashapi": ["http://trashapi.azurewebsites.net/trash?Location={0}&ZipCode={1}&HouseNumber={2}"],
    "uden": ["https://www.uden.nl/inwoners/afval/ophaaldagen-afval/{0}-{1}.html"],
    "veldhoven": ["https://www.veldhoven.nl/afvalkalender/{0}-{1}"],
    "venlo": ["https://www.venlo.nl/trash-removal-calendar/{0}/{1}"],
    "westerkwartier": ["https://www.afvalalert.nl/kalender/{0}/{1}/?web=1"],
    "westerwolde": ["https://www.westerwolde.nl/trash-removal-calendar/{0}/{1}"],
    "westland": ["https://huisvuilkalender.gemeentewestland.nl/huisvuilkalender/Huisvuilkalender/get-huisvuilkalender-ajax"]
}

SENSOR_LOCATIONS_TO_COMPANY_CODE = {
    "westland": ["https://huisvuilkalender.gemeentewestland.nl/huisvuilkalender/Huisvuilkalender/get-huisvuilkalender-ajax"]
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

NUMBER_TO_MONTH = {
    1: "januari",
    2: "februari",
    3: "maart",
    4: "april",
    5: "mei",
    6: "juni",
    7: "juli",
    8: "augustus",
    9: "september",
    10: "oktober",
    11: "november",
    12: "december",
}

CONF_CITY = "city"
CONF_LOCATION = "location"
CONF_POSTCODE = "postcode"
CONF_STREET_NUMBER = "streetnumber"
CONF_DATE_FORMAT = "dateformat"
CONF_TIMESPAN_IN_DAYS = "timespanindays"
CONF_LOCALE = "locale"
CONF_ID = "id"
SENSOR_PREFIX = "Afvalinfo "
ATTR_LAST_UPDATE = "last_update"
ATTR_HIDDEN = "hidden"
ATTR_IS_COLLECTION_DATE_TODAY = "is_collection_date_today"
ATTR_DAYS_UNTIL_COLLECTION_DATE = "days_until_collection_date"
ATTR_YEAR_MONTH_DAY_DATE = "year_month_day_date"

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)