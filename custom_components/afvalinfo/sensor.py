#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

with zipcode and housenumber you can get the bagID:
https://apps.hvcgroep.nl/rest/adressen/ 5" …zipcode…"-"…housenumber…"
example: https://apps.hvcgroep.nl/rest/adressen/3328DB-37 4

output looks like

[{"bagId":"0505200000092263","postcode":"3328LN","huisnummer":35,"huisletter":"","huisnummerToevoeging":"","openbareRuimteNaam":"Moestuin","woonplaatsNaam":"Dordrecht","latitude":51.7701971,"longitude":4.6597255,"woonplaatsId":2351,"gemeenteId":505}]
find bagid:0505200000092263

get data:
https://apps.hvcgroep.nl/rest/adressen/ 5" …myBagId … “/kalender/” … myYear
url looks like:
https://apps.hvcgroep.nl/rest/adressen/0505200000092263/kalender/2019 5

Urls for other providers:

Copy to clipboard
Cyclus NV: https://afvalkalender.cyclusnv.nl
HVC: https://apps.hvcgroep.nl
Dar: https://afvalkalender.dar.nl
Afvalvrij / Circulus-Berkel: https://afvalkalender.circulus-berkel.nl
Meerlanden: https://afvalkalender.meerlanden.nl
Cure: https://afvalkalender.cure-afvalbeheer.nl
Avalex: https://www.avalex.nl
RMN: https://inzamelschema.rmn.nl
Venray: https://afvalkalender.venray.nl
Berkelland: https://afvalkalender.gemeenteberkelland.nl
Alphen aan den Rijn: https://afvalkalender.alphenaandenrijn.nlrest/adressen/0505200000061116/afvalstromen
Waalre: http://afvalkalender.waalre.nl
ZRD: https://afvalkalender.zrd.nl
Spaarnelanden: https://afvalwijzer.spaarnelanden.nl
Montfoort: https://afvalkalender.montfoort.nl
GAD: https://inzamelkalender.gad.nl
Cranendonck: https://afvalkalender.cranendonck.nl

