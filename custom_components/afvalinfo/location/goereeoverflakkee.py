from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime
import urllib.request
import urllib.error
import requests
import json

from datetime import date
from dateutil.relativedelta import relativedelta


class GoereeOverflakkeeAfval(object):
    def get_date_from_afvaltype(self, data, afvalnaam):
        try:
            date = data["datum"]
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
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            #######################################################
            # First request
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["goereeoverflakkee"][0].format(
                postcode, street_number
            )

            # sending get request
            r = requests.get(url=API_ENDPOINT)

            containers = r.content[1:]
            containers = containers[:len(containers)-1]

            jsonResult = json.loads(containers)["containers"][0]["container"]

            for data in jsonResult:
                if "gft" in resources:
                    if data["class"] == "ak_gft" and "gft" not in waste_dict:
                        waste_dict["gft"] = self.get_date_from_afvaltype(data, "gft")
                if "restafval" in resources:
                    if data["class"] == "ak_rest" and "restafval" not in waste_dict:
                        waste_dict["restafval"] = self.get_date_from_afvaltype(data, "restafval")
                if "papier" in resources:
                    if data["class"] == "ak_papier" and "papier" not in waste_dict:
                        waste_dict["papier"] = self.get_date_from_afvaltype(data, "papier")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
