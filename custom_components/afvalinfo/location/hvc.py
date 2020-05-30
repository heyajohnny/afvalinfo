from ..const.const import (
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime, date
import urllib.request
import urllib.error
import requests

class HvcAfval(object):
    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            # First request: get bagid
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["hvc"][0].format(
                postcode, street_number
            )
            r = requests.get(url=API_ENDPOINT)
            bagid = r.json()[0]["bagId"]

            # Second request: get the dates
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["hvc"][1].format(
                bagid, date.today().year
            )
            r = requests.get(url=API_ENDPOINT)
            dataList = r.json()

            for data in dataList:
                # afvalstroom_id 2 = restafval
                if "restafval" in resources:
                    if data["afvalstroom_id"] == 2:
                        if(not "restafval" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["restafval"] = data["ophaaldatum"]
                # afvalstroom_id 3 = papier
                if "papier" in resources:
                    if data["afvalstroom_id"] == 3:
                        if(not "papier" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["papier"] = data["ophaaldatum"]
                # afvalstroom_id 5 = gft
                if "gft" in resources:
                    if data["afvalstroom_id"] == 5:
                        if(not "gft" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["gft"] = data["ophaaldatum"]
                # afvalstroom_id 6 = pbd
                if "pbd" in resources:
                    if data["afvalstroom_id"] == 6:
                        if(not "pbd" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["pbd"] = data["ophaaldatum"]
                # afvalstroom_id 8 = textiel
                if "textiel" in resources:
                    if data["afvalstroom_id"] == 8:
                        if(not "textiel" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["textiel"] = data["ophaaldatum"]
            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