ToDo: Merge / refactor all the Ximmio stuff and add hellendoorn
ToDo: Add the old municities: Bedum, Winsum (Het Hoge Land). https://gemeente.groningen.nl/afvalwijzer/
ToDo: Add huisnummer toevoeging
ToDo: Fix all the next year problems
ToDo: Add the following gemeenten:
Amsterdam                       ???
Beesel                          (https://www.beesel.nl/inwoners/afval-en-milieu/afvalkalender/)
Bergen Limburg                  bergen.nl/home/afval_44490/item/afvalkalender-2020_38953.html
Coevorden                       https://www.area-afval.nl/voor-bewoners/afvalkalender/digitale-afvalkalender
Cranendonck                     https://afvalkalender.cranendonck.nl/
Dantumadeel                     https://www.dantumadiel.frl/afvalkalender Woont u in het voormalige Ferwerderadiel dan wordt het afval opgehaald door Omrin
Delft                           http://www.avalex.nl/kalender/ Avalex heeft waarschijnlijk nergens een kalender. Voor alle zoekopdrachten krijg je "Voor dit adres is geen kalender beschikbaar"
Delfzijl                        https://www.delfzijl.nl/inwoners/afvalkalender_43586/
Edam-Volendam                   https://www.edam-volendam.nl/portal-home/inzamelkalender_43466/
Eemnes                          https://www.eemnes.nl/inwoners/Afval/Afvalwijzer
Emmen                           https://www.area-afval.nl/voor-bewoners/afvalkalender/digitale-afvalkalender
Gennep                          https://www.gennep.nl/document.php?m=28&fileid=98242&f=834a3177a76c30293e3e9d1c200729fb&attachment=0&c=34148
Goes                            https://afvalkalender.goes.nl/
Gorinchem                       https://www.waardlanden.nl/particulieren/afvalinzameling/afvalkalender
Groningen                       https://gemeente.groningen.nl/afvalwijzer/groningen
Haaren                          https://haaren.afvalstoffendienstkalender.nl/
Hardinxveld-Giessendam          https://www.waardlanden.nl/particulieren/afvalinzameling/afvalkalender
Hellevoetsluis                  https://www.hellevoetsluis.nl/Inwoners/WONEN_EN_LEEFOMGEVING/Afval/Afvalkalender
's-Hertogenbosch                https://www.afvalstoffendienst.nl/login
Het Hogeland                    https://hethogeland.nl/afval/afvalkalender
Hoeksche Waard                  https://www.radhw.nl/inwoners/ophaalschema
Hoogeveen                       https://www.area-afval.nl/voor-bewoners/afvalkalender/digitale-afvalkalender
Katwijk                         https://afval.katwijk.nl/nc/afvalkalender/
Landerd                         https://www.landerd.nl/inwoners-en-ondernemers/afval/afvalkalender/pdf/2020
Landsmeer                       https://admin.sduconnect.nl/linked_links/1577977473Afvalkalender_2020_DEF.pdf
Leidschendam-Voorburg           http://www.avalex.nl/kalender/
Loppersum                       https://gemeente.groningen.nl/afvalwijzer/loppersum?pk_campaign=Redirects&pk_kwd=data-afvalinzameling
Maassluis                       https://www.maassluis.nl/wonen-verkeer-en-veiligheid/afvalinzameling_43871/
Middelburg                      https://www.middelburg.nl/Inwoners/Afval/Ophaaldagen_huisvuil
Midden-Delfland                 http://www.avalex.nl/kalender/
Molenlanden                     https://www.waardlanden.nl/particulieren/afvalinzameling/afvalkalender
Mook en Middelaar               https://www.mookenmiddelaar.nl/inwoner/afval-en-duurzaamheid_42542/item/afvalkalender-2020_40888.html
Nederweert                      https://www.nederweert.nl/inwoners/huisvuil-2019_45554/
Oegstgeest                      https://www.oegstgeest.nl/fileadmin/editor/Documenten/Inwoners/Alles_over_afval/afvalkalender_2020_v8.pdf
Oisterwijk                      https://oisterwijk.afvalstoffendienstkalender.nl/
Oostzaan                        https://www.oostzaan.nl/mozard/document/docnr/1182761/bijlage%20-%20afvalkalender%20Oostzaan%202020%20-%20met%20wijkindeling
Ouder-Amstel                    https://www.ouder-amstel.nl/Home/Nieuws_en_actualiteiten/Nieuws/Alle_nieuwsberichten_2020/April/Data_inzameling_afval
Peel en Maas                    https://afvalkalender.peelenmaas.nl/
Pijnacker-Nootdorp              http://www.avalex.nl/kalender/
Reusel-De Mierden               https://www.reuseldemierden.nl/document.php?m=25&fileid=123208&f=3e3d90c015a9b15ffc98c993c8e4e9da&attachment=0&c=40975
Rijswijk                        http://www.avalex.nl/kalender/
Rozendaal                       https://www.rozendaal.nl/dsresource?objectid=d7a004f0-ff97-490a-8837-1b66e5bc11e1&type=org
Schiermonnikoog
Schouwen-Duiveland              https://afvalkalender.schouwen-duiveland.nl/
Steenbergen                     https://www.gemeente-steenbergen.nl/inwoners_overzicht/afval/
Texel                           https://www.texel.nl/mozard/!suite86.scherm0325?mVrg=5059
Uden                            https://www.uden.nl/inwoners/afval/ophaaldagen-afval/
Uithoorn                        https://www.uithoorn.nl/Home/Afval/Afvalkalender
Vlieland                        https://www.vlieland.nl/v-zelf-regelen/producten_42533/product/afval-huishoudelijk-afval_17.html
Vlissingen                      https://www.vlissingen.nl/inwoner/afval-en-milieu/afval/huishoudelijk-afval-en-afvalkalender.html
Voorschoten                     https://www.voorschotenmaakthetverschil.nl/
Vught                           https://vught.afvalstoffendienstkalender.nl/
Waalre                          https://afvalkalender.waalre.nl/
Wassenaar                       http://www.avalex.nl/kalender/
Weert                           https://www.weert.nl/huisvuil-duobak-en-ophaaldagen
Westerwolde                     https://www.westerwolde.nl/trash-removal-calendar
Zundert                         https://www.zundert.nl/afval-en-milieustraat/afvalkalender-2020.html
"""

import voluptuous as vol
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.error
from babel import Locale
from babel.dates import format_date, format_datetime, format_time
import re

from .const.const import (
    MIN_TIME_BETWEEN_UPDATES,
    _LOGGER,
    CONF_CITY,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_DATE_FORMAT,
    CONF_TIMESPAN_IN_DAYS,
    CONF_LOCALE,
    SENSOR_PREFIX,
    ATTR_LAST_UPDATE,
    ATTR_HIDDEN,
    ATTR_DAYS_UNTIL_COLLECTION_DATE,
    ATTR_IS_COLLECTION_DATE_TODAY,
    ATTR_YEAR_MONTH_DAY_DATE,
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
from .location.circulusberkel import CirculusBerkelAfval
from .location.acv import AcvAfval
from .location.irado import IradoAfval
from .location.rd4 import Rd4Afval
from .location.dar import DarAfval
from .location.drimmelen import DrimmelenAfval
from .location.zrd import ZrdAfval
from .location.rmn import RmnAfval
from .location.goereeoverflakkee import GoereeOverflakkeeAfval
from .location.berkelland import BerkellandAfval
from .location.middendrenthe import MiddenDrentheAfval
from .location.denhaag import DenHaagAfval
from .location.purmerend import PurmerendAfval
from .location.borsele import BorseleAfval
from .location.hellendoorn import HellendoornAfval

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
        vol.Optional(CONF_TIMESPAN_IN_DAYS, default="365"): cv.string,
        vol.Optional(CONF_LOCALE, default = "en"): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup Afvalinfo sensor")

    city = config.get(CONF_CITY).lower().strip()
    postcode = config.get(CONF_POSTCODE).strip()
    street_number = config.get(CONF_STREET_NUMBER)
    date_format = config.get(CONF_DATE_FORMAT).strip()
    timespan_in_days = config.get(CONF_TIMESPAN_IN_DAYS)
    locale = config.get(CONF_LOCALE)

    try:
        resourcesMinusTodayAndTomorrow = config[CONF_RESOURCES].copy()
        if "trash_type_today" in resourcesMinusTodayAndTomorrow:
            resourcesMinusTodayAndTomorrow.remove("trash_type_today")
        if "trash_type_tomorrow" in resourcesMinusTodayAndTomorrow:
            resourcesMinusTodayAndTomorrow.remove("trash_type_tomorrow")

        data = AfvalinfoData(city, postcode, street_number, resourcesMinusTodayAndTomorrow)
    except urllib.error.HTTPError as error:
        _LOGGER.error(error.reason)
        return False

    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        #if sensor_type not in SENSOR_TYPES:
        if sensor_type.title().lower() != "trash_type_today" and sensor_type.title().lower() != "trash_type_tomorrow":
            entities.append(AfvalinfoSensor(data, sensor_type, date_format, timespan_in_days, locale))

        #Add sensor -trash_type_today
        if sensor_type.title().lower() == "trash_type_today":
            today = AfvalInfoTodaySensor(data, sensor_type, entities)
            entities.append(today)
        #Add sensor -trash_type_tomorrow
        if sensor_type.title().lower() == "trash_type_tomorrow":
            tomorrow = AfvalInfoTomorrowSensor(data, sensor_type, entities)
            entities.append(tomorrow)

    add_entities(entities)


class AfvalinfoData(object):
    def __init__(self, city, postcode, street_number, resources):
        self.data = None
        self.city = city
        self.postcode = postcode
        self.street_number = street_number
        self.resources = resources

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Updating Waste collection dates")
        acv = ["bennekom", "de klomp", "deelen", "doorwerth", "ede", "ederveen", "harskamp", "heelsum", "heveadorp", "lunteren", "oosterbeek", "otterlo", "renkum", "renswoude", "veenendaal", "wageningen", "wekerom", "wolfheze"]
        if self.city in acv:
            self.data = AcvAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        alkmaar = ["alkmaar", "driehuizen", "graft", "grootschermer", "koedijk", "markenbinnen", "noordeinde", "oost-graftdijk", "oterleek", "oudorp", "de rijp", "schermerhorn", "starnmeer", "stompetoren", "ursem", "west-graftdijk", "zuidschermer"]
        if self.city in alkmaar:
            self.data = AlkmaarAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        almere = ["almere"]
        if self.city in almere:
            self.data = AlmereAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        alphenaandenrijn = ["aarlanderveen", "alphen aan den rijn", "benthuizen", "boskoop", "hazerswoude-dorp", "hazerswoude-rijndijk", "koudekerk aan den rijn", "zwammerdam"]
        if self.city in alphenaandenrijn:
            self.data = AlphenAanDenRijnAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        bar = ["barendrecht", "bolnes", "oostendam", "poortugaal", "rhoon", "ridderkerk"]
        if self.city in bar:
            self.data = BarAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        berkelland = ["beltrum", "borculo", "eibergen", "geesteren", "gelselaar", "haarlo", "neede", "noordijk", "rekken", "rietmolen", "ruurlo"]
        if self.city in berkelland:
            self.data = BerkellandAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        blink = ["aarle-rixtel", "asten", "bakel", "beek en donk", "de mortel", "de rips", "deurne", "elsendorp", "gemert", "gerwen", "handel", "heeze", "helenaveen", "helmond", "heusden", "leende", "lierop", "lieshout", "liessel", "mariahout", "milheeze", "nederwetten", "neerkant", "nuenen",
        "ommel", "someren", "sterksel", "vlierden"]
        if self.city in blink:
            self.data = BlinkAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        borsele = ["baarland", "borssele", "driewegen", "ellewoutsdijk", "heinkenszand", "hoedekenskerke", "kwadendamme", "lewedorp", "nieuwdorp", "nisse", "oudelande", "ovezande", "s-gravenpolder", "s-heer abtskerke", "s-heerenhoek"]
        if self.city in borsele:
            self.data = BorseleAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        circulusberkel = ["almen", "apeldoorn", "baak", "barchem", "bathmen", "beekbergen", "beemte-broekland", "bronkhorst", "bussloo", "de vecht", "deventer", "diepenveen", "doesburg", "drempt", "eefde", "emst", "epe", "epse", "gorssel", "halle", "harfsen", "hengelo", "hoenderloo",
        "hoog soeren", "hoog-keppel", "hummelo", "joppe", "keijenborg", "klarenbeek", "kring van dorth", "laag-keppel", "laren", "lettele", "lieren", "lochem", "loenen", "nijbroek", "oene", "okkenbroek", "olburgen", "radio kootwijk", "rha", "schalkhaar", "steenderen", "terwolde", "teuge",
        "toldijk", "twello", "uddel", "ugchelen", "vaassen", "vierakker", "voorst", "vorden", "warnsveld", "wenum-wiesel", "wichmond", "wilp", "wilp-achterhoek", "zelhem", "zutphen"]
        if self.city in circulusberkel:
            self.data = CirculusBerkelAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        cyclus = ["ammerstol", "bergambacht", "berkenwoude", "bodegraven", "de meije", "driebruggen", "gouda", "gouderak", "haastrecht", "hogebrug", "hoogmade", "kaag", "krimpen aan de lek", "lageweg", "langeraar", "leimuiden", "lekkerkerk", "linschoten", "moerkapelle", "montfoort",
        "moordrecht", "nieuwe wetering", "nieuwerbrug", "nieuwerkerk aan den ijssel", "nieuwkoop", "nieuwveen", "noordeinde", "noorden", "opperduit", "oud ade", "oude wetering", "ouderkerk aan den ijssel", "reeuwijk-brug", "reeuwijk-dorp", "rijnsaterwoude", "rijpwetering", "roelofarendsveen",
        "schoonhoven", "schuwacht", "sluipwijk", "stolwijk", "tempel", "ter aar", "vlist", "waarde", "waddinxveen", "willeskop", "willige langerak", "woerdense verlaat", "woubrugge", "zevenhoven", "zevenhuizen"]
        if self.city in cyclus:
            self.data = CyclusAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        dar = ["afferden", "balgoij", "batenburg", "beek", "berg en dal", "bergharen", "beuningen", "deest", "druten", "erlecom", "ewijk", "groesbeek", "heilig landstichting", "hernen", "heumen", "horssen", "kekerdom", "leur", "leuth", "malden", "millingen aan de rijn", "nederasselt", "niftrik",
        "nijmegen", "ooij", "overasselt", "persingen", "puiflijk", "ubbergen", "weurt", "wijchen", "winssen"]
        if self.city in dar:
            self.data = DarAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
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
                self.city, self.postcode, self.street_number, self.resources
            )
        denhaag = ["den haag"]
        if self.city in denhaag:
            self.data = DenHaagAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        defriesemeren = ["akmarijp", "bakhuizen", "balk", "ballingbuur", "bantega", "bargebek", "boornzwaag", "boornzwaag over de wielen", "brekkenpolder", "broek", "commissiepolle", "de bels", "de polle", "de rijlst", "delburen", "delfstrahuizen", "dijken", "doniaga", "echten", "echtenerbrug",
        "eesterga", "elahuizen", "finkeburen", "follega", "goingarijp", "harich", "haskerhorne", "heide", "hooibergen", "huisterheide", "idskenhuizen", "joure", "kolderwolde", "langweer", "legemeer", "lemmer", "marderhoek", "mirns", "nieuw amerika", "nijehaske", "nijemirdum", "noed", "oldeouwer",
        "onland", "oosterzee", "oudega", "oudehaske", "oudemirdum", "ouwster-nijega", "ouwsterhaule", "rijs", "rohel", "rotstergaast", "rotsterhaule", "rottum", "ruigahuizen", "scharsterbrug", "schoterzijl", "schouw", "sint nicolaasga", "sintjohannesga", "sloten", "snikzwaag", "sondel", "spannenburg",
        "tacozijl", "terhorne", "terkaple", "teroele", "tjerkgaast", "trophorne", "vegelinsoord", "vierhuis", "vinkeburen", "vrisburen", "westend", "westerend-harich", "wijckel", "zevenbuurt"]
        if self.city in defriesemeren:
            self.data = DeFrieseMerenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        drimmelen = ["blauwe sluis", "drimmelen", "helkant", "hooge zwaluwe", "lage zwaluwe", "made", "oud-drimmelen", "terheijden", "wagenberg"]
        if self.city in drimmelen:
            self.data = DrimmelenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        gad = ["ankeveen", "blaricum", "bussum", "de horn", "hilversum", "huizen", "kortenhoef", "laren", "muiden", "muiderberg", "naarden", "nederhorst den berg", "nieuw-loosdrecht", "oud-loosdrecht", "s-graveland", "uitermeer", "weesp"]
        if self.city in gad:
            self.data = GadAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        goereeoverflakkee = ["achthuizen", "den bommel", "dirksland", "goedereede", "havenhoofd", "herkingen", "melissant", "middelharnis", "nieuwe-tonge", "ooltgensplaat", "ouddorp", "oude-tonge", "sommelsdijk", "stad aan t haringvliet", "stellendam", "zuidzijde"]
        if self.city in goereeoverflakkee:
            self.data = GoereeOverflakkeeAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        hellendoorn = ["daarle", "daarlerveen", "haarle", "hellendoorn", "nijverdal"]
        if self.city in hellendoorn:
            self.data = HellendoornAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        hvc = ["aagtdorp", "aartswoud", "abbekerk", "abbestede", "alblasserdam", "andijk", "anna paulowna", "assendelft", "avenhorn", "bant", "barsingerhorn", "benningbroek", "bergen aan zee", "bergen", "berkhout", "beverwijk", "blokdijk", "blokker", "bobeldijk", "bovenkarspel", "breezand", "bregtdorp",
        "burgerbrug", "burgervlotbrug", "callantsoog", "camperduin", "catrijp", "creil", "de buurt", "de goorn", "de haukes", "de stolpen", "de strook", "de weere", "den helder", "den oever", "dirkshorn", "dordrecht", "driehuis", "eenigenburg", "egmond aan den hoef", "egmond aan zee", "egmond-binnen",
        "emmeloord", "enkhuizen", "ens", "espel", "gouwe", "groenveld", "groet", "groote keeten", "grootebroek", "grosthuizen", "hargen", "haringhuizen", "hauwert", "heemskerk", "heerjansdam", "hem", "hendrik-ido-ambacht", "hensbroek", "hippolytushoef", "hoogkarspel", "hoogwoud", "hoorn", "huisduinen",
        "ijmuiden", "jisp", "julianadorp", "kalverdijk", "keinse", "kleine sluis", "kleine-lindt", "kolhorn", "koog aan de zaan", "krabbendam", "kraggenburg", "kreil", "kreileroord", "krommenie", "lambertschaag", "lelystad", "lutjebroek", "lutjewinkel", "luttelgeest", "marknesse", "medemblik", "middenmeer",
        "midwoud", "moerbeek", "nagele", "neck", "nibbixwoud", "nieuwe niedorp", "nieuwesluis", "obdam", "onderdijk", "oosterblokker", "oosterdijk", "oosterklief", "oosterland", "oosterleek", "oostknollendam", "oostwoud", "opmeer", "opperdoes", "oude niedorp", "oudendijk", "oudesluis", "papendrecht", "petten",
        "rinnegom", "rustenburg", "rutten", "santpoort-noord", "santpoort-zuid", "schagen", "schagerbrug", "scharwoude", "schellinkhout", "schokland", "schoorl", "schoorldam", "sijbekarspel", "sint maarten", "sint maartensbrug", "sint maartensvlotbrug", "sint maartenszee", "slootdorp", "smerp", "spaarndammerpolder",
        "spanbroek", "spierdijk", "spijkerboor", "stroe", "stroet", "t rijpje", "t veld", "t zand", "terdiek", "tjallewal", "tolke", "tollebeek", "tuitjenhorn", "twisk", "ursem", "valkkoog", "van ewijcksluis", "vatrop", "velsen", "velsen-noord", "velsen-zuid", "velserbroek", "venhuizen", "verlaat", "waarland",
        "wadway", "warmenhuizen", "wervershoof", "westerklief", "westerland", "westknollendam", "westwoud", "westzaan", "wieringerwaard", "wieringerwerf", "wijdenes", "wijdewormer", "wijk aan duin", "wijk aan zee", "wimmenum", "winkel", "wogmeer", "wognum", "wormer", "wormerveer", "zaandam", "zaandijk",
        "zandwerven", "zeewolde", "zijdewind", "zuidermeer", "zwaag", "zwaagdijk-oost", "zwaagdijk-west", "zwijndrecht"]
        if self.city in hvc:
            self.data = HvcAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        irado = ["capelle aan den ijssel", "rozenburg", "schiedam", "vlaardingen"]
        if self.city in irado:
            self.data = IradoAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        meerlanden = ["aalsmeer", "aalsmeerderbrug", "abbenes", "aerdenhout", "badhoevedorp", "beinsdorp", "bennebroek", "bentveld", "bloemendaal", "bloemendaal aan zee", "boesingheliede", "buitenkaag", "burgerveen", "cruquius", "de zilk", "diemen", "haarlemmerliede", "halfweg", "heemstede", "hillegom",
        "hoofddorp", "kudelstaart", "leimuiderbrug", "lijnden", "lisse", "lisserbroek", "nieuw-vennep", "noordwijk aan zee", "noordwijk-binnen", "noordwijkerhout", "oude meer", "overveen", "rijsenhout", "schiphol", "schiphol-rijk", "spaarndam", "vijfhuizen", "vogelenzang", "weteringbrug",
        "zwaanshoek", "zwanenburg"]
        if self.city in meerlanden:
            self.data = MeerlandenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        meppel = ["havelterberg", "kolderveen", "meppel", "nijeveen", "rogat"]
        if self.city in meppel:
            self.data = MeppelAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        middendrenthe = ["balinge", "beilen", "bovensmilde", "bruntinge", "drijber", "elp", "eursinge", "garminge", "hijken", "hoogersmilde", "hooghalen", "mantinge", "nieuw-balinge", "oranje", "orvelte", "smilde", "spier", "westerbork", "wijster", "witteveen", "zuidveld", "zwiggelte"]
        if self.city in middendrenthe:
            self.data = MiddenDrentheAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        mijnafvalwijzer = ["aarle", "abcoude", "achterberg", "achterveld", "aerdt", "akersloot", "almkerk", "alphen", "altena", "alteveer", "amen", "america", "amerongen", "amstelhoek", "amstelveen", "amstenrade", "andel", "andelst", "anderen", "angeren", "angerlo", "anloo", "annen", "annerveenschekanaal",
        "anreep-schieven", "ansen", "assen", "assum", "baambrugge", "baarle", "baarschot", "babberich", "babylonienbroek", "bad nieuweschans", "baexem", "bahr", "bakkum", "bakkum-noord", "balloerveld", "balloo", "bareveld", "barlage", "barneveld", "bavel", "beegden", "beek", "beerta", "beesel", "bemmel",
        "benschop", "berg aan de maas", "bergeijk", "bergen op zoom", "berghem", "berghuizen", "bergschenhoek", "berkel en rodenrijs", "berkel-enschot", "berlicum", "best", "bevermeer", "biddinghuizen", "biest-houtakker", "bilthoven", "bingelrade", "bingerden", "bladel", "blauwestad", "bleiswijk", "blekslage",
        "boerdonk", "bontebrug", "boornbergum", "borger", "borgercompagnie", "borkel", "born", "boskant", "bosschenhoofd", "boven pekela", "bovenveen", "boxtel", "braamberg", "breda", "breedenbroek", "breukelen", "brielle", "broek in waterland", "broek op langedijk", "broekhorn", "broekhuizen", "broekhuizenvorst",
        "broeksittard", "bronneger", "bronnegerveen", "buchten", "buggenum", "buinen", "buinerveen", "bunne", "cabauw", "calfven", "capelle", "castelre", "casteren", "castricum aan zee", "castricum", "catsop", "ceresdorp", "chaam", "cothen", "dalem", "de beek", "de bilt", "de glind", "de groeve", "de hoef",
        "de meern", "de meije", "de moer", "de noord", "de punt", "de steeg", "de tike", "de veenhoop", "de vleut", "de vorst", "de wijk", "de wilgen", "de woude", "demen", "den berg", "den dungen", "den hout", "dennenburg", "deursen", "deurze", "dieden", "dieren", "diessen", "doenrade", "doetinchem", "dommelen",
        "donderen", "dongen", "dongense vaart", "doorn", "doornenburg", "doornspijk", "dorst", "draai", "drachten", "drachtstercompagnie", "drie", "driebergen-rijsenburg", "drieborg", "driel", "drogteropslagen", "drongelen", "dronten", "drouwen", "drouwenermond", "drouwenerveen", "duiven", "duizel", "dusseldorp",
        "dussen", "echten", "eekt", "eelde", "eelderwolde", "een", "een-west", "eerde", "eersel", "eerste exloermond", "ees", "eesergroen", "eeserveen", "eethen", "eext", "eexterveen", "eexterveenschekanaal", "eexterzandvoort", "eindhoven", "einighausen", "ekehaar", "elburg", "eldersloo", "eleveld", "ell", "ellecom",
        "ellertshaar", "elsloo", "elspeet", "elst", "ermelo", "erp", "esbeek", "etsberg", "etten", "etten-leur", "eursinge", "evertsoord", "exloo", "exloërveen", "fijnaart", "finsterwolde", "fort", "foxhol", "foxwolde", "froombosch", "gaanderen", "galder", "garderen", "gasselte", "gasselternijveen", "gasselternijveenschemond",
        "gasteren", "geelbroek", "geertruidenberg", "geffen", "gelderswoude", "geldrop", "geleen", "gemonde", "genderen", "gendringen", "gendt", "genhout", "geverik", "giesbeek", "giessen", "gieten", "gieterveen", "gilze", "goengahuizen", "goirle", "grafhorst", "graswijk", "grathem", "grevenbicht", "griendtsveen", "groenekan",
        "groessen", "grolloo", "grubbenvorst", "guttecoven", "haalderen", "haarzuilens", "haelen", "haghorst", "haler", "hank", "hapert", "harderwijk", "haren", "harkstede", "harmelen", "hattemerbroek", "heel", "heerhugowaard", "heerle", "heesch", "heeswijk-dinther", "hegelsom", "heibloem", "heijningen", "heiligerlee", "heiloo",
        "hekendorp", "hellum", "helwijk", "hemmen", "herkenbosch", "herpen", "herveld", "herwen", "heteren", "heythuysen", "hezelaar", "hierden", "hilvarenbeek", "hochte", "hoevelaken", "hoeven", "hollandsche rading", "holten", "holtum", "hoog geldrop", "hoogeloon", "hoogerheide", "hoogezand", "horn", "horst", "horsten",
        "houtdorp", "houten", "houtigehage", "huijbergen", "huis ter heide", "huisseling", "huissen", "hulsberg", "hulshorst", "hulten", "hunsel", "ijsselmuiden", "ilpendam", "ittervoort", "jaarsveld", "jabeek", "kaatsheuvel", "kamerik", "kampen", "kamperveen", "kanis", "kasteren", "katwoude", "keldonk", "kelmond",
        "kelpen-oler", "kerkdorp", "kerkenveld", "kessel", "kibbelgaarn", "kiel-windeweer", "kinderbos", "klein-dongen", "kleine meers", "klijndijk", "klundert", "knegsel", "kockengen", "koedijk", "koekange", "koekangerveld", "kolham", "kootwijk", "kootwijkerbroek", "kopstukken", "kortehemmen", "krimpen aan den ijssel",
        "kronenberg", "kropswolde", "kruisweg", "laag-soeren", "langbroek", "langelo", "langenberg", "langeweg", "lapstreek", "lathum", "leersum", "leiden", "leiderdorp", "lennisheuvel", "lerop", "leusden", "leusden-zuid", "leutingewolde", "leuvenum", "liempde", "lieveren", "limbricht", "limmen", "limmerkoog", "linde",
        "linne", "lith", "lithoijen", "lobith", "loenen aan de vecht", "loenersloot", "loo", "looeind", "loon op zand", "loon", "loosbroek", "lopik", "lopikerkapel", "lottum", "luddeweer", "luissel", "luyksgestel", "maarn", "maarsbergen", "maarssen", "maarssenbroek", "maartensdijk", "maasband", "maasbracht", "maaskantje",
        "macharen", "maren", "maren-kessel", "mariaheide", "marken", "marwijksoord", "matsloot", "meeden", "meerlo", "meers", "meeuwen", "megchelen", "megen", "melderslo", "melick", "merkelbeek", "meterik", "middelbeers", "middelrode", "midlaren", "midwolda", "mierlo", "mijdrecht", "moerdijk", "moerstraten", "molenschot",
        "monnickendam", "montfort", "mullegen", "munstergeleen", "muntendam", "mussel", "musselkanaal", "nattenhoven", "neer", "neerbeek", "neeritter", "neerlangel", "neerloon", "nergena", "nes aan de amstel", "netersel", "netterden", "nietap", "nieuw annerveen", "nieuw-beerta", "nieuw-buinen", "nieuw-roden", "nieuw-scheemda",
        "nieuw-wehl", "nieuwe pekela", "nieuwediep", "nieuwendijk", "nieuwer ter aa", "nieuwersluis", "nieuwolda", "nigtevecht", "nijega", "nijkerk", "nijkerkerveen", "nijlande", "nijnsel", "nispen", "nistelrode", "nooitgedacht", "noord-scharwoude", "noordbroek", "noordeinde", "noordhoek", "norg", "numero dertien", "nunhem",
        "nunspeet", "nuth", "obbicht", "odoorn", "odoornerveen", "offenbeek", "ohe en laak", "oijen", "oirsbeek", "oirschot", "oldebroek", "olland", "ommelanderwijk", "onstwedde", "oosteind", "oosteinde", "oostelbeers", "oosterhout", "oosterwolde", "oostvoorne", "oostwold", "ooy", "opeinde", "oss", "ossendrecht", "oud annerveen",
        "oud gastel", "oud-zevenaar", "oud-zuilen", "oude pekela", "oudega", "oudemolen", "oudenbosch", "oudewater", "oudezijl", "oudkarspel", "overberg", "overlangel", "overschild", "paarlo", "pannerden", "papekop", "papenhoven", "papenvoort", "paterswolde", "peest", "peize", "peizermade", "peizerwold", "polsbroek",
        "polsbroekerdam", "posterholt", "posthoorn", "purmer", "puth", "putte", "putten", "raamsdonk", "raamsdonksveer", "randwijk", "ravenstein", "ressen", "reutje", "reuver", "rheden", "rhee", "rhenen", "riel", "riethoven", "rijen", "rijkel", "rijssen", "rockanje", "roden", "rodenrijs", "roderesch", "roderwolde", "roermond",
        "roggel", "rolde", "roond", "roosendaal", "rotte", "rotterdam", "rottevalle", "rucphen", "ruinen", "ruinerwold", "s gravenmoer", "s-gravenmoerse vaart", "s-heerenbroek", "sandebuur", "sappemeer", "sassenheim", "schaft", "schalkwijk", "scharmer", "scheemda", "scherpenzeel", "schijf", "schijndel", "schildwolde", "schimmert",
        "schinnen", "schinveld", "schipborg", "schoonloo", "selissen", "sevenum", "siddeburen", "silvolde", "sinderen", "sint odilienberg", "sint pancras", "sint-michielsgestel", "sint-oedenrode", "sittard", "sleeuwijk", "slijk-ewijk", "slochteren", "smalle ee", "smeerling", "spankeren", "spaubeek", "speuld", "spijk", "spijkerboor",
        "spoordonk", "sprang", "sprundel", "st. willebrord", "stadskanaal", "stampersgat", "standdaarbuiten", "staverden", "steenbergen", "steendam", "steensel", "stein", "sterenborg", "stevensweert", "stoutenburg", "strijbeek", "stroe", "swalmen", "sweikhuizen", "swifterbant", "swolgen", "t goy", "t harde", "t loo", "taarlo",
        "teeffelen", "telgt", "ter aard", "ter wupping", "terborg", "terheijl", "terschuur", "thorn", "tienhoven", "tienray", "tilburg", "tjuchem", "tolkamer", "tongeren", "tonnekreek", "tonsel", "tripscompagnie", "trutjeshoek", "tuindorp", "tull en t waal", "tweede exloermond", "tweede valthermond", "tynaarlo", "ubbena",
        "udenhout", "uitdam", "uitgeest", "uitweg", "uitwijk", "ulft", "ulicoten", "ulvenhout", "uppel", "urmond", "utrecht", "valburg", "valkenswaard", "valthe", "valthermond", "varsselder", "varsseveld", "veen", "veendam", "veenhuizen", "veeningen", "veghel", "velp", "verlaat", "vessem", "vierhouten", "vierpolders", "vinkel",
        "vinkeveen", "vledderhuizen", "vledderveen", "vleuten", "vlodrop", "vlodrop-station", "voorhout", "voorthuizen", "vorstenbosch", "voskuil", "vosseberg", "vredenheim", "vreeland", "vries", "vrijhoeve-capelle", "vrilkhoven", "waalwijk", "waardhuizen", "warmond", "waspik", "waspik-zuid", "watergang", "waterhuizen",
        "waverveen", "weebosch", "wehl", "werkendam", "wessem", "westbroek", "westdorp", "westelbeers", "westendorp", "westerbroek", "westerhoven", "westerlee", "westervelde en zuidvelde", "westervoort", "wezep", "wijbosch", "wijk bij duurstede", "wijk en aalburg", "wijnandsrade", "wijnbergen", "wildervank", "wildervanksterdallen",
        "willemstad", "willige langerak", "wilnis", "wilsum", "winde", "winschoten", "wintelre", "witten", "woensdrecht", "woerden", "woudbloem", "woudrichem", "wouw", "wouwse plantage", "yde", "zalk", "zandberg", "zeegse", "zegge", "zegveld", "zeijen", "zeijerveld", "zetten", "zevenaar", "zevenbergschen hoek", "zijtaart",
        "zoetermeer", "zoeterwoude-dorp", "zoeterwoude-rijndijk", "zuid-scharwoude", "zuidbroek", "zuiderwoude", "zuidlaarderveen", "zuidlaren", "zuidwolde", "zwartebroek", "zwartewaal"]
        if self.city in mijnafvalwijzer:
            self.data = MijnAfvalWijzerAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        nissewaard = ["abbenbroek", "geervliet", "heenvliet", "hekelingen", "simonshaven", "spijkenisse", "zuidland"]
        if self.city in nissewaard:
            self.data = NissewaardAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        omrin = ["aalsum", "achlum", "aegum", "akkrum", "anjum", "appelscha", "appingedam", "augsbuurt", "augustinusga", "baaiduinen", "baard", "baijum", "bakkeveen", "ballum", "beers", "beetgum", "beetgumermolen", "beetsterzwaag", "bergum", "berlikum", "birdaard", "blesdijke", "blessum", "blija", "boelenslaan",
        "boer", "boijl", "boksum", "bokum", "bontebok", "bornwird", "brantgum", "breede", "britsum", "broek", "buitenpost", "buren", "burum", "cornjum", "de blesse", "de hoeve", "de knijpe", "deinum", "dokkum", "dongjum", "donkerbroek", "doodstil", "douwen", "drachten-azeven", "drogeham", "dronrijp", "ee",
        "eemshaven", "eenrum", "eernewoude", "eestrum", "elsloo", "engelum", "engwierum", "eppenhuizen", "ewer", "ferwerd", "finkum", "firdgum", "fochteloo", "formerum", "foudgum", "franeker", "friens", "frieschepalen", "garijp", "genum", "gerkesklooster", "gersloot", "giekerk", "gorredijk", "goutum", "grijssloot",
        "groot maarslag", "grouw", "hallum", "hantum", "hantumeruitburen", "hantumhuizen", "hardegarijp", "harkema", "harlingen", "haskerdijken", "haule", "haulerwijk", "hee", "heerenveen", "hefswal", "hempens	hempus", "hemrik", "herbaijum", "hiaure", "hijlaard", "hijum", "hitzum", "hogebeintum", "hollum", "holwerd",
        "hoorn", "hoornsterzwaag", "hornhuizen", "houwerzijl", "huins", "idaard", "irnsum", "janum", "jellum", "jelsum", "jislum", "jonkersland", "jorwerd", "jouswier", "jubbega", "kaakhorn", "kaard", "kantens", "katershorn", "katlijk", "kinnum", "klein maarslag", "kleine huisjes", "klooster-lidlum", "kloosterburen",
        "kollum", "kollumerpomp", "kollumerzwaag", "koningsoord", "kootstertille", "kruisweg", "landerum", "langedijke", "langelille", "langezwaag", "lauwersoog", "leens", "leeuwarden", "lekkum", "lichtaard", "lies", "lioessens", "lions", "lippenhuizen", "luinjeberd", "luxwoude", "makkinga", "mantgum", "marrum",
        "marssum", "menaldum", "mensingeweer", "metslawier", "midlum", "midsland", "miedum", "mildam", "minnertsga", "moddergat", "molenend", "molenrij", "morra", "munnekeburen", "munnekezijl", "nes", "niawier", "niekerk", "nieuwebrug", "nieuwehorne", "nieuweschoot", "nij altoenae", "nij beets", "nijeberkoop",
        "nijeholtpade", "nijeholtwolde", "nijelamer", "nijetrijne", "noordbergum", "noordpolderzijl", "noordwolde", "oenkerk", "oldeberkoop", "oldeboorn", "oldeholtpade", "oldeholtwolde", "oldelamer", "oldenzijl", "oldetrijne", "oldorp", "olterterp", "oosteinde", "oosterbierum", "oosterend", "oosterlittens",
        "oostermeer", "oosternieland", "oosternijkerk", "oosterstreek", "oosterwolde", "oostrum", "opwierde", "oranjewoud", "oude leije", "oudebildtzijl", "oudedijk", "oudehorne", "oudeschip", "oudeschoot", "oudkerk", "oudwoude", "paapstil", "paesens", "peins", "peperga", "pieterburen", "pietersbierum", "raard",
        "ravenswoud", "reitsum", "ried", "rijperkerk", "roodehaan", "roodeschool", "roordahuizum", "rottum", "rottumeroog", "rottumerplaat", "schalsum", "scherpenzeel", "schingen", "schouwen", "schouwerzijl", "sexbierum", "siegerswoude", "simonszand", "sint annaparochie", "sint jacobiparochie", "slappeterp",
        "slijkenburg", "snakkerburen", "solwerd", "sonnega", "spanga", "spannum", "startenhuizen", "steggerda", "stiens", "stitswerd", "striep", "stroobos", "suameer", "suawoude", "surhuisterveen", "surhuizum", "swichum", "t lage van de weg", "t stort", "teerns", "ter idzard", "terband", "ternaard", "terwispel",
        "tietjerk", "tijnje", "tjalleberd", "tjamsweer", "triemen", "twijzel", "twijzelerheide", "tzum", "tzummarum", "uithuizen", "uithuizermeeden", "ulrum", "ureterp", "usquert", "valom", "veenklooster", "vierhuizen", "vinkega", "vliedorp", "vrouwenparochie", "waaxens", "wadwerd", "wanswerd", "warffum",
        "warfhuizen", "warfstermolen", "warga", "warstiens", "wartena", "waskemeer", "wehe-den hoorn", "weidum", "welsrijp", "west-terschelling", "westergeest", "westernieland", "westhoek", "wetsens", "wier", "wierhuizen", "wierum", "wijnaldum", "wijnjewoude", "wijns", "wijtgaard", "winsum", "wirdum", "wolvega",
        "zandeweer", "zandhuizen", "zevenhuizen", "zoutkamp", "zuurdijk", "zwagerbosch", "zweins"]
        if self.city in omrin:
            self.data = OmrinAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        purmerend = ["middenbeemster", "noordbeemster", "purmerend", "purmerbuurt", "westbeemster", "zuidoostbeemster"]
        if self.city in purmerend:
            self.data = PurmerendAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        rd4 = ["amstenrade", "banholt", "bemelen", "berg", "beutenaken", "bingelrade", "bocholtz", "broekhem", "brunssum", "bunde", "cadier en keer", "doenrade", "eckelrade", "eijsden", "elkenrade", "epen", "eperheide", "etenaken", "euverem", "eys", "eyserheide", "geulle aan de maas", "geulle", "gronsveld", "gulpen",
        "heerlen", "heijenrath", "hilleshagen", "hoensbroek", "holset", "houthem", "hulsberg", "ingber", "jabeek", "kerkrade", "klimmen", "kunrade", "landgraaf", "lemiers", "maastricht", "margraten", "mariadorp en poelveld", "mechelen", "meerssen", "merkelbeek", "mesch en withuis", "mheer", "moorveld", "nijswiller",
        "noorbeek", "nuth", "oirsbeek", "oost-maarland", "oud-valkenburg", "partij-wittem", "puth", "ransdaal", "reijmerstok", "rijckholt", "rothem", "scheulder", "schimmert", "schin op geul", "schinnen", "schinveld", "schweiberg", "sibbe", "simpelveld", "sint geertruid", "slenaken", "stokhem", "sweikhuizen",
        "trintelen", "ubachsberg", "ulestraten", "vaals", "valkenburg", "vijlen", "vilt", "voerendaal", "wahlwiller", "wijlre", "wijnandsrade"]
        if self.city in rd4:
            self.data = Rd4Afval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        rmn = ["austerlitz", "baarn", "bosch en duin", "bunnik", "den dolder", "eembrugge", "huis ter heide", "ijsselstein", "lage vuursche", "nieuwegein", "odijk", "soest", "soestduinen", "soesterberg", "werkhoven", "zeist"]
        if self.city in rmn:
            self.data = RmnAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
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
                self.city, self.postcode, self.street_number, self.resources
            )
        sliedrecht = ["sliedrecht"]
        if self.city in sliedrecht:
            self.data = SliedrechtAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        spaarnelanden = ["haarlem", "spaarndam-west", "zandvoort"]
        if self.city in spaarnelanden:
            self.data = SpaarnelandenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        suez = ["arnhem", "elden", "schaarsbergen"]
        if self.city in suez:
            self.data = SuezAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        twentemilieu = ["aadorp", "almelo", "ambt delden", "beckum", "bentelo", "beuningen", "boekelo", "borne", "bornerbroek", "buurse", "de lutte", "delden", "diepenheim", "enschede", "enter", "glane", "glanerbrug", "goor", "haaksbergen", "hengelo", "hengevelde",
        "hertme", "lonneker", "losser", "markelo", "oldenzaal", "overdinkel", "st. isidorushoeve", "usselo", "wierden", "zenderen"]
        if self.city in twentemilieu:
            self.data = TwentemilieuAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        veldhoven = ["veldhoven"]
        if self.city in veldhoven:
            self.data = VeldhovenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        venlo = ["arcen", "belfeld", "lomm", "steyl", "tegelen", "velden", "venlo"]
        if self.city in venlo:
            self.data = VenloAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        venray = ["blitterswijck", "castenray", "geijsteren", "heide", "leunen", "merselo", "oirlo", "oostrum", "smakt", "venray", "veulen", "vredepeel", "wanssum", "ysselsteyn"]
        if self.city in venray:
            self.data = VenrayAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        vijfheerenlanden = ["ameide", "everdingen", "hagestein", "hei- en boeicop", "hoef en haag", "kedichem", "leerbroek", "leerdam", "lexmond", "meerkerk", "nieuwland", "oosterwijk", "ossenwaard", "schoonrewoerd", "tienhoven aan de lek", "vianen", "zijderveld"]
        if self.city in vijfheerenlanden:
            self.data = VijfheerenlandenAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        westerkwartier = ["aduard", "boerakker", "briltil", "de wilp", "den ham_" "den horn", "doezum", "enumatil", "ezinge", "feerwerd", "garnwerd", "grijpskerk", "grootegast", "jonkersvaart", "kommerzijl", "kornhorn", "lauwerzijl", "leek", "lettelbert",
        "lucaswolde", "lutjegast", "marum", "midwolde", "niebert", "niehove", "niekerk", "niezijl", "noordhorn", "noordwijk", "nuis", "oldehove", "oldekerk", "oostwold", "opende", "pieterzijl", "saaksum", "sebaldeburen", "tolbert", "visvliet", "zevenhuizen", "zuidhorn"]
        if self.city in westerkwartier:
            self.data = WesterkwartierAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        westland = ["de lier", "honselersdijk", "kwintsheul", "maasdijk", "monster", "naaldwijk", "poeldijk", "s-gravenzande", "ter heijde", "wateringen"]
        if self.city in westland:
            self.data = WestlandAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        zrd = ["aagtekerke", "aardenburg", "anna jacobapolder", "bath", "biezelinge", "biggekerke", "breskens", "cadzand", "clinge", "colijnsplaat", "dishoek", "domburg", "eede", "gapinge", "geersdijk", "graauw", "grijpskerke", "groede", "hansweert", "heikant",
        "hengstdijk", "hoofdplaat", "hulst", "ijzendijke", "kamperland", "kapelle", "kapellebrug", "kats", "kloosterzande", "kortgene", "koudekerke", "krabbendijke", "kruiningen", "kuitaart", "lamswaarde", "meliskerke", "nieuw-namen", "nieuwvliet", "oostburg",
        "oostdijk", "oostkapelle", "ossenisse", "oud-vossemeer", "poortvliet", "retranchement", "rilland", "scherpenisse", "schoondijke", "schore", "serooskerke", "sint anna ter muiden", "sint jansteen", "sint kruis", "sint philipsland", "sint-annaland", "sint-maartensdijk",
        "sluis", "stavenisse", "terhole", "tholen", "veere", "vogelwaarde", "vrouwenpolder", "waarde", "walsoorden", "waterlandkerkje", "wemeldinge", "westkapelle", "wissenkerke", "yerseke", "zoutelande", "zuidzande"]
        if self.city in zrd:
            self.data = ZrdAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )
        zuidwestfriesland = ["abbega", "allingawier", "arum", "blauwhuis", "bolsward", "bozum", "breezanddijk", "britswerd", "burgwerd", "cornwerd", "dedgum", "deersum", "edens", "exmorra", "ferwoude", "folsgare", "gaast", "gaastmeer", "gauw", "goënga", "greonterp",
        "hartwerd", "heeg", "hemelum", "hennaard", "hichtum", "hidaard", "hieslum", "hindeloopen", "hommerts", "idsegahuizum", "idzega", "ijlst", "ijsbrechtum", "indijk", "heidenschap", "itens", "jutrijp", "kimswerd", "kornwerderzand", "koudum", "koufurderrige",
        "kubaard", "loënga", "lollum", "longerhouw", "lutkewierum", "makkum", "molkwerum", "nijhuizum", "nijland", "offingawier", "oosterend", "oosterwierum", "oosthem", "oppenhuizen", "oudega", "parrega", "piaam", "pingjum", "poppingawier", "rauwerd", "rien", "roodhuis",
        "sandfirden", "scharnegoutum", "schettens", "schraard", "sijbrandaburen", "smallebrugge", "sneek", "stavoren", "terzool", "tirns", "tjalhuizum", "tjerkwerd", "uitwellingerga", "waaxens", "warns", "westhem", "wieuwerd", "witmarsum", "wolsum", "wommels", "wons",
        "workum", "woudsend", "ypecolsga", "zurich"]
        if self.city in zuidwestfriesland:
            self.data = ZuidWestFrieslandAfval().get_data(
                self.city, self.postcode, self.street_number, self.resources
            )

class AfvalinfoSensor(Entity):
    def __init__(self, data, sensor_type, date_format, timespan_in_days, locale):
        self.data = data
        self.type = sensor_type
        self.date_format = date_format
        self.timespan_in_days = timespan_in_days
        self.locale = locale
        self._name = SENSOR_PREFIX + SENSOR_TYPES[sensor_type][0]
        self._icon = SENSOR_TYPES[sensor_type][1]
        self._hidden = False
        self._state = None
        self._last_update = None
        self._days_until_collection_date = None
        self._is_collection_date_today = False
        self._year_month_day_date = None

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
        return {ATTR_YEAR_MONTH_DAY_DATE: self._year_month_day_date, ATTR_LAST_UPDATE: self._last_update, ATTR_HIDDEN: self._hidden, ATTR_DAYS_UNTIL_COLLECTION_DATE: self._days_until_collection_date, ATTR_IS_COLLECTION_DATE_TODAY: self._is_collection_date_today}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.data.update()
        waste_data = self.data.data

        try:
            if waste_data:
                if self.type in waste_data:
                    collection_date = datetime.strptime(
                        waste_data[self.type], "%Y-%m-%d"
                    ).date()

                    # Date in date format "%Y-%m-%d"
                    self._year_month_day_date = str(collection_date)

                    if collection_date:
                        # Set the values of the sensor
                        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")

                        # Is the collection date today?
                        self._is_collection_date_today = date.today() == collection_date

                        # Days until collection date
                        delta = collection_date - date.today()
                        self._days_until_collection_date = delta.days

                        # Only show the value if the date is lesser than or equal to (today + timespan_in_days)
                        if collection_date <= date.today() + relativedelta(days=int(self.timespan_in_days)):
                            #if the date does not contain a named day or month, return the date as normal
                            if (self.date_format.find('a') == -1 and self.date_format.find('A') == -1
                            and self.date_format.find('b') == -1 and self.date_format.find('B') == -1):
                                self._state = collection_date.strftime(self.date_format)
                            #else convert the named values to the locale names
                            else:
                                edited_date_format = self.date_format.replace('%a', 'EEE')
                                edited_date_format = edited_date_format.replace('%A', 'EEEE')
                                edited_date_format = edited_date_format.replace('%b', 'MMM')
                                edited_date_format = edited_date_format.replace('%B', 'MMMM')

                                #half babel, half date string... something like EEEE 04-MMMM-2020
                                half_babel_half_date = collection_date.strftime(edited_date_format)

                                #replace the digits with qquoted digits 01 --> '01'
                                half_babel_half_date = re.sub(r"(\d+)", r"'\1'", half_babel_half_date)
                                #transform the EEE, EEEE etc... to a real locale date, with babel
                                locale_date = format_date(collection_date, half_babel_half_date, locale=self.locale)

                                self._state = locale_date
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
            self._year_month_day_date = None
            self._is_collection_date_today = False
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
