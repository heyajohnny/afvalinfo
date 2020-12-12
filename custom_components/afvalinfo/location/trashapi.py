from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import requests


class TrashApiAfval(object):
    def get_data(self, location, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["trashapi"][0].format(
                location, postcode, street_number
            )

            r = requests.get(url=API_ENDPOINT)
            dataList = r.json()

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            #_LOGGER.warning(dataList)

            for data in dataList:

                # find gft.
                if "gft" in resources and data["name"].lower() == "gft":
                    waste_dict["gft"] = data["date"].split("T")[0]
                # find papier
                if "papier" in resources and data["name"].lower() == "papier":
                    waste_dict["papier"] = data["date"].split("T")[0]
                # find pbd.
                if "pbd" in resources and data["name"].lower() == "pbd":
                    waste_dict["pbd"] = data["date"].split("T")[0]
                # find restafval.
                if "restafval" in resources and data["name"].lower() == "restafval":
                    waste_dict["restafval"] = data["date"].split("T")[0]
                # find textiel
                if "textiel" in resources and data["name"].lower() == "textiel":
                    waste_dict["textiel"] = data["date"].split("T")[0]

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
