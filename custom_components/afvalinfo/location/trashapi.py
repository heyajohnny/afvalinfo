from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import date, datetime, timedelta
import urllib.request
import urllib.error
import requests


class TrashApiAfval(object):
    def get_data(
        self,
        location,
        postcode,
        street_number,
        street_number_suffix,
        diftar_code,
        resources,
    ):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["trashapi"][0].format(
                location, postcode, street_number, street_number_suffix, diftar_code
            )

            r = requests.get(url=API_ENDPOINT)
            dataList = r.json()

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            # _LOGGER.warning(dataList)

            for data in dataList:

                # find gft.
                if "gft" in resources and data["name"].lower() == "gft":
                    waste_dict["gft"] = data["date"].split("T")[0]
                # find kerstboom.
                if "kerstboom" in resources and data["name"].lower() == "kerstboom":
                    waste_dict["kerstboom"] = data["date"].split("T")[0]
                # find papier
                if "papier" in resources and data["name"].lower() == "papier":
                    waste_dict["papier"] = data["date"].split("T")[0]
                # find pbd.
                if "pbd" in resources and data["name"].lower() == "pbd":
                    waste_dict["pbd"] = data["date"].split("T")[0]
                # find restafval.
                if "restafval" in resources and data["name"].lower() == "restafval":
                    if (
                        date.today()
                        < datetime.strptime(
                            data["date"].split("T")[0], "%Y-%m-%d"
                        ).date()
                    ):
                        waste_dict["restafval"] = data["date"].split("T")[0]
                    else:
                        waste_dict["restafvaldiftardate"] = data["date"].split("T")[0]
                        waste_dict["restafvaldiftarcollections"] = data["totalThisYear"]
                # find takken
                if "takken" in resources and data["name"].lower() == "takken":
                    waste_dict["takken"] = data["date"].split("T")[0]
                # find textiel
                if "textiel" in resources and data["name"].lower() == "textiel":
                    waste_dict["textiel"] = data["date"].split("T")[0]

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
        except Exception as exc:
            _LOGGER.error(
                """Error occurred. Please check the address with postcode: %r and huisnummer: %r%r on the website of your local waste collector in the gemeente: %r. It's probably a faulty address or the website of the waste collector is unreachable. If the address is working on the website of the local waste collector and this error still occured, please report the issue in the Github repository https://github.com/heyajohnny/afvalinfo with details of the location that isn't working""",
                postcode,
                street_number,
                street_number_suffix,
                location,
            )
            return False
