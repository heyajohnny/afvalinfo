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
import http.cookiejar
import ssl


class MontferlandAfval(object):
    def get_date_from_afvaltype(self, data, afvaltype, afvalnaam):
        try:
            results = data.findAll("li")

            for result in results:
                data = str(result).find(afvaltype)

                if data != -1:
                    html = result.find("div")

                    #get innerHTML
                    date = html.decode_contents(formatter="html")

                    day = date.split()[1]
                    month = MONTH_TO_NUMBER[date.split()[2]]
                    year = str(
                        datetime.today().year
                        if datetime.today().month <= int(month)
                        else datetime.today().year + 1
                    )
                    return year + "-" + month + "-" + day
            return ""
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""


    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # all cookies received will be stored in the session object
            session = requests.Session()

            #1st request
            url = SENSOR_LOCATIONS_TO_URL["montferland"][0]

            response = session.get(url=url, verify=False)

            #2nd request
            url = SENSOR_LOCATIONS_TO_URL["montferland"][1]

            data = {
                "__VIEWSTATE": "/wEPDwUKLTM5MTk3ODQzN2RkSMQs/PGhkTwWHZC8SVdt6IaYIIDuEWuoJGIgf3Be0ZU=",
                "__EVENTVALIDATION": "/wEdAArjvnOxLwB9PxTCWtoaK2+zouXMNXvm40+eE6LS7ueoPudOJulUMxnDSIQD5teXezAJGvdwo0h2UOH1R1pgUXydhF5U1gvAwwAlNYIz3+sICAgttuVT/1BKUUO4wraV4ri6agKYYACjPfI86+Yqx0yzLfsQS1LRccAKKtzS/QsOtnjGk3N/PZcV0uc8RRlYMqcjS29nfr0aSaK0LTwLryCerJaYuRWq5LYeiMQ/PuQaAMYBK7Zbr8dfTq6n77jvx9o=",
                "ctl00$content$adr_postcode": postcode,
                "ctl00$content$adr_huisnr": street_number,
                "ctl00$content$adr_toevoeging": "",
                "ctl00$content$BtnLogin": "Verder"
            }

            postdata = urllib.parse.urlencode(data).encode()
            response = session.post(url=url, data=data, verify=False)

            #read the data
            soup = BeautifulSoup(response.text, "html.parser")
            nextPickup = soup.find("div", {"id": ['ctl00_content_Inzameldata_content']})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(nextPickup, "Rest afval", "restafval")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(nextPickup, "GFT afval", "gft")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(nextPickup, "Papier", "papier")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(nextPickup, "Plastic, Metaal en Drankenkartons", "pbd")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False