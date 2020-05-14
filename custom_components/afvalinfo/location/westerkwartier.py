from ..const.const import (
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime
from datetime import date
import urllib.request
import urllib.error
import requests


class WesterkwartierAfval(object):

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # first call to save cookie
            url = SENSOR_LOCATIONS_TO_URL["westerkwartier"][0].format(
                postcode, street_number
            )

            # sending post request and saving response as response object
            r = requests.post(url=url)

            items = r.json()["items"]

            today = date.today()

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            for item in items:
                if datetime.strptime(item["date"], '%Y-%m-%d').date() >= today:
                    if "restafval" in resources:
                        if item["type"] == "rest" and not "restafval" in waste_dict:
                            waste_dict["restafval"] = item["date"]
                    if "gft" in resources:
                        if item["type"] == "gft" and not "gft" in waste_dict:
                            waste_dict["gft"] = item["date"]
                    # milb = milieuboer = papier, textiel, gft (maar gft staat ook al los als gft aangegeven)
                    if item["type"] == "milb" and not "papier" in waste_dict:
                        if "papier" in resources:
                            waste_dict["papier"] = item["date"]
                        if "textiel" in resources:
                            waste_dict["textiel"] = item["date"]
            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
