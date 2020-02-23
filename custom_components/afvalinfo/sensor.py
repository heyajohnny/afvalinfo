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
Version: 0.1.6  20200214 - Bug fix for empty values in Westland
Version: 0.2.0  20200216 - Bug fix for multiple spaces in Westland (and all the other locations)
                           + extra attributes: Is collection today? and Days until collection
Version: 0.2.1  20200216 - Changed some attribute naming
Version: 0.2.2  20200218 - Added some locations for DeAfvalApp
Version: 0.2.3  20200219 - Refactor + added all the locations for DeAfvalApp
Version: 0.2.4  20200221 - Added locations for Westerkwartier
Version: 0.2.5  20200221 - Added locations for Rova
Version: 0.2.6  20200223 - Added Almere
ToDo: Merge / refactor all the Ximmio stuff and add hellendoorn and acv
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
    ATTR_DAYS_UNTIL_COLLECTION_DATE,
    ATTR_IS_COLLECTION_DATE_TODAY,
    SENSOR_TYPES,
)

from .location.sliedrecht import SliedrechtAfval
from .location.vijfheerenlanden import VijfheerenlandenAfval
from .location.deafvalapp import DeAfvalAppAfval
from .location.twentemilieu import TwentemilieuAfval
from .location.westerkwartier import WesterkwartierAfval
from .location.westland import WestlandAfval
from .location.rova import RovaAfval
from .location.almere import AlmereAfval

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

    city = config.get(CONF_CITY).lower().strip()
    postcode = config.get(CONF_POSTCODE).strip()
    street_number = config.get(CONF_STREET_NUMBER)
    date_format = config.get(CONF_DATE_FORMAT).strip()
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

        almere = ["almere"]
        if self.city in almere:
            self.data = AlmereAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        deafvalapp = ["aalst", "alem", "alphen", "altforst", "ammerzoden", "appeltern", "asperen", "asch", "axel", "beers", "beneden-leeuwen", "beugen", "beusichem", "biervliet", "boekel", "boven-leeuwen", "boxmeer", "brakel", "bruchem", "buren", "buurmalsen", "cuijk",
        "culemborg", "delwijnen", "dieteren", "dodewaard", "dreumel", "echt", "echteld", "eck en wiel", "erichem", "est", "gameren", "geldermalsen", "grave", "groeningen", "haaften", "haps", "hedel", "heerewaarden", "heesselt", "hellouw", "helmond", "herwijnen", "heukelem",
        "hoek", "hoenzadriel", "holthees", "hurwenen", "ijzendoorn", "ingen", "kapel-avezaath", "katwijk", "kerk-avezaath", "kerkdriel", "kerkwijk", "koewacht", "koningsbosch", "landhorst", "langenboom", "ledeacker", "lienden", "linden", "maasbommel", "maashees", "maria hoop",
        "maurik", "mill", "nederhemert-noord", "nederhemert-zuid", "neerijnen", "nieuwaal", "nieuwstadt", "ochten", "oeffelt", "ommeren", "ophemert", "opheusden", "opijnen", "oploo", "overloon", "overslag", "pey", "philippine", "poederoijen", "ravenswaaij", "rijkevoort", "rijswijk",
        "roosteren", "rossum", "sambeek", "sas van gent", "sint agatha", "sint anthonis", "sint hubert", "sint joost", "sluiskil", "son en breugel", "spijk", "spui", "stevensbeek", "susteren", "terneuzen", "tiel", "tuil", "varik", "velddriel", "vierlingsbeek", "vortum-mullem",
        "vuren", "waardenburg", "wadenoijen", "wamel", "wanroij", "well", "wellseind", "westerbeek", "westdorpe", "wilbertoord", "zaamslag", "zaltbommel", "zoelen", "zoelmond", "zuiddorpe", "zuilichem"]
        if self.city in deafvalapp:
            self.data = DeAfvalAppAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        rova = ["aalten", "agelo", "albergen", "amersfoort", "ane", "anerveen", "anevelde", "ankum", "archem en nieuwebrug", "arrien", "arrierveld", "baarlo", "baars", "balkbrug", "barlo", "barsbeek", "basse", "basserveld", "beekdorp", "beerze", "beerzerveld", "belt-schutsloot",
        "bergentheim", "berghum", "besthmen", "blankenham", "blauwe hand", "blokzijl", "boschoord", "bredevoort", "breklenkamp", "brinkheurne", "broekhuizen", "broekland", "brucht", "bruchterveld", "bruinehaar", "bunschoten-spakenburg", "collendoorn", "corle", "dale", "dalfsen",
        "dalfserveld", "dalmsholte", "dalmsholte", "darp", "de bult", "de heurne", "de klosse", "de kolk", "de krim", "de leijen", "de lichtmis", "de marshoek", "de meele", "de pol", "de pollen", "dedemsvaart", "den ham", "den hulst", "den velde", "denekamp", "deurningen", "diever",
        "dieverbrug", "diffelen", "dinxperlo", "dinxterveen", "doldersum", "doosje", "dulder", "dwarsgracht", "dwingeloo", "eefsele", "eemdijk", "eemster", "eerde", "eesveen", "emsland", "engeland", "fleringen", "frederiksoord", "gammelke", "geerdijk", "geesteren", "geeuwenbrug",
        "genemuiden", "gerner", "giethmen", "giethoorn", "gramsbergen", "groenlo", "haarle", "haart heurne", "halfweg", "hamingen", "harbrinkhoek", "hardenberg", "harreveld", "hasselt", "havelte", "havelterberg", "heemserveen", "heerde", "heeten", "heetveld", "heino", "henxel",
        "hessum", "het stift", "hezingen", "holt", "holtheme", "holthone", "hoogengraven en stegeren", "hoogenweg", "hoonhorst", "huppel", "ijhorst", "ijsselham", "ijzerlo", "jonen", "junne", "kadoelen", "kalenberg", "kallenkote", "kloosterhaar", "kloosterhaar", "kluinhaar",
        "kotten", "kuinre", "laag zuthem", "langeveen", "lankhorst", "lattrop-breklenkamp", "leeuwte", "leggeloo", "lemele", "lemelerveld", "lemselo", "lenthe", "leusenerveld", "lhee", "lheebroek", "lichtenvoorde", "lierderholthuis", "lievelde", "lintelo", "loozen", "lutten",
        "luttenberg", "mander", "manderveen", "mariaparochie", "marienberg", "marienheem", "marienvelde", "marijenkampen", "marle", "mastenbroek", "meddo", "millingen", "miste", "moespot", "molenhoek", "muggenbeet", "nederland", "nieuw heeten", "nieuwleusen", "nijensleek", "nijstad",
        "nutter", "oldemarkt", "olst", "ommen", "ommerkanaal en ommerbosch", "ommerschans", "ommerveld", "onna", "ootmarsum", "ossenzijl", "oud ootmarsum", "oudleusen", "oudleusenerveld", "paasloo", "punthorst", "raalte", "radewijk", "ratum", "rechteren", "reutum", "rheeze",
        "rheezerveen", "ronduite", "rossum", "rotbrink", "rouveen", "ruitenveen", "saasveld", "scheerwolde", "schuinesloot", "sibculo", "sibculo", "sint jansklooster", "slagharen", "slennebroek", "slingenberg", "staphorst", "steenwijk", "steenwijkerwold", "stegeren", "stegerveld",
        "strenkhaar", "t klooster", "tilligte", "tubbergen", "tuk", "uffelte", "urk", "varsen", "vasse", "venebrugge", "vilsteren", "vinkenbuurt", "vledder", "vledderveen", "vollenhove", "volthe", "vragender", "vriezenveen", "vroomshoop", "wanneperveen", "wapse", "wapserveen",
        "weerselo", "weitemanslanden", "welsum", "welsum", "wesepe", "westeinde", "westerhaar-vriezenveensewijk", "westerhoeven", "westerhuizingerveld", "wetering", "wijhe", "wilhelminaoord", "willemsoord", "winterswijk", "witharen", "witte paarden", "wittelte", "woold", "woudenberg",
        "zeesse", "zieuwent", "zorgvlied", "zuideinde", "zuidveen", "zwartsluis", "zwolle"]
        if self.city in rova:
            self.data = RovaAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        # try:
        sliedrecht = ["sliedrecht"]
        if self.city in sliedrecht:
            self.data = SliedrechtAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        twentemilieu = ["almelo", "borne", "enschede", "haaksbergen", "hengelo", "hof van twente", "losser", "oldenzaal", "wierden"]
        if self.city in twentemilieu:
            self.data = TwentemilieuAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        vijfheerenlanden = ["ameide", "everdingen", "hagestein", "hei- en boeicop", "hoef en haag", "kedichem", "leerbroek", "leerdam", "lexmond", "meerkerk", "nieuwland", "oosterwijk", "ossenwaard", "schoonrewoerd", "tienhoven aan de lek", "vianen", "zijderveld"]
        if self.city in vijfheerenlanden:
            self.data = VijfheerenlandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        westerkwartier = ["aduard", "boerakker", "briltil", "de wilp", "den ham", "den horn", "doezum", "enumatil", "ezinge,feerwerd", "garnwerd", "grijpskerk", "grootegast", "jonkersvaart", "kommerzijl", "kornhorn,lauwerzijl", "leek", "lettelbert", "lucaswolde", "lutjegast",
        "marum", "midwolde", "niebert", "niehove", "niekerk", "niezijl", "noordhorn", "noordwijk", "nuis", "oldehove", "oldekerk", "oostwold", "opende", "pieterzijl", "saaksum", "sebaldeburen", "tolbert", "visvliet", "zevenhuizen", "zuidhorn"]
        if self.city in westerkwartier:
            self.data = WesterkwartierAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        westland = ["de lier", "s-gravenzande", "honselersdijk", "kwintsheul", "maasdijk", "monster", "naaldwijk", "poeldijk", "ter heijde", "wateringen"]
        if self.city in westland:
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
        self._days_until_collection_date = None
        self._is_collection_date_today = False
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
        return {ATTR_LAST_UPDATE: self._last_update, ATTR_HIDDEN: self._hidden, ATTR_DAYS_UNTIL_COLLECTION_DATE: self._days_until_collection_date, ATTR_IS_COLLECTION_DATE_TODAY: self._is_collection_date_today}

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

                        # Is the collection date today?
                        self._is_collection_date_today = today == collection_date

                        # Days until collection date
                        delta = collection_date - today
                        self._days_until_collection_date = delta.days

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
