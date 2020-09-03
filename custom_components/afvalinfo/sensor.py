#!/usr/bin/env python3
"""
Sensor component for Afvalinfo
Author: Johnny Visser

ToDo: Add huisnummer toevoeging
ToDo: Fix all the next year problems
ToDo: Add the following gemeenten:
PDF: #####################################################################################################
Bergen Limburg                  bergen.nl/home/afval_44490/item/afvalkalender-2020_38953.html (PDF)
Dantumadeel                     https://www.dantumadiel.frl/afvalkalender Woont u in het voormalige Ferwerderadiel dan wordt het afval opgehaald door Omrin (PDF)
Delfzijl                        https://www.delfzijl.nl/inwoners/afvalkalender_43586/ (PDF)
Edam-Volendam                   https://www.edam-volendam.nl/portal-home/inzamelkalender_43466/ (PDF)
Eemnes                          https://www.eemnes.nl/inwoners/Afval/Afvalwijzer (PDF)
Gennep                          https://www.gennep.nl/document.php?m=28&fileid=98242&f=834a3177a76c30293e3e9d1c200729fb&attachment=0&c=34148 (PDF)
Goes                            https://afvalkalender.goes.nl/4461AB-2.html (PDF)
Hellevoetsluis                  https://www.hellevoetsluis.nl/Inwoners/WONEN_EN_LEEFOMGEVING/Afval/Afvalkalender (PDF)
Landerd                         https://www.landerd.nl/inwoners-en-ondernemers/afval/afvalkalender/pdf/2020 (PDF)
Landsmeer                       https://admin.sduconnect.nl/linked_links/1577977473Afvalkalender_2020_DEF.pdf (PDF)
Middelburg                      https://www.middelburg.nl/Inwoners/Afval/Ophaaldagen_huisvuil (PDF)
Mook en Middelaar               https://www.mookenmiddelaar.nl/inwoner/afval-en-duurzaamheid_42542/item/afvalkalender-2020_40888.html (PDF)
Oegstgeest                      https://www.oegstgeest.nl/fileadmin/editor/Documenten/Inwoners/Alles_over_afval/afvalkalender_2020_v8.pdf (PDF)
Oostzaan                        https://www.oostzaan.nl/mozard/document/docnr/1182761/bijlage%20-%20afvalkalender%20Oostzaan%202020%20-%20met%20wijkindeling (PDF)
Ouder-Amstel                    https://www.ouder-amstel.nl/Home/Nieuws_en_actualiteiten/Nieuws/Alle_nieuwsberichten_2020/April/Data_inzameling_afval (PDF)
Reusel-De Mierden               https://www.reuseldemierden.nl/document.php?m=25&fileid=123208&f=3e3d90c015a9b15ffc98c993c8e4e9da&attachment=0&c=40975 (PDF)
Rozendaal                       https://www.rozendaal.nl/dsresource?objectid=d7a004f0-ff97-490a-8837-1b66e5bc11e1&type=org (PDF)
Uithoorn                        https://www.uithoorn.nl/Home/Afval/Afvalkalender (PDF)
Vlissingen                      https://www.vlissingen.nl/inwoner/afval-en-milieu/afval/huishoudelijk-afval-en-afvalkalender.html (PDF)
Zundert                         https://www.zundert.nl/afval-en-milieustraat/afvalkalender-2020.html (PDF)
Steenbergen                     https://www.gemeente-steenbergen.nl/inwoners_overzicht/afval/ (PDF)
Vlieland                        https://www.vlieland.nl/v-zelf-regelen/producten_42533/product/afval-huishoudelijk-afval_17.html (PDF)
#############################################################################################################
Buurt / dorp indeling of geen kalender: #####################################################################
Weert                           https://www.weert.nl/huisvuil-duobak-en-ophaaldagen
Texel                           https://www.texel.nl/mozard/!suite86.scherm0325?mVrg=5059
Maassluis                       https://www.maassluis.nl/wonen-verkeer-en-veiligheid/afvalinzameling_43871/
Voorschoten                     https://www.voorschotenmaakthetverschil.nl/ 2251dn 121
Nederweert                      https://www.nederweert.nl/inwoners/huisvuil-2019_45554/
Amsterdam                       Geen kalender, alleen inleverpunten
Schiermonnikoog                 Geen kalender
############################################################################################################
############################################################################################################
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
    CONF_LOCATION,
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
from .location.deafvalapp import DeAfvalAppAfval
from .location.westerkwartier import WesterkwartierAfval
from .location.westland import WestlandAfval
from .location.rova import RovaAfval
from .location.venlo import VenloAfval
from .location.hvc import HvcAfval
from .location.alkmaar import AlkmaarAfval
from .location.alphenaandenrijn import AlphenAanDenRijnAfval
from .location.mijnafvalwijzer import MijnAfvalWijzerAfval
from .location.suez import SuezAfval
from .location.omrin import OmrinAfval
from .location.defriesemeren import DeFrieseMerenAfval
from .location.veldhoven import VeldhovenAfval
from .location.venray import VenrayAfval
from .location.gad import GadAfval
from .location.zuidwestfriesland import ZuidWestFrieslandAfval
from .location.blink import BlinkAfval
from .location.spaarnelanden import SpaarnelandenAfval
from .location.cyclus import CyclusAfval
from .location.circulusberkel import CirculusBerkelAfval
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
from .location.avalex import AvalexAfval
from .location.ximmio import XimmioAfval
from .location.cranendonck import CranendonckAfval
from .location.peelenmaas import PeelEnMaasAfval
from .location.afvalstoffendienstkalender import AfvalstoffendienstkalenderAfval
from .location.schouwenduiveland import SchouwenDuivelandAfval
from .location.waalre import WaalreAfval
from .location.groningen import GroningenAfval
from .location.beesel import BeeselAfval
from .location.hoekschewaard import HoekscheWaardAfval
from .location.katwijk import KatwijkAfval
from .location.uden import UdenAfval
from .location.westerwolde import WesterwoldeAfval

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
        vol.Optional(CONF_CITY, default=""): cv.string,
        vol.Optional(CONF_LOCATION, default="sliedrecht"): cv.string,
        vol.Required(CONF_POSTCODE, default="3361AB"): cv.string,
        vol.Required(CONF_STREET_NUMBER, default="1"): cv.string,
        vol.Optional(CONF_DATE_FORMAT, default = "%d-%m-%Y"): cv.string,
        vol.Optional(CONF_TIMESPAN_IN_DAYS, default="365"): cv.string,
        vol.Optional(CONF_LOCALE, default = "en"): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup Afvalinfo sensor")

    location = config.get(CONF_CITY).lower().strip()
    if len(location) == 0:
        location = config.get(CONF_LOCATION).lower().strip()
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

        data = AfvalinfoData(location, postcode, street_number, resourcesMinusTodayAndTomorrow)
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
    def __init__(self, location, postcode, street_number, resources):
        self.data = None
        self.location = location
        self.postcode = postcode
        self.street_number = street_number
        self.resources = resources

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Updating Waste collection dates")
        afvalstoffendienstkalender = ["haaren", "heusden", "oisterwijk", "s-hertogenbosch", "vught"]
        if self.location in afvalstoffendienstkalender:
            self.data = AfvalstoffendienstkalenderAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        alkmaar = ["alkmaar"]
        if self.location in alkmaar:
            self.data = AlkmaarAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        alphenaandenrijn = ["alphen aan den rijn"]
        if self.location in alphenaandenrijn:
            self.data = AlphenAanDenRijnAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        avalex = ["delft", "leidschendam-voorburg", "midden-delfland", "pijnacker-nootdorp", "rijswijk", "wassenaar"]
        if self.location in avalex:
            self.data = AvalexAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        beesel = ["beesel"]
        if self.location in beesel:
            self.data = BeeselAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        berkelland = ["berkelland"]
        if self.location in berkelland:
            self.data = BerkellandAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        blink = ["asten", "deurne", "gemert-bakel", "heeze-leende", "laarbeek", "nuenen", "someren"]
        if self.location in blink:
            self.data = BlinkAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        borsele = ["borsele"]
        if self.location in borsele:
            self.data = BorseleAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        circulusberkel = ["apeldoorn", "bronckhorst", "brummen", "deventer", "doesburg", "epe", "lochem", "voorst", "zutphen"]
        if self.location in circulusberkel:
            self.data = CirculusBerkelAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        cranendonck = ["cranendonck"]
        if self.location in cranendonck:
            self.data = CranendonckAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        cyclus = ["bodegraven-reeuwijk", "gouda", "kaag en braassem", "krimpenerwaard", "montfoort", "nieuwkoop", "waddinxveen", "zuidplas"]
        if self.location in cyclus:
            self.data = CyclusAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        dar = ["berg en dal", "beuningen", "druten", "heumen", "nijmegen", "wijchen"]
        if self.location in dar:
            self.data = DarAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        deafvalapp = ["boekel", "boxmeer", "buren", "cuijk", "culemborg", "echt-susteren", "grave", "helmond", "maasdriel", "mill en sint hubert", "neder-betuwe", "sint anthonis", "son en breugel", "terneuzen", "tiel", "west betuwe", "west maas en waal", "zaltbommel"]
        if self.location in deafvalapp:
            self.data = DeAfvalAppAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        denhaag = ["den haag"]
        if self.location in denhaag:
            self.data = DenHaagAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        defriesemeren = ["de friese meren"]
        if self.location in defriesemeren:
            self.data = DeFrieseMerenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        drimmelen = ["drimmelen"]
        if self.location in drimmelen:
            self.data = DrimmelenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        gad = ["blaricum", "gooise meren", "hilversum", "huizen", "laren", "weesp", "wijdemeren"]
        if self.location in gad:
            self.data = GadAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        goereeoverflakkee = ["goeree-overflakkee"]
        if self.location in goereeoverflakkee:
            self.data = GoereeOverflakkeeAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        groningen = ["groningen", "het hogeland bw", "loppersum"]
        if self.location in groningen:
            self.data = GroningenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        hoekschewaard = ["hoeksche waard"]
        if self.location in hoekschewaard:
            self.data = HoekscheWaardAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        hvc = ["alblasserdam", "bergen", "beverwijk", "den helder", "dordrecht", "drechterland", "enkhuizen", "hendrik-ido-ambacht", "heemskerk", "hollands kroon", "hoorn", "koggenland", "lelystad", "medemblik", "noordoostpolder", "opmeer", "papendrecht", "schagen", "stede broec", "velsen", "wormerland",
        "zaanstad", "zeewolde", "zwijndrecht"]
        if self.location in hvc:
            self.data = HvcAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        irado = ["capelle aan den ijssel", "schiedam", "vlaardingen"]
        if self.location in irado:
            self.data = IradoAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        katwijk = ["katwijk"]
        if self.location in katwijk:
            self.data = KatwijkAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        middendrenthe = ["midden-drenthe"]
        if self.location in middendrenthe:
            self.data = MiddenDrentheAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        mijnafvalwijzer = ["aa en hunze", "alphen-chaam", "assen", "altena", "amstelveen", "baarle-nassau", "barneveld", "beek", "beekdaelen", "bergeijk", "bergen op zoom", "bernheze", "best", "bladel", "borger-odoorn", "boxtel", "breda", "brielle", "castricum", "de ronde venen", "de wolden", "de bilt",
        "doetinchem", "dongen", "dronten", "duiven", "eersel", "eindhoven", "elburg", "ermelo", "etten-leur", "geertruidenberg", "geldrop-mierlo", "gilze en rijen", "goirle", "halderberge", "harderwijk", "heerhugowaard", "heiloo", "hilvarenbeek", "horst aan de maas", "houten", "kampen", "krimpen aan den ijssel",
        "langedijk", "lansingerland", "leiden", "leiderdorp", "leudal", "leusden", "lingewaard", "loon op zand", "lopik", "maasgouw", "meierijstad", " midden-groningen", "moerdijk", "nijkerk", "noordenveld", "nunspeet", "oirschot", "oldambt", "oldebroek", "oosterhout", "oss", "oude ijsselstreek", "oude pekela",
        "putten", "oudewater", "overbetuwe", "rheden", "rhenen", "rijssen-holten", "roerdalen", "roermond", "roosendaal", "rotterdam", "rucphen", "scherpenzeel", "sint-michielsgestel", "sittard-geleen", "smallingerland", "stadskanaal", "stein", "stichtse vecht", "teylingen", "tilburg", "tynaarlo", "uitgeest",
        "utrecht", "utrechtse heuvelrug", "valkenswaard", "veendam", "waalwijk", "waterland", "wijk bij duurstede", "westervoort", "westvoorne", "woensdrecht", "woerden", "zevenaar", "zoetermeer", "zoeterwoude"]
        if self.location in mijnafvalwijzer:
            self.data = MijnAfvalWijzerAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        omrin = ["achtkarspelen", "ameland", "appingedam", "dantumadeel f", "harlingen", "heerenveen", "het hogeland", "leeuwarden", "noardeast fryslan", "ooststellingwerf", "opsterland", "terschelling", "tietjerksteradeel", "waadhoeke", "weststellingwerf"]
        if self.location in omrin:
            self.data = OmrinAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        peelenmaas = ["peel en maas"]
        if self.location in peelenmaas:
            self.data = PeelEnMaasAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        purmerend = ["beemster", "purmerend"]
        if self.location in purmerend:
            self.data = PurmerendAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        rd4 = ["brunssum", "eijsden-margraten", "gulpen-wittem", "heerlen", "kerkrade", "landgraaf", "maastricht", "meerssen", "simpelveld", "vaals", "valkenburg aan de geul", "voerendaal"]
        if self.location in rd4:
            self.data = Rd4Afval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        rmn = ["baarn", "bunnik", "ijsselstein", "nieuwegein", "soest", "zeist"]
        if self.location in rmn:
            self.data = RmnAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        rova = ["aalten", "amersfoort", "bunschoten", "dalfsen", "dinkelland", "hardenberg", "hattem", "heerde", "olst-wijhe", "ommen", "oost gelre", "raalte", "staphorst", "steenwijkerland", "tubbergen", "twenterand", "urk", "westerveld", "winterswijk",
        "woudenberg", "zwartewaterland", "zwolle"]
        if self.location in rova:
            self.data = RovaAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        schouwenduiveland = ["schouwen-duiveland"]
        if self.location in schouwenduiveland:
            self.data = SchouwenDuivelandAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        sliedrecht = ["sliedrecht"]
        if self.location in sliedrecht:
            self.data = SliedrechtAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        spaarnelanden = ["haarlem", "zandvoort"]
        if self.location in spaarnelanden:
            self.data = SpaarnelandenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        suez = ["arnhem"]
        if self.location in suez:
            self.data = SuezAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        uden = ["uden"]
        if self.location in uden:
            self.data = UdenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        veldhoven = ["veldhoven"]
        if self.location in veldhoven:
            self.data = VeldhovenAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        venlo = ["venlo"]
        if self.location in venlo:
            self.data = VenloAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        venray = ["venray"]
        if self.location in venray:
            self.data = VenrayAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        waalre = ["waalre"]
        if self.location in waalre:
            self.data = WaalreAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        westerkwartier = ["westerkwartier"]
        if self.location in westerkwartier:
            self.data = WesterkwartierAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        westerwolde = ["westerwolde"]
        if self.location in westerwolde:
            self.data = WesterwoldeAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        westland = ["westland"]
        if self.location in westland:
            self.data = WestlandAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        ximmio = ["aalsmeer", "albrandswaard", "almelo", "almere", "barendrecht", "bloemendaal", "borne", "coevorden", "diemen", "ede", "emmen", "enschede", "gorinchem", "haaksbergen", "haarlemmermeer", "hardinxveld-giessendam", "heemstede", "hellendoorn",
        "hengelo", "hillegom", "hof van twente", "hoogeveen", "lisse", "losser", "meppel", "molenlanden", "nissewaard", "noordwijk", "oldenzaal", "renkum", "renswoude", "ridderkerk", "veenendaal", "vijfheerenlanden", "wageningen", "wierden"]
        if self.location in ximmio:
            self.data = XimmioAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        zrd = ["hulst", "kapelle", "noord-beveland", "reimerswaal", "sluis", "tholen", "veere"]
        if self.location in zrd:
            self.data = ZrdAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
            )
        zuidwestfriesland = ["zuidwest-friesland"]
        if self.location in zuidwestfriesland:
            self.data = ZuidWestFrieslandAfval().get_data(
                self.location, self.postcode, self.street_number, self.resources
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
