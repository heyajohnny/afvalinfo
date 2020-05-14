from ..const.const import (
    SENSOR_LOCATIONS_TO_COMPANY_CODE,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)

from datetime import datetime, date
import urllib.request
import urllib.error
import requests

from dateutil.relativedelta import relativedelta


class VijfheerenlandenAfval(object):
    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            # Get companyCode for this location
            companyCode = SENSOR_LOCATIONS_TO_COMPANY_CODE["vijfheerenlanden"]

            #######################################################
            # First request: get uniqueId and community
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["vijfheerenlanden"][0]

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
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["vijfheerenlanden"][1]

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
                # pickupType 0 = restafval
                if "restafval" in resources:
                    if data["pickupType"] == 0:
                        waste_dict["restafval"] = data["pickupDates"][0].split("T")[0]
                # pickupType 1 = gft
                if "gft" in resources:
                    if data["pickupType"] == 1:
                        waste_dict["gft"] = data["pickupDates"][0].split("T")[0]
                # pickupType 2 = papier
                if "papier" in resources:
                    if data["pickupType"] == 2:
                        waste_dict["papier"] = data["pickupDates"][0].split("T")[0]
                # pickupType 4 = textiel
                if "textiel" in resources:
                    if data["pickupType"] == 4:
                        waste_dict["textiel"] = data["pickupDates"][0].split("T")[0]
                # pickupType 10 = pbd
                if "pbd" in resources:
                    if data["pickupType"] == 10:
                        waste_dict["pbd"] = data["pickupDates"][0].split("T")[0]

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
