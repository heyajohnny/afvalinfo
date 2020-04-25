#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

ToDo: Add more locations for MijnAfvalWijzer
Leudal,
Leusden,
Loon op Zand,
Lopik,
Maasgouw,
Meierijstad,
Moerdijk,
Nijkerk,
Noordenveld,
Nunspeet,
Oldambt,
Oldebroek,
Oosterhout,
Oss,
Oude-IJsselstreek,
Oude Pekela,
Oudewater,
Overbetuwe,
Rhenen,
Rijssen-Holten,
Roerdalen,
Roosendaal,
Rucphen,
Scherpenzeel,
Sint-Michielsgestel,
Sittard-Geleen,
Smallingerland,
Stadskanaal,
Stein,
Stichtse Vecht,
Teylingen,
Tilburg,
Tynaarlo,
Uitgeest,
Utrechtse Heuvelrug,
Veendam,
Waalwijk,
Waterland,
Wijk bij Duurstede,
Westervoort,
Westvoorne,
Woensdrecht,
Woerden,
Zoetermeer,
Zoeterwoude
ToDo: Merge / refactor all the Ximmio stuff and add hellendoorn and acv
ToDo: Add huisnummer toevoeging
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
from .location.omrin import OmrinAfval
from .location.defriesemeren import DeFrieseMerenAfval
from .location.veldhoven import VeldhovenAfval
from .location.venray import VenrayAfval
from .location.gad import GadAfval
from .location.zuidwestfriesland import ZuidWestFrieslandAfval
from .location.blink import BlinkAfval
from .location.bar import BarAfval
from .location.spaarnelanden import SpaarnelandenAfval
from .location.cyclus import CyclusAfval

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
        if sensor_type.title().lower() != "trash_type_today" and sensor_type.title().lower() != "trash_type_tomorrow":
            entities.append(AfvalinfoSensor(data, sensor_type, date_format, timespan_in_days))

        #Add sensor -trash_type_today
        if sensor_type.title().lower() == "trash_type_today":
            today = AfvalInfoTodaySensor(data, sensor_type, date_format, entities)
            entities.append(today)
        #Add sensor -trash_type_tomorrow
        if sensor_type.title().lower() == "trash_type_tomorrow":
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
        bar = ["barendrecht", "bolnes", "oostendam", "poortugaal", "rhoon", "ridderkerk"]
        if self.city in bar:
            self.data = BarAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        blink = ["aarle-rixtel", "asten", "bakel", "beek en donk", "de mortel", "de rips", "deurne", "elsendorp", "gemert", "gerwen", "handel", "heeze", "helenaveen", "helmond", "heusden", "leende", "lierop", "lieshout", "liessel", "mariahout", "milheeze", "nederwetten", "neerkant", "nuenen",
        "ommel", "someren", "sterksel", "vlierden"]
        if self.city in blink:
            self.data = BlinkAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        cyclus = ["ammerstol", "bergambacht", "berkenwoude", "bodegraven", "de meije", "driebruggen", "gouda", "gouderak", "haastrecht", "hogebrug", "hoogmade", "kaag", "krimpen aan de lek", "lageweg", "langeraar", "leimuiden", "lekkerkerk", "linschoten", "moerkapelle", "montfoort",
        "moordrecht", "nieuwe wetering", "nieuwerbrug", "nieuwerkerk aan den ijssel", "nieuwkoop", "nieuwveen", "noordeinde", "noorden", "opperduit", "oud ade", "oude wetering", "ouderkerk aan den ijssel", "reeuwijk-brug", "reeuwijk-dorp", "rijnsaterwoude", "rijpwetering", "roelofarendsveen",
        "schoonhoven", "schuwacht", "sluipwijk", "stolwijk", "tempel", "ter aar", "vlist", "waarde", "waddinxveen", "willeskop", "willige langerak", "woerdense verlaat", "woubrugge", "zevenhoven", "zevenhuizen"]
        if self.city in cyclus:
            self.data = CyclusAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        deafvalapp = ["aalst", "acquoy", "alem", "alphen", "altforst", "ammerzoden", "appeltern", "asch", "asperen", "axel", "beers", "beesd", "beneden-leeuwen", "beugen", "beusichem", "biervliet", "boekel", "boven-leeuwen", "boxmeer", "brakel", "breugel", "bruchem", "buren", "buurmalsen",
        "buurmalsen", "cuijk", "culemborg", "deil", "delwijnen", "dieteren", "dodewaard", "dreumel", "echt", "echteld", "eck en wiel", "enspijk", "erichem", "escharen", "est", "gameren", "gassel", "geldermalsen", "gellicum", "grave", "groeningen", "haaften", "haps", "hedel", "heerewaarden",
        "heesselt", "hellouw", "helmond", "herwijnen", "heukelum", "hoek", "hoenzadriel", "holthees", "huize padua", "hurwenen", "ijzendoorn", "ingen", "kapel-avezaath", "katwijk", "kerk-avezaath", "kerkdriel", "kerkwijk", "kesteren", "koewacht", "koningsbosch", "landhorst", "langenboom",
        "ledeacker", "lienden", "linden", "maasbommel", "maashees", "maria hoop", "maurik", "meteren", "mill", "nederhemert-noord", "nederhemert-zuid", "neerijnen", "nieuwaal", "nieuwstadt", "ochten", "oeffelt", "ommeren", "ophemert", "opheusden", "opijnen", "oploo", "overloon", "overslag",
        "pey", "philippine", "poederoijen", "ravenswaaij", "rhenoy", "rijkevoort", "rijswijk", "roosteren", "rossum", "rumpt", "sambeek", "sas van gent", "sint agatha", "sint anthonis", "sint hubert", "sint joost", "sluiskil", "son", "spijk", "spui", "stevensbeek", "susteren", "terneuzen",
        "tiel", "tricht", "tuil", "varik", "velddriel", "velp", "venhorst", "vierlingsbeek", "vortum-mullem", "vuren", "waardenburg", "wamel", "wanroij", "well", "wellseind", "westdorpe", "westerbeek", "wilbertoord", "zaamslag", "zaltbommel", "zennewijnen", "zoelen", "zoelmond",
        "zuiddorpe", "zuilichem"]
        if self.city in deafvalapp:
            self.data = DeAfvalAppAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        defriesemeren = ["akmarijp", "bakhuizen", "balk", "ballingbuur", "bantega", "bargebek", "boornzwaag", "boornzwaag over de wielen", "brekkenpolder", "broek", "commissiepolle", "de bels", "de polle", "de rijlst", "delburen", "delfstrahuizen", "dijken", "doniaga", "echten", "echtenerbrug",
        "eesterga", "elahuizen", "finkeburen", "follega", "goingarijp", "harich", "haskerhorne", "heide", "hooibergen", "huisterheide", "idskenhuizen", "joure", "kolderwolde", "langweer", "legemeer", "lemmer", "marderhoek", "mirns", "nieuw amerika", "nijehaske", "nijemirdum", "noed", "oldeouwer",
        "onland", "oosterzee", "oudega", "oudehaske", "oudemirdum", "ouwster-nijega", "ouwsterhaule", "rijs", "rohel", "rotstergaast", "rotsterhaule", "rottum", "ruigahuizen", "scharsterbrug", "schoterzijl", "schouw", "sint nicolaasga", "sintjohannesga", "sloten", "snikzwaag", "sondel", "spannenburg",
        "tacozijl", "terhorne", "terkaple", "teroele", "tjerkgaast", "trophorne", "vegelinsoord", "vierhuis", "vinkeburen", "vrisburen", "westend", "westerend-harich", "wijckel", "zevenbuurt"]
        if self.city in defriesemeren:
            self.data = DeFrieseMerenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        gad = ["hilversum"]
        if self.city in gad:
            self.data = GadAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        hvc = ["aagtdorp", "aartswoud", "abbekerk", "abbestede", "alblasserdam", "andijk", "anna paulowna", "assendelft", "bant", "barsingerhorn", "benningbroek", "bergen aan zee", "beverwijk", "blokdijk", "blokker", "bovenkarspel", "breezand", "bregtdorp", "burgerbrug", "burgervlotbrug", "callantsoog",
        "camperduin", "catrijp", "creil", "de buurt", "de haukes", "de stolpen", "de strook", "de weere", "den helder", "den oever", "dirkshorn", "dordrecht", "driehuis", "eenigenburg", "egmond aan den hoef", "egmond aan zee", "egmond-binnen", "emmeloord", "enkhuizen", "ens", "espel", "gouwe", "groenveld",
        "groet", "groote keeten", "grootebroek", "hargen", "haringhuizen", "hauwert", "heemskerk", "heerjansdam", "hem", "hendrik-ido-ambacht", "hippolytushoef", "hoogkarspel", "hoogwoud", "hoorn", "huisduinen", "ijmuiden", "julianadorp", "kalverdijk", "keinse", "kleine sluis", "kleine-lindt", "kolhorn",
        "koog aan de zaan", "krabbendam", "kraggenburg", "kreil", "kreileroord", "krommenie", "lambertschaag", "lelystad", "lutjebroek", "lutjewinkel", "luttelgeest", "marknesse", "medemblik", "middenmeer", "midwoud", "moerbeek", "nagele", "nibbixwoud", "nieuwe niedorp", "nieuwesluis", "onderdijk",
        "oosterblokker", "oosterdijk", "oosterklief", "oosterland", "oosterleek", "oostwoud", "opmeer", "opperdoes", "oude niedorp", "oudesluis", "papendrecht", "petten", "rinnegom", "rutten", "santpoort-noord", "santpoort-zuid", "schagen", "schagerbrug", "schellinkhout", "schokland", "schoorl",
        "schoorldam", "schoorldam", "sijbekarspel", "sint maarten", "sint maartensbrug", "sint maartensvlotbrug", "sint maartenszee", "slootdorp", "smerp", "spaarndammerpolder", "spanbroek", "stroe", "stroet", "t rijpje", "t veld", "t zand", "terdiek", "tjallewal", "tolke", "tolke", "tollebeek",
        "tuitjenhorn", "twisk", "valkkoog", "van ewijcksluis", "vatrop", "velsen", "velsen-noord", "velsen-zuid", "velserbroek", "venhuizen", "verlaat", "waarland", "wadway", "wadway", "warmenhuizen", "wervershoof", "westerklief", "westerland", "westknollendam", "westwoud", "westzaan", "wieringerwaard",
        "wieringerwerf", "wijdenes", "wijk aan duin", "wijk aan zee", "wimmenum", "winkel", "wognum", "wormerveer", "zaandam", "zaandijk", "zandwerven", "zijdewind", "zwaag", "zwaagdijk-oost", "zwaagdijk-west", "zwijndrecht"]
        if self.city in hvc:
            self.data = HvcAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        meerlanden = ["aalsmeer", "aalsmeerderbrug", "abbenes", "aerdenhout", "badhoevedorp", "beinsdorp", "bennebroek", "bentveld", "bloemendaal", "bloemendaal aan zee", "boesingheliede", "buitenkaag", "burgerveen", "cruquius", "de zilk", "diemen", "haarlemmerliede", "halfweg", "heemstede", "hillegom",
        "hoofddorp", "kudelstaart", "leimuiderbrug", "lijnden", "lisse", "lisserbroek", "nieuw-vennep", "noordwijk aan zee", "noordwijk-binnen", "noordwijkerhout", "oude meer", "overveen", "rijsenhout", "rozenburg", "schiphol", "schiphol-rijk", "spaarndam", "vijfhuizen", "vogelenzang", "weteringbrug",
        "zwaanshoek", "zwanenburg"]
        if self.city in meerlanden:
            self.data = MeerlandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        meppel = ["havelterberg", "kolderveen", "meppel", "nijeveen", "rogat"]
        if self.city in meppel:
            self.data = MeppelAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        mijnafvalwijzer = ["aarle", "abcoude", "achterveld", "aerdt", "akersloot", "almkerk", "alteveer", "amen", "america", "amstelhoek", "amstelveen", "amstenrade", "andel", "anderen", "angerlo", "anloo", "annen", "annerveenschekanaal", "anreep-schieven", "ansen", "assen", "baambrugge", "baarschot",
        "babberich", "babylonienbroek", "bahr", "bakkum", "bakkum-noord", "balloerveld", "balloo", "barneveld", "beek", "beesel", "bergen op zoom", "berghuizen", "bergschenhoek", "berkel en rodenrijs", "best", "bevermeer", "biddinghuizen", "biest-houtakker", "bilthoven", "bingelrade", "bingerden",
        "bleiswijk", "borger", "bosschenhoofd", "boxtel", "breda", "brielle", "broekhorn", "broekhuizen", "broekhuizenvorst", "bronneger", "bronnegerveen", "buinen", "buinerveen", "castricum aan zee", "castricum", "de beek", "de bilt", "de glind", "de hoef", "de meern", "de noord", "de steeg", "de vleut",
        "de vorst", "de wijk", "de woude", "den berg", "deurze", "dieren", "diessen", "doenrade", "doetinchem", "dongen", "dongense vaart", "doornspijk", "draai", "drie", "drogteropslagen", "drongelen", "dronten", "drouwen", "drouwenermond", "drouwenerveen", "duiven", "dusseldorp", "dussen", "echten",
        "eerste exloermond", "ees", "eesergroen", "eeserveen", "eethen", "eext", "eexterveen", "eexterveenschekanaal", "eexterzandvoort", "ekehaar", "elburg", "eldersloo", "eleveld", "ellecom", "ellertshaar", "ermelo", "esbeek", "etten-leur", "eursinge", "evertsoord", "exloo", "exloërveen", "fort",
        "foxhol", "froombosch", "gaanderen", "garderen", "gasselte", "gasselternijveen", "gasselternijveenschemond", "gasteren", "geelbroek", "geertruidenberg", "genderen", "genhout", "geverik", "giesbeek", "giessen", "gieten", "gieterveen", "gilze", "goirle", "grafhorst", "graswijk", "griendtsveen",
        "groenekan", "groessen", "grolloo", "grubbenvorst", "haarzuilens", "haghorst", "hank", "harderwijk", "harkstede", "heerhugowaard", "heesch", "heeswijk-dinther", "hegelsom", "heiloo", "hellum", "herwen", "hezelaar", "hierden", "hilvarenbeek", "hoeven", "hollandsche rading", "hoogezand", "horst",
        "houtdorp", "houten", "hulsberg", "hulten", "ijsselmuiden", "jabeek", "kampen", "kamperveen", "kasteren", "kelmond", "kerkenveld", "kiel-windeweer", "kinderbos", "klein-dongen", "klijndijk", "koekange", "koekangerveld", "kolham", "kootwijk", "kootwijkerbroek", "krimpen aan den ijssel", "kronenberg",
        "kropswolde", "kruisweg", "laag-soeren", "langenberg", "lathum", "leiden", "leiderdorp", "lennisheuvel", "leuvenum", "liempde", "limmen", "linde", "lobith", "loo", "looeind", "loon", "loosbroek", "lottum", "luddeweer", "luissel", "maartensdijk", "marwijksoord", "meeden", "meerlo", "meeuwen", "melderslo",
        "merkelbeek", "meterik", "mijdrecht", "molenschot", "muntendam", "neerbeek", "nergena", "nes aan de amstel", "nieuw annerveen", "nieuw-buinen", "nieuw-wehl", "nieuwediep", "nieuwendijk", "nijlande", "nistelrode", "nooitgedacht", "noordbroek", "nuth", "odoorn", "odoornerveen", "offenbeek", "oirsbeek",
        "oosteinde", "ooy", "oud annerveen", "oud gastel", "oud-zevenaar", "ouddorp", "oudenbosch", "overschild", "pannerden", "papenvoort", "puth", "raamsdonk", "raamsdonksveer", "reuver", "rheden", "rhee", "riel", "rijen", "rijkel", "rijswijk", "rodenrijs", "roermond", "rolde", "roond", "rotte", "rotterdam",
        "ruinen", "ruinerwold", "s gravenmoer", "s-gravenmoerse vaart", "s-heerenbroek", "sappemeer", "schalkwijk", "scharmer", "schildwolde", "schimmert", "schinnen", "schinveld", "schipborg", "schoonloo", "selissen", "sevenum", "siddeburen", "sleeuwijk", "slochteren", "spankeren", "spaubeek", "speuld", "spijk",
        "spijkerboor", "stampersgat", "staverden", "steendam", "stroe", "swalmen", "sweikhuizen", "swifterbant", "swolgen", "t goy", "t harde", "telgt", "ter aard", "terschuur", "tienray", "tjuchem", "tolkamer", "tongeren", "tonsel", "tripscompagnie", "tuindorp", "tull en t waal", "tweede exloermond",
        "tweede valthermond", "ubbena", "uitwijk", "uppel", "utrecht", "valthe", "valthermond", "veen", "veenhuizen", "veeningen", "velp", "verlaat", "vierpolders", "vinkel", "vinkeveen", "vleuten", "voorthuizen", "vorstenbosch", "vredenheim", "vrilkhoven", "waardhuizen", "waterhuizen", "waverveen", "wehl",
        "werkendam", "westbroek", "westdorp", "westerbroek", "wijk en aalburg", "wijnandsrade", "wijnbergen", "wilnis", "wilsum", "witten", "woudbloem", "woudrichem", "zalk", "zandberg", "zeijerveld", "zevenaar", "zuidbroek", "zuidwolde", "zwartebroek", "zwartewaal"]
        if self.city in mijnafvalwijzer:
            self.data = MijnAfvalWijzerAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        nissewaard = ["abbenbroek", "geervliet", "heenvliet", "hekelingen", "simonshaven", "spijkenisse", "zuidland"]
        if self.city in nissewaard:
            self.data = NissewaardAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        omrin = ["aalsum", "achlum", "aegum", "akkrum", "anjum", "appelscha", "augsbuurt", "augustinusga", "baaiduinen", "baard", "baijum", "bakkeveen", "ballum", "beers", "beetgum", "beetgumermolen", "beetsterzwaag", "bergum", "berlikum", "birdaard", "blesdijke", "blessum", "blija", "boelenslaan",
        "boer", "boijl", "boksum", "bontebok", "bornwird", "brantgum", "britsum", "buitenpost", "buren", "burum", "cornjum", "de blesse", "de hoeve", "de knijpe", "deinum", "dokkum", "dongjum", "donkerbroek", "drachten-azeven", "drogeham", "dronrijp", "ee", "eernewoude", "eestrum", "elsloo", "engelum",
        "engwierum", "ferwerd", "finkum", "firdgum", "fochteloo", "formerum", "foudgum", "franeker", "friens", "frieschepalen", "garijp", "genum", "gerkesklooster", "gersloot", "giekerk", "gorredijk", "goutum", "grouw", "hallum", "hantum", "hantumeruitburen", "hantumhuizen", "hardegarijp", "harkema",
        "harlingen", "haskerdijken", "haule", "haulerwijk", "hee", "heerenveen", "hempens	hempus", "hemrik", "herbaijum", "hiaure", "hijlaard", "hijum", "hitzum", "hogebeintum", "hollum", "holwerd", "hoorn", "hoornsterzwaag", "huins", "idaard", "irnsum", "janum", "jellum", "jelsum", "jislum",
        "jonkersland", "jorwerd", "jouswier", "jubbega", "kaard", "katlijk", "kinnum", "klooster-lidlum", "kollum", "kollumerpomp", "kollumerzwaag", "kootstertille", "landerum", "langedijke", "langelille", "langezwaag", "leeuwarden", "lekkum", "lichtaard", "lies", "lioessens", "lions", "lippenhuizen",
        "luinjeberd", "luxwoude", "makkinga", "mantgum", "marrum", "marssum", "menaldum", "metslawier", "midlum", "midsland", "miedum", "mildam", "minnertsga", "moddergat", "molenend", "morra", "munnekeburen", "munnekezijl", "nes", "niawier", "nieuwebrug", "nieuwehorne", "nieuweschoot", "nij altoenae",
        "nij beets", "nijeberkoop", "nijeholtpade", "nijeholtwolde", "nijelamer", "nijetrijne", "noordbergum", "noordwolde", "oenkerk", "oldeberkoop", "oldeboorn", "oldeholtpade", "oldeholtwolde", "oldelamer", "oldetrijne", "olterterp", "oosterbierum", "oosterend", "oosterlittens", "oostermeer",
        "oosternijkerk", "oosterstreek", "oosterwolde", "oostrum", "oranjewoud", "oude leije", "oudebildtzijl", "oudehorne", "oudeschoot", "oudkerk", "oudwoude", "paesens", "peins", "peperga", "pietersbierum", "raard", "ravenswoud", "reitsum", "ried", "rijperkerk", "roordahuizum", "schalsum",
        "scherpenzeel", "schingen", "sexbierum", "siegerswoude", "sint annaparochie", "sint jacobiparochie", "slappeterp", "slijkenburg", "snakkerburen", "sonnega", "spanga", "spannum", "steggerda", "stiens", "striep", "stroobos", "suameer", "suawoude", "surhuisterveen", "surhuizum", "swichum", "teerns",
        "ter idzard", "terband", "ternaard", "terwispel", "tietjerk", "tijnje", "tjalleberd", "triemen", "twijzel", "twijzelerheide", "tzum", "tzummarum", "ureterp", "veenklooster", "vinkega", "vrouwenparochie", "waaxens", "wanswerd", "warfstermolen", "warga", "warstiens", "wartena", "waskemeer", "weidum",
        "welsrijp", "west-terschelling", "westergeest", "westhoek", "wetsens", "wier", "wierum", "wijnaldum", "wijnjewoude", "wijns", "wijtgaard", "winsum", "wirdum", "wolvega", "zandhuizen", "zwagerbosch", "zweins"]
        if self.city in omrin:
            self.data = OmrinAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        rova = ["aalten", "agelo", "albergen", "amersfoort", "ane", "anerveen", "anevelde", "ankum", "arrien", "baarlo", "baars", "balkbrug", "basse", "beerze", "beerzerveld", "belt-schutsloot", "bergentheim", "blankenham", "blokzijl", "boschoord", "bredevoort", "broekland", "brucht", "bruchterveld",
        "bunschoten-spakenburg", "collendoorn", "dalfsen", "dalmsholte", "darp", "de bult", "de heurne", "de krim", "de pol", "dedemsvaart", "den ham", "den velde", "denekamp", "deurningen", "diever", "dieverbrug", "diffelen", "dinxperlo", "doldersum", "dwingeloo", "eemdijk", "eemster", "eesveen",
        "fleringen", "frederiksoord", "geerdijk", "geesteren", "geeuwenbrug", "genemuiden", "giethmen", "giethoorn", "gramsbergen", "groenlo", "haarle", "harbrinkhoek", "hardenberg", "harreveld", "hasselt", "hattem", "havelte", "havelterberg", "heemserveen", "heerde", "heeten", "heino", "hezingen", "holtheme",
        "holthone", "hoogenweg", "hoogland", "hooglanderveen", "hoonhorst", "ijhorst", "ijsselham", "kalenberg", "kallenkote", "kloosterhaar", "kuinre", "laag zuthem", "langeveen", "lattrop-breklenkamp", "leggeloo", "lemele", "lemelerveld", "lhee", "lheebroek", "lichtenvoorde", "lierderholthuis", "lievelde",
        "loozen", "lutten", "luttenberg", "mander", "manderveen", "mariaparochie", "marienvelde", "marijenkampen", "mariënberg", "mariënheem", "marle", "mastenbroek", "meddo", "nederland", "nieuw heeten", "nieuwleusen", "nijensleek", "nutter", "oldemarkt", "olst", "ommen", "onna", "ootmarsum", "ossenzijl",
        "oud ootmarsum", "oudleusen", "paasloo", "punthorst", "raalte", "radewijk", "reutum", "rheeze", "rheezerveen", "rossum", "rouveen", "saasveld", "scheerwolde", "schuinesloot", "sibculo", "sint jansklooster", "slagharen", "staphorst", "steenwijk", "steenwijkerwold", "stegeren", "tilligte", "tubbergen",
        "tuk", "uffelte", "urk", "vasse", "veessen", "venebrugge", "vilsteren", "vinkenbuurt", "vledder", "vledderveen", "vollenhove", "vorchten", "vragender", "vriezenveen", "vroomshoop", "wanneperveen", "wapenveld", "wapse", "wapserveen", "weerselo", "welsum", "wesepe", "westeinde", "westerhaar-vriezenveensewijk",
        "wetering", "wijhe", "wilhelminaoord", "willemsoord", "winterswijk", "witharen", "witte paarden", "wittelte", "woudenberg", "zieuwent", "zorgvlied", "zuidveen", "zwartsluis", "zwolle"]
        if self.city in rova:
            self.data = RovaAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        sliedrecht = ["sliedrecht"]
        if self.city in sliedrecht:
            self.data = SliedrechtAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        spaarnelanden = ["haarlem", "spaarndam-west", "zandvoort"]
        if self.city in spaarnelanden:
            self.data = SpaarnelandenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        suez = ["arnhem", "elden", "schaarsbergen"]
        if self.city in suez:
            self.data = SuezAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        twentemilieu = ["aadorp", "almelo", "ambt delden", "beckum", "bentelo", "beuningen", "boekelo", "borne", "bornerbroek", "buurse", "de lutte", "delden", "diepenheim", "enschede", "enter", "glane", "glanerbrug", "goor", "haaksbergen", "hengelo", "hengevelde",
        "hertme", "lonneker", "losser", "mariaparochie", "markelo", "oldenzaal", "overdinkel", "st. isidorushoeve", "usselo", "wierden", "zenderen"]
        if self.city in twentemilieu:
            self.data = TwentemilieuAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        veldhoven = ["veldhoven"]
        if self.city in veldhoven:
            self.data = VeldhovenAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        venlo = ["arcen", "belfeld", "lomm", "steyl", "tegelen", "velden", "venlo"]
        if self.city in venlo:
            self.data = VenloAfval().get_data(
                self.city, self.postcode, self.street_number
            )
        venray = ["blitterswijck", "castenray", "geijsteren", "heide", "leunen", "merselo", "oirlo", "oostrum", "smakt", "venray", "veulen", "vredepeel", "wanssum", "ysselsteyn"]
        if self.city in venray:
            self.data = VenrayAfval().get_data(
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
        zuidwestfriesland = ["abbega", "allingawier", "arum", "blauwhuis", "bolsward", "bozum", "breezanddijk", "britswerd", "burgwerd", "cornwerd", "dedgum", "deersum", "edens", "exmorra", "ferwoude", "folsgare", "gaast", "gaastmeer", "gauw", "goënga", "greonterp",
        "hartwerd", "heeg", "hemelum", "hennaard", "hichtum", "hidaard", "hieslum", "hindeloopen", "hommerts", "idsegahuizum", "idzega", "ijlst", "ijsbrechtum", "indijk", "heidenschap", "itens", "jutrijp", "kimswerd", "kornwerderzand", "koudum", "koufurderrige",
        "kubaard", "loënga", "lollum", "longerhouw", "lutkewierum", "makkum", "molkwerum", "nijhuizum", "nijland", "offingawier", "oosterend", "oosterwierum", "oosthem", "oppenhuizen", "oudega", "parrega", "piaam", "pingjum", "poppingawier", "rauwerd", "rien", "roodhuis",
        "sandfirden", "scharnegoutum", "schettens", "schraard", "sijbrandaburen", "smallebrugge", "sneek", "stavoren", "terzool", "tirns", "tjalhuizum", "tjerkwerd", "uitwellingerga", "waaxens", "warns", "westhem", "wieuwerd", "witmarsum", "wolsum", "wommels", "wons",
        "workum", "woudsend", "ypecolsga", "zurich"]
        if self.city in zuidwestfriesland:
            self.data = ZuidWestFrieslandAfval().get_data(
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
