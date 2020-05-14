from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_COMPANY_CODE,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import requests

from datetime import date
from dateutil.relativedelta import relativedelta


class WestlandAfval(object):
    def get_date_from_afvaltype(self, html, afvaltype, afvalnaam):
        try:
            tag = BeautifulSoup(html, "html.parser").find(
                "li", {"class": afvaltype}
            )
            date = BeautifulSoup(str(tag), "html.parser").find(
                "span", {"class": "text dag"}
            )
            # get the value of the span
            date = date.string

            day = date.split()[1]
            month = MONTH_TO_NUMBER[date.split()[2]]
            year = date.split()[3]
            return year + "-" + month + "-" + day
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            #######################################################
            # First request:
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["westland"][0]

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }

            data = {
                "postcode": postcode,
                "query": "",
                "huisnummer": street_number
            }

            # Make a request. do not check certificate (verify=False), of you do verify, it fails
            r = requests.post(url=API_ENDPOINT, headers=headers, data=data, verify=False)

            # extracting response json
            html = r.json()["html"]

            # find gft
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(html, "soort-groen", "gft")
            # find papier
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(html, "soort-papier", "papier")
            # find restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(html, "soort-grijs", "restafval")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
