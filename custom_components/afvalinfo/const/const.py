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
    "afvalstoffendienstkalender": ["https://{0}.afvalstoffendienstkalender.nl/nl/{1}/{2}/"],
    "afvalstoffendienstkalender-s-hertogenbosch": ["https://afvalstoffendienstkalender.nl/nl/{0}/{1}/"],
    "alkmaar": ["https://inzamelkalender.stadswerk072.nl/adres/{0}:{1}"],
    "alphenaandenrijn": ["https://afvalkalender.alphenaandenrijn.nl/adres/{0}:{1}"],
    "avalex": [
        "https://www.avalex.nl/rest/adressen/{0}-{1}",
        "https://www.avalex.nl/rest/adressen/{0}/kalender/{1}"
    ],
    "beesel": ["https://www.beesel.nl/inwoners/afval-en-milieu/afvalkalender/{0}-{1}.html"],
    "berkelland": ["https://afvalkalender.gemeenteberkelland.nl/adres/{0}:{1}"],
    "blink": ["https://mijnblink.nl/adres/{0}:{1}"],
    "borsele": ["https://afvalkalender.borsele.nl/afval/afvalkalender/{0}/{1}"],
    "circulusberkel": ["https://afvalkalender.circulus-berkel.nl/adres/{0}:{1}"],
    "cranendonck": ["https://afvalkalender.cranendonck.nl/adres/{0}:{1}"],
    "cyclus": ["https://afvalkalender.cyclusnv.nl/adres/{0}:{1}"],
    "dar": ["https://afvalkalender.dar.nl/adres/{0}:{1}"],
    "deafvalapp": [
        "http://www.deafvalapp.nl/calendar/kalender_sessie.jsp?land=NL&postcode={0}&straatId=&huisnr={1}&huisnrtoev=",
        "http://www.deafvalapp.nl/calendar/kalender_dashboard.jsp",
    ],
    "defriesemeren": ["https://www.afvalalert.nl/kalender/{0}/{1}/?web=1"],
    "denhaag": [
        "https://huisvuilkalender.denhaag.nl/rest/adressen/{0}-{1}",
        "https://huisvuilkalender.denhaag.nl/rest/adressen/{0}/kalender/{1}"
    ],
    "drimmelen": ["https://drimmelen.nl/trash-removal-calendar/{0}/{1}"],
    "gad": ["https://inzamelkalender.gad.nl/adres/{0}:{1}"],
    "goereeoverflakkee": ["https://webadapter.watsoftware.nl/widget.aspx?version=3.7&action=3000001&xml=<postcode>{0}</postcode><huisnummer>{1}</huisnummer><guid>BCE23C06-E248-4300-B97F-E308A451C6B4</guid>"],
    "groningen": ["https://gemeente.groningen.nl/afvalwijzer/groningen/{0}/{1}/{2}/"],
    "hoekschewaard": ["https://www.radhw.nl/inwoners/ophaalschema?p={0}&h={1}"],
    "hvc": [
        "https://inzamelkalender.hvcgroep.nl/rest/adressen/{0}-{1}",
        "https://inzamelkalender.hvcgroep.nl/rest/adressen/{0}/kalender/{1}"
        ],
    "irado": [
        "https://www.irado.nl/bewoners/afvalkalender",
        "https://www.irado.nl/bewoners/afvalkalender"],
    "katwijk": ["https://afval.katwijk.nl/nc/afvalkalender/?tx_windwastecalendar_pi1%5Baction%5D=search"],
    "middendrenthe": [
        "https://www.middendrenthe.nl/website/!suite86.scherm0325?mPag=6523&mAlle=J",
        "https://www.middendrenthe.nl/website/!ctm_afval.Kalender"],
    "mijnafvalwijzer": ["https://www.mijnafvalwijzer.nl/nl/{0}/{1}/"],
    "peelenmaas": ["https://afvalkalender.peelenmaas.nl/adres/{0}:{1}"],
    "omrin": ["https://www.omrin.nl/bij-mij-thuis/afval-regelen/afvalkalender"],
    "purmerend": ["https://afvalkalender.purmerend.nl/adres/{0}:{1}"],
    "rd4": ["https://www.rd4info.nl/NSI/Burger/Aspx/afvalkalender_public_text.aspx?pc={0}&nr={1}&t="],
    "rmn": ["https://inzamelschema.rmn.nl/adres/{0}:{1}"],
    "rova": ["http://afvalkalender.rova.nl/nl/{0}/{1}/"],
    "schouwenduiveland": ["https://afvalkalender.schouwen-duiveland.nl/adres/{0}:{1}"],
    "sliedrecht": ["https://sliedrecht.afvalinfo.nl/adres/{0}:{1}"],
    "spaarnelanden": ["https://afvalwijzer.spaarnelanden.nl/adres/{0}:{1}"],
    "suez": ["https://inzamelwijzer.suez.nl/adres/{0}:{1}"],
    "uden": ["https://www.uden.nl/inwoners/afval/ophaaldagen-afval/{0}-{1}.html"],
    "veldhoven": ["https://www.veldhoven.nl/afvalkalender/{0}-{1}"],
    "venlo": ["https://www.venlo.nl/trash-removal-calendar/{0}/{1}"],
    "venray": ["https://afvalkalender.venray.nl/adres/{0}:{1}"],
    "waalre": [
        "https://afvalkalender.waalre.nl/rest/adressen/{0}-{1}",
        "https://afvalkalender.waalre.nl/rest/adressen/{0}/kalender/{1}"
    ],
    "westerkwartier": ["https://www.afvalalert.nl/kalender/{0}/{1}/?web=1"],
    "westerwolde": ["https://www.westerwolde.nl/trash-removal-calendar/{0}/{1}"],
    "westland": ["https://huisvuilkalender.gemeentewestland.nl/huisvuilkalender/Huisvuilkalender/get-huisvuilkalender-ajax"],
    "ximmio": [
        "https://wasteapi.ximmio.com/api/FetchAdress",
        "https://wasteapi.ximmio.com/api/GetCalendar"
    ],
    "zrd": ["https://afvalkalender.zrd.nl/adres/{0}:{1}"],
    "zuidwestfriesland": ["https://afvalkalender.sudwestfryslan.nl/adres/{0}:{1}"]
}

