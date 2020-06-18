from ..const.const import (
    SENSOR_LOCATIONS_TO_COMPANY_CODE,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime
import urllib.request
import urllib.error
import requests

from datetime import date
from dateutil.relativedelta import relativedelta


class XimmioAfval(object):
    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            location = ""
            acv = ["ede", "renkum", "renswoude", "veenendaal", "wageningen"]
            if city in acv:
                location = "acv"
            almere = ["almere"]
            if city in almere:
                location = "almere"
            area = ["coevorden", "emmen", "hoogeveen"]
            if city in area:
                location = "area"
            bar = ["barendrecht", "albrandswaard", "ridderkerk"]
            if city in bar:
                location = "bar"
            hellendoorn = ["hellendoorn"]
            if city in hellendoorn:
                location = "hellendoorn"
            meerlanden = ["aalsmeer", "bloemendaal", "diemen", "haarlemmermeer", "heemstede", "hillegom", "lisse", "noordwijk"]
            if city in meerlanden:
                location = "meerlanden"
            meppel = ["meppel"]
            if city in meppel:
                location = "meppel"
            nissewaard = ["nissewaard"]
            if city in nissewaard:
                location = "nissewaard"
            twentemilieu = ["almelo", "borne", "enschede", "haaksbergen", "hengelo", "hof van twente", "losser", "oldenzaal", "wierden"]
            if city in twentemilieu:
                location = "twentemilieu"
            vijfheerenlanden = ["vijfheerenlanden"]
            if city in vijfheerenlanden:
                location = "vijfheerenlanden"
            waardlanden = ["gorinchem", "hardinxveld-giessendam", "molenlanden"]
            if city in waardlanden:
                location = "waardlanden"

            # Get companyCode for this location
            companyCode = SENSOR_LOCATIONS_TO_COMPANY_CODE[location]

            #######################################################
            # First request: get uniqueId and community
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["ximmio"][0]

            data = {
                "postCode": postcode,
                "houseNumber": street_number,
                "companyCode": companyCode,
            }

            # sending post request and saving response as response object
            r = requests.post(url=API_ENDPOINT, data=data)

            # extracting response json
            uniqueId = r.json()["dataList"][0]["UniqueId"]
            community = r.json()["dataList"][0]["Community"]

            #######################################################
            # Second request: get the dates
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["ximmio"][1]

            today = date.today()
            todayNextYear = today + relativedelta(years=1)

            data = {
                "companyCode": companyCode,
                "startDate": today,
                "endDate": todayNextYear,
                "community": community,
                "uniqueAddressID": uniqueId,
            }

            r = requests.post(url=API_ENDPOINT, data=data)

            dataList = r.json()["dataList"]

            for data in dataList:
                # _pickupTypeText = "GREEN"
                if "gft" in resources:
                    if data["_pickupTypeText"] == "GREEN":
                        waste_dict["gft"] = data["pickupDates"][0].split("T")[0]
                    if "gft" not in waste_dict or len(waste_dict["gft"]) == 0:
                        if data["_pickupTypeText"] == "GREENGREY":
                            waste_dict["gft"] = data["pickupDates"][0].split("T")[0]
                # _pickupTypeText = "GREY"
                if "restafval" in resources:
                    if data["_pickupTypeText"] == "GREY":
                        waste_dict["restafval"] = data["pickupDates"][0].split("T")[0]
                    if "restafval" not in waste_dict or len(waste_dict["restafval"]) == 0:
                        if data["_pickupTypeText"] == "GREENGREY":
                            waste_dict["restafval"] = data["pickupDates"][0].split("T")[0]
                    if "restafval" not in waste_dict or len(waste_dict["restafval"]) == 0:
                        if data["_pickupTypeText"] == "GREYPACKAGES":
                            waste_dict["restafval"] = data["pickupDates"][0].split("T")[0]
                # _pickupTypeText = "PAPER"
                if "papier" in resources:
                    if data["_pickupTypeText"] == "PAPER":
                        waste_dict["papier"] = data["pickupDates"][0].split("T")[0]
                # _pickupTypeText = "PLASTIC"
                if "pbd" in resources:
                    if data["_pickupTypeText"] == "PACKAGES":
                        waste_dict["pbd"] = data["pickupDates"][0].split("T")[0]
                    if "pbd" not in waste_dict:
                        if data["_pickupTypeText"] == "GREY":
                            waste_dict["pbd"] = data["pickupDates"][0].split("T")[0]
                    if "pbd" not in waste_dict:
                        if data["_pickupTypeText"] == "PLASTIC":
                            waste_dict["pbd"] = data["pickupDates"][0].split("T")[0]
                    if "pbd" not in waste_dict or len(waste_dict["pbd"]) == 0:
                        if data["_pickupTypeText"] == "GREYPACKAGES":
                            waste_dict["pbd"] = data["pickupDates"][0].split("T")[0]
                # _pickupTypeText = "TEXTILE"
                if "textiel" in resources:
                    if data["_pickupTypeText"] == "TEXTILE":
                        waste_dict["textiel"] = data["pickupDates"][0].split("T")[0]
                    if "textiel" not in waste_dict or len(waste_dict["textiel"]) == 0:
                        if data["_pickupTypeText"] == "VET":
                            waste_dict["textiel"] = data["pickupDates"][0].split("T")[0]
                # _pickupTypeText = "TREE" = kerstbomen

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
