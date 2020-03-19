#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

ToDo: Add more locations for MijnAfvalWijzer
ToDo: Merge / refactor all the Ximmio stuff and add hellendoorn and acv
"""

import voluptuous as vol
from datetime import datetime, date, timedelta
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
from .location.venlo import VenloAfval
from .location.hvc import HvcAfval
from .location.alkmaar import AlkmaarAfval
from .location.alphenaandenrijn import AlphenAanDenRijnAfval
from .location.mijnafvalwijzer import MijnAfvalWijzerAfval
from .location.meppel import MeppelAfval
from .location.nissewaard import NissewaardAfval
from .location.meerlanden import MeerlandenAfval
from .location.suez import SuezAfval

from .sensortomorrow import AfvalInfoTomorrowSensor
from .sensortoday import AfvalInfoTodaySensor

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

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

        #if sensor_type not in SENSOR_TYPES:
        #    SENSOR_TYPES[sensor_type] = [sensor_type.title(), "", "mdi:recycle"]
        entities.append(AfvalinfoSensor(data, sensor_type, date_format, timespan_in_days))

        #Add sensor -trash_type_today
        if sensor_type.title() == "Trash_Type_Today":
            today = AfvalInfoTodaySensor(data, sensor_type, date_format, entities)
            entities.append(today)
        #Add sensor -trash_type_tomorrow
        if sensor_type.title() == "Trash_Type_Tomorrow":
            tomorrow = AfvalInfoTomorrowSensor(data, sensor_type, date_format, entities)
            entities.append(tomorrow)

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
        alkmaar = ["alkmaar", "driehuizen", "graft", "grootschermer", "koedijk", "markenbinnen", "noordeinde", "oost-graftdijk", "oterleek", "oudorp", "de rijp", "schermerhorn", "starnmeer", "stompetoren", "ursem", "west-graftdijk", "zuidschermer"]
        if self.city in alkmaar:
            self.data = AlkmaarAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        almere = ["almere"]
        if self.city in almere:
            self.data = AlmereAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        alphenaandenrijn = ["aarlanderveen", "alphen aan den rijn", "benthuizen", "boskoop", "hazerswoude-dorp", "hazerswoude-rijndijk", "koudekerk aan den rijn", "zwammerdam"]
        if self.city in alphenaandenrijn:
            self.data = AlphenAanDenRijnAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        deafvalapp = ["aalst", "alem", "alphen", "altforst", "ammerzoden", "appeltern", "asch", "asperen", "axel", "beers", "beneden-leeuwen", "beugen", "beusichem", "biervliet", "boekel", "boven-leeuwen", "boxmeer", "brakel", "bruchem", "buren", "buurmalsen", "cuijk", "culemborg", "delwijnen",
        "dieteren", "dodewaard", "dreumel", "echt", "echteld", "eck en wiel", "erichem", "est", "gameren", "geldermalsen", "grave", "groeningen", "haaften", "haps", "hedel", "heerewaarden", "heesselt", "hellouw", "helmond", "herwijnen", "heukelem", "hoek", "hoenzadriel", "holthees", "hurwenen",
        "ijzendoorn", "ingen", "kapel-avezaath", "katwijk", "kerk-avezaath", "kerkdriel", "kerkwijk", "koewacht", "koningsbosch", "landhorst", "langenboom", "ledeacker", "lienden", "linden", "maasbommel", "maashees", "maria hoop", "maurik", "mill", "nederhemert-noord", "nederhemert-zuid",
        "neerijnen", "nieuwaal", "nieuwstadt", "ochten", "oeffelt", "ommeren", "ophemert", "opheusden", "opijnen", "oploo", "overloon", "overslag", "pey", "philippine", "poederoijen", "ravenswaaij", "rijkevoort", "rijswijk", "roosteren", "rossum", "sambeek", "sas van gent", "sint agatha",
        "sint anthonis", "sint hubert", "sint joost", "sluiskil", "son en breugel", "spijk", "spui", "stevensbeek", "susteren", "terneuzen", "tiel", "tuil", "varik", "velddriel", "vierlingsbeek", "vortum-mullem", "vuren", "waardenburg", "wadenoijen", "wamel", "wanroij", "well", "wellseind",
        "westdorpe", "westerbeek", "wilbertoord", "zaamslag", "zaltbommel", "zoelen", "zoelmond", "zuiddorpe", "zuilichem"]
        if self.city in deafvalapp:
            self.data = DeAfvalAppAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        hvc = ["aagtdorp", "aartswoud", "abbekerk", "abbekerkeweere", "abbestede", "alblasserdam", "andijk", "anna paulowna", "assendelft", "avendorp", "avenhorn", "baarsdorpermeer", "bangert", "bant", "barsingerhorn", "bartelsluis", "bennemeer", "benningbroek", "bergen", "bergen aan zee",
        "bergermeer", "berkhout", "berkmeer", "beverwijk", "binnenwijzend", "bliekenbos", "blokdijk", "blokhuizen", "blokker", "bobeldijk", "bovenkarspel", "breezand", "bregtdorp", "broekerhaven", "broerdijk", "burgerbrug", "burgervlotbrug", "burghorn", "callantsoog", "camperduin", "catrijp",
        "cornelissenwerf", "creil", "dam", "de bangert", "de banne", "de belt", "de bomen", "de buurt", "de buurt", "de dijken", "de elft", "de gest", "de goorn", "de hale", "de haukes", "de heid", "de hoelm", "de hout", "de hulk", "de kaag", "de kampen", "de kolk", "de leijen", "de normer",
        "de snip", "de stolpen", "de strook", "de weed", "de weel", "de weere", "den helder", "den oever", "dijkstaal", "dirkshorn", "dordrecht", "driehuis", "duyncroft", "eenigenburg", "egmond aan den hoef", "egmond aan zee", "egmond-binnen", "egmondermeer", "emaus", "emmeloord", "engewormer",
        "enkhuizen", "ens", "espel", "gelderse buurt", "gouwe", "groenveld", "groet", "groetpolder", "groote keeten", "grootebroek", "grootven", "grosthuizen", "grotewal", "hanedoes", "harderwijk", "hargen", "hargen aan zee", "haringhuizen", "hauwert", "heemskerk", "hem", "hemkewerf",
        "hendrik-ido-ambacht", "hensbroek", "het hoogeland", "het korfwater", "het woud", "hippolytushoef", "hogebieren", "hollebalg", "hoogkarspel", "hoogwoud", "hoorn", "horn", "huiskebuurt", "ijmuiden", "jisp", "kalverdijk", "kathoek", "keinse", "keinsmerbrug", "kerkbuurt", "kerkbuurt",
        "kleine sluis", "kolhorn", "koog aan de zaan", "koppershorn", "kraaienburg", "krabbendam", "kraggenburg", "kreil", "kreileroord", "krommenie", "lagedijk", "lagehoek", "lambertschaag", "langereis", "leekerweg", "leihoek", "lekermeer", "lelystad", "lutjebroek", "lutjekolhorn", "lutjewinkel",
        "luttelgeest", "marknesse", "medemblik", "mennonietenbuurt", "middenmeer", "midwoud", "mientbrug", "moerbeek", "munnickaij", "munnikij", "nagele", "neck", "nes", "nibbixwoud", "nieuwe niedorp", "nieuwesluis", "noord-spierdijk", "noord-stroe", "noordburen", "noorddijk", "noorderbuurt",
        "noordermeer", "obdam", "obdammerdijk", "onderdijk", "oosteinde", "oosterblokker", "oostergouw", "oosterklief", "oosterland", "oosterleek", "oosterwijzend", "oostknollendam", "oostmijzen", "oostwoud", "opmeer", "opperdoes", "oude niedorp", "oudendijk", "oudesluis", "oudijk", "papendrecht",
        "paradijs", "petten", "poolland", "rinnegom", "rustenburg", "rutten", "santpoort-noord", "santpoort-zuid", "schagen", "schagerbrug", "schagerwaard", "scharwoude", "schellinkhout", "schokland", "schoorl", "schoorl aan zee", "schoorldam", "sijbekarspel", "sint maarten", "sint maartensbrug",
        "sint maartensvlotbrug", "sint maartenszee", "slootdorp", "slootgaard", "smerp", "spaarndammerpolder", "spanbroek", "spierdijk", "spijkerboor", "spoorbuurt", "stolpervlotbrug", "stroe", "stroet", "t buurtje", "t rijpje", "t slot", "t veld", "t wad", "t westeinde", "t zand", "terdiek", "tersluis",
        "tin", "tjallewal", "tolke", "tollebeek", "tuitjenhorn", "twisk", "ursem", "valkkoog", "van ewijcksluis", "vatrop", "veldhuis", "velsen-noord", "velsen-zuid", "velserbroek", "venhuizen", "vennik", "verlaat", "waarland", "wadway", "wadway", "warmenhuizen", "wateringskant", "wervershoof",
        "westeinde", "westerbuurt", "westerklief", "westerland", "westerwijzend", "westknollendam", "westwoud", "westzaan", "wieringerwaard", "wieringerwerf", "wijdenes", "wijdewormer", "wijmers", "wijzend", "wimmenum", "winkel", "wogmeer", "wognum", "wormer", "wormerveer", "woudmeer", "zaandam",
        "zaandijk", "zandburen", "zandwerven", "zanegeest", "zeewolde", "zijbelhuizen", "zijdewind", "zijpersluis", "zittend", "zomerdijk", "zuid-spierdijk", "zuidermeer", "zwaag", "zwaagdijk-oost", "zwaagdijk-west", "zwijndrecht"]
        if self.city in hvc:
            self.data = HvcAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        meerlanden = ["aalsmeer", "aalsmeerderbrug", "abbenes", "aerdenhout", "badhoevedorp", "beinsdorp", "bennebroek", "bentveld", "bloemendaal aan zee", "bloemendaal", "boesingheliede", "buitenkaag", "burgerveen", "cruquius", "de klei", "de zilk", "diemen", "haarlemmerliede", "halfweg", "heemstede",
        "hillegom", "hoofddorp", "kudelstaart", "langevelderslag", "leimuiderbrug", "lijnden", "lisse", "lisserbroek", "nieuw-vennep", "nieuwe meer", "nieuwebrug", "noordwijk aan zee", "noordwijk-binnen", "noordwijkerhout", "oud-diemen", "oude meer", "over-diemen", "overveen", "rijsenhout", "rozenburg",
        "schiphol", "schiphol-rijk", "spaarndam", "stammerdijk", "vijfhuizen", "vogelenzang", "vrouwentroost", "weteringbrug", "zwaanshoek", "zwanenburg"]
        if self.city in meerlanden:
            self.data = MeerlandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        meppel = ["broekhuizen", "de schiphorst", "havelterberg", "kolderveen", "kolderveense bovenboer", "meppel", "nijentap", "nijeveen", "nijeveense bovenboer", "rogat"]
        if self.city in meppel:
            self.data = MeppelAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        mijnafvalwijzer = ["almkerk", "andel", "babylonienbroek", "broekhorn", "de meern", "de noord", "draai", "drongelen", "dussen", "eethen", "frik", "genderen", "giessen", "haarzuilens", "hank", "heerhugowaard", "kabel", "meeuwen", "nieuwendijk", "oudendijk", "pannekeet", "rijswijk", "sleeuwijk", "t kruis",
        "uitwijk", "uppel", "utrecht", "veen", "veenhuizen", "verlaat", "vleuten", "waardhuizen", "werkendam", "wijk en aalburg", "woudrichem"]
        if self.city in mijnafvalwijzer:
            self.data = MijnAfvalWijzerAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        nissewaard = ["abbenbroek", "beerenplaat", "biert", "geervliet", "heenvliet", "hekelingen", "simonshaven", "spijkenisse", "tweede vlotbrug", "zuidland"]
        if self.city in nissewaard:
            self.data = NissewaardAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        rova = ["aalten", "agelo", "albergen", "amersfoort", "ane", "anerveen", "anevelde", "ankum", "archem en nieuwebrug", "arrien", "arrierveld", "baarlo", "baars", "balkbrug", "barlo", "barsbeek", "basse", "basserveld", "beekdorp", "beerze", "beerzerveld", "belt-schutsloot", "bergentheim",
        "berghum", "besthmen", "blankenham", "blauwe hand", "blokzijl", "boschoord", "bredevoort", "breklenkamp", "brinkheurne", "broekhuizen", "broekland", "brucht", "bruchterveld", "bruinehaar", "bunschoten-spakenburg", "collendoorn", "corle", "dale", "dalfsen", "dalfserveld", "dalmsholte",
        "darp", "de bult", "de heurne", "de klosse", "de kolk", "de krim", "de leijen", "de lichtmis", "de marshoek", "de meele", "de pol", "de pollen", "dedemsvaart", "den ham", "den hulst", "den velde", "denekamp", "deurningen", "diever", "dieverbrug", "diffelen", "dinxperlo", "dinxterveen",
        "doldersum", "doosje", "dulder", "dwarsgracht", "dwingeloo", "eefsele", "eemdijk", "eemster", "eerde", "eesveen", "emsland", "engeland", "fleringen", "frederiksoord", "gammelke", "geerdijk", "geesteren", "geeuwenbrug", "genemuiden", "gerner", "giethmen", "giethoorn", "gramsbergen",
        "groenlo", "haarle", "haart heurne", "halfweg", "hamingen", "harbrinkhoek", "hardenberg", "harreveld", "hasselt", "havelte", "havelterberg", "heemserveen", "heerde", "heeten", "heetveld", "heino", "henxel", "hessum", "het stift", "hezingen", "holt", "holtheme", "holthone",
        "hoogengraven en stegeren", "hoogenweg", "hoonhorst", "huppel", "ijhorst", "ijsselham", "ijzerlo", "jonen", "junne", "kadoelen", "kalenberg", "kallenkote", "kloosterhaar", "kluinhaar", "kotten", "kuinre", "laag zuthem", "langeveen", "lankhorst", "lattrop-breklenkamp", "leeuwte",
        "leggeloo", "lemele", "lemelerveld", "lemselo", "lenthe", "leusenerveld", "lhee", "lheebroek", "lichtenvoorde", "lierderholthuis", "lievelde", "lintelo", "loozen", "lutten", "luttenberg", "mander", "manderveen", "mariaparochie", "marienberg", "marienheem", "marienvelde",
        "marijenkampen", "marle", "mastenbroek", "meddo", "millingen", "miste", "moespot", "molenhoek", "muggenbeet", "nederland", "nieuw heeten", "nieuwleusen", "nijensleek", "nijstad", "nutter", "oldemarkt", "olst", "ommen", "ommerkanaal en ommerbosch", "ommerschans", "ommerveld", "onna",
        "ootmarsum", "ossenzijl", "oud ootmarsum", "oudleusen", "oudleusenerveld", "paasloo", "punthorst", "raalte", "radewijk", "ratum", "rechteren", "reutum", "rheeze", "rheezerveen", "ronduite", "rossum", "rotbrink", "rouveen", "ruitenveen", "saasveld", "scheerwolde", "schuinesloot",
        "sibculo", "sint jansklooster", "slagharen", "slennebroek", "slingenberg", "staphorst", "steenwijk", "steenwijkerwold", "stegeren", "stegerveld", "strenkhaar", "t klooster", "tilligte", "tubbergen", "tuk", "uffelte", "urk", "varsen", "vasse", "venebrugge", "vilsteren", "vinkenbuurt",
        "vledder", "vledderveen", "vollenhove", "volthe", "vragender", "vriezenveen", "vroomshoop", "wanneperveen", "wapse", "wapserveen", "weerselo", "weitemanslanden", "welsum", "wesepe", "westeinde", "westerhaar-vriezenveensewijk", "westerhoeven", "westerhuizingerveld", "wetering", "wijhe",
        "wilhelminaoord", "willemsoord", "winterswijk", "witharen", "witte paarden", "wittelte", "woold", "woudenberg", "zeesse", "zieuwent", "zorgvlied", "zuideinde", "zuidveen", "zwartsluis", "zwolle"]
        if self.city in rova:
            self.data = RovaAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        sliedrecht = ["sliedrecht"]
        if self.city in sliedrecht:
            self.data = SliedrechtAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        suez = ["arnhem", "de praets", "deelen", "elden", "schaarsbergen", "t vlot", "terlet"]
        if self.city in suez:
            self.data = SuezAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        twentemilieu = ["almelo", "borne", "enschede", "haaksbergen", "hengelo", "hof van twente", "losser", "oldenzaal", "wierden"]
        if self.city in twentemilieu:
            self.data = TwentemilieuAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        venlo = ["arcen", "belfeld", "lomm", "steyl", "tegelen", "velden", "venlo"]
        if self.city in venlo:
            self.data = VenloAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        vijfheerenlanden = ["ameide", "everdingen", "hagestein", "hei- en boeicop", "hoef en haag", "kedichem", "leerbroek", "leerdam", "lexmond", "meerkerk", "nieuwland", "oosterwijk", "ossenwaard", "schoonrewoerd", "tienhoven aan de lek", "vianen", "zijderveld"]
        if self.city in vijfheerenlanden:
            self.data = VijfheerenlandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        westerkwartier = ["aduard", "boerakker", "briltil", "de wilp", "den ham_" "den horn", "doezum", "enumatil", "ezinge", "feerwerd", "garnwerd", "grijpskerk", "grootegast", "jonkersvaart", "kommerzijl", "kornhorn", "lauwerzijl", "leek", "lettelbert",
        "lucaswolde", "lutjegast", "marum", "midwolde", "niebert", "niehove", "niekerk", "niezijl", "noordhorn", "noordwijk", "nuis", "oldehove", "oldekerk", "oostwold", "opende", "pieterzijl", "saaksum", "sebaldeburen", "tolbert", "visvliet", "zevenhuizen", "zuidhorn"]
        if self.city in westerkwartier:
            self.data = WesterkwartierAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        westland = ["de lier", "honselersdijk", "kwintsheul", "maasdijk", "monster", "naaldwijk", "poeldijk", "s-gravenzande", "ter heijde", "wateringen"]
        if self.city in westland:
            self.data = WestlandAfval().get_data(
                self.city, self.postcode, self.street_number
            )

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

    def update(self):
        self.data.update()
        waste_data = self.data.data

        try:
            if waste_data:
                if self.type in waste_data:
                    collection_date = datetime.strptime(
                        waste_data[self.type], "%Y-%m-%d"
                    ).date()

                    if collection_date:
                        # Set the values of the sensor
                        self._last_update = date.today().strftime("%d-%m-%Y %H:%M")

                        # Is the collection date today?
                        self._is_collection_date_today = date.today() == collection_date

                        # Days until collection date
                        delta = collection_date - date.today()
                        self._days_until_collection_date = delta.days

                        # Only show the value if the date is lesser than or equal to (today + timespan_in_days)
                        if collection_date <= date.today() + relativedelta(days=int(self.timespan_in_days)):
                            self._state = collection_date.strftime(self.date_format)
                        else:
                            self._hidden = True
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
            else:
                raise ValueError()
        except ValueError:
            self._state = None
            self._hidden = True
            self._days_until_collection_date = None
            self._is_collection_date_today = False
            self._last_update = date.today().strftime("%d-%m-%Y %H:%M")
