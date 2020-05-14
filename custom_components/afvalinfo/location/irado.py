from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import http.cookiejar
import json


class IradoAfval(object):
    def get_date_from_afvaltype(self, data, afvaltype, afvalnaam):
        try:
            html = data.find("div", {"class": "avk-block-row pickup-type-item " + str(afvaltype) + " active"})
            #get innerHTML
            html = html.decode_contents(formatter="html")
            date = html.split("<")[0].strip()
            day = date.split()[1]
            month = MONTH_TO_NUMBER[date.split()[2]]
            year = str(
                datetime.today().year
                if datetime.today().month <= int(month)
                else datetime.today().year + 1
            )
            return year + "-" + month + "-" + day
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""


    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Storing cookies in cj variable
            cj = http.cookiejar.CookieJar()

            # Defining a handler for later http operations with cookies(cj).
            op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            url = SENSOR_LOCATIONS_TO_URL["irado"][0]

            data = {
                "appointment_zipcode": postcode[:4],
                "appointment_zipcode_suffix": postcode[4:],
                "appointment_housenumber": street_number,
                "appointment_housenumber_suffix": "",
                "wsa_calendar": "364b570c83"
            }

            postdata = urllib.parse.urlencode(data).encode()

            # sending post request and saving response as response object
            request = urllib.request.Request(url, postdata)
            #open the response object
            response = op.open(request)

            #read the data
            html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            nextPickup = soup.find("div", {"class": ['avk-block avk-next-pickup']})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(nextPickup, "pickup-type-item-rest", "restafval")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(nextPickup, "pickup-type-item-gft", "gft")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(nextPickup, "pickup-type-item-papier", "papier")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(nextPickup, "pickup-type-item-kunststof", "pbd")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False