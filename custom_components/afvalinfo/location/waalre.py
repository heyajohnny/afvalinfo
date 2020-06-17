from ..const.const import (
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime, date
import urllib.request
import urllib.error
import requests

class WaalreAfval(object):
    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            # First request: get bagid
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["waalre"][0].format(
                postcode, street_number
            )
            r = requests.get(url=API_ENDPOINT)
            bagid = r.json()[0]["bagId"]

            # Second request: get the dates
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["waalre"][1].format(
                bagid, date.today().year
            )
            r = requests.get(url=API_ENDPOINT)
            dataList = r.json()

            for data in dataList:

                # afvalstroom_id 92 = pbd
                if "pbd" in resources:
                    if data["afvalstroom_id"] == 92:
                        if(not "pbd" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["pbd"] = data["ophaaldatum"]

                # afvalstroom_id 3 = gft
                if "gft" in resources:
                    if data["afvalstroom_id"] == 3:
                        if(not "gft" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["gft"] = data["ophaaldatum"]

                # afvalstroom_id 87 = papier
                if "papier" in resources:
                    if data["afvalstroom_id"] == 87:
                        if(not "papier" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["papier"] = data["ophaaldatum"]


                # afvalstroom_id 101 = restafval
                if "restafval" in resources:
                    if data["afvalstroom_id"] == 101:
                        if(not "restafval" in waste_dict and datetime.strptime(data["ophaaldatum"], "%Y-%m-%d").date() >= date.today()):
                            waste_dict["restafval"] = data["ophaaldatum"]


            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
