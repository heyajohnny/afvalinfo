from ..const.const import (
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import date, datetime, timedelta
import urllib.request
import urllib.error
import requests
import asyncio


class TrashApiAfval(object):
    async def get_data(
        self,
        location,
        postcode,
        street_number,
        street_number_suffix,
        district,
        diftar_code,
        get_whole_year,
        resources,
        get_cleanprofs_data,
    ):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            API_ENDPOINT = SENSOR_LOCATIONS_TO_URL["trashapi"][0].format(
                location,
                postcode,
                street_number,
                street_number_suffix,
                district,
                diftar_code,
                get_whole_year,
                get_cleanprofs_data,
            )

            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(None, requests.get, API_ENDPOINT)
            r = await future

            # r = await requests.get(url=API_ENDPOINT, timeout=10)
            dataList = r.json()

            # Place all possible values in the dictionary even if they are not necessary
            waste_array = []

            # _LOGGER.warning(dataList)

            for data in dataList:
                if (
                    (
                        "cleanprofsgft" in resources
                        and data["name"].lower() == "cleanprofsgft"
                    )
                    or (
                        "cleanprofspbd" in resources
                        and data["name"].lower() == "cleanprofspbd"
                    )
                    or (
                        "cleanprofsrestafval" in resources
                        and data["name"].lower() == "cleanprofsrestafval"
                    )
                    or ("gft" in resources and data["name"].lower() == "gft")
                    or ("grofvuil" in resources and data["name"].lower() == "grofvuil")
                    or ("kca" in resources and data["name"].lower() == "kca")
                    or (
                        "kerstboom" in resources and data["name"].lower() == "kerstboom"
                    )
                    or ("papier" in resources and data["name"].lower() == "papier")
                    or ("pbd" in resources and data["name"].lower() == "pbd")
                    or ("takken" in resources and data["name"].lower() == "takken")
                    or ("textiel" in resources and data["name"].lower() == "textiel")
                ):
                    waste_array.append(
                        {data["name"].lower(): data["date"].split("T")[0]}
                    )
                # find restafval and diftar.
                if "restafval" in resources and data["name"].lower() == "restafval":
                    if (
                        date.today()
                        <= datetime.strptime(
                            data["date"].split("T")[0], "%Y-%m-%d"
                        ).date()
                    ):
                        waste_array.append(
                            {data["name"].lower(): data["date"].split("T")[0]}
                        )
                    else:
                        waste_array.append(
                            {"restafvaldiftardate": data["date"].split("T")[0]}
                        )
                        waste_array.append(
                            {"restafvaldiftarcollections": data["totalThisYear"]}
                        )

            # _LOGGER.warning(waste_array)

            return waste_array
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