SENSOR_LOCATIONS_TO_COMPANY_CODE = {
    "acv": ["f8e2844a-095e-48f9-9f98-71fceb51d2c3"],
    "almere": ["53d8db94-7945-42fd-9742-9bbc71dbe4c1"],
    "area": ["adc418da-d19b-11e5-ab30-625662870761"],
    "bar": ["bb58e633-de14-4b2a-9941-5bc419f1c4b0"],
    "hellendoorn": ["24434f5b-7244-412b-9306-3a2bd1e22bc1"],
    "meerlanden": ["800bf8d7-6dd1-4490-ba9d-b419d6dc8a45"],
    "meppel": ["b7a594c7-2490-4413-88f9-94749a3ec62a"],
    #nissewaard also known as reinis
    "nissewaard": ["9dc25c8a-175a-4a41-b7a1-83f237a80b77"],
    "twentemilieu": ["8d97bb56-5afd-4cbc-a651-b4f7314264b4"],
    "vijfheerenlanden": ["942abcf6-3775-400d-ae5d-7380d728b23c"],
    "waardlanden": ["942abcf6-3775-400d-ae5d-7380d728b23c"]
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
SENSOR_PREFIX = "Afvalinfo "
ATTR_LAST_UPDATE = "last_update"
ATTR_HIDDEN = "hidden"
ATTR_IS_COLLECTION_DATE_TODAY = "is_collection_date_today"
ATTR_DAYS_UNTIL_COLLECTION_DATE = "days_until_collection_date"
ATTR_YEAR_MONTH_DAY_DATE = "year_month_day_date"

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)