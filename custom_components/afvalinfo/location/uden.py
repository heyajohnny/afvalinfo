from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import http.cookiejar
import json


class UdenAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                match = data.find("th", {"class": "icon-" + afvaltype})
                if match:
                    date = str(data.find("td"))
                    date = date.split("<br/>")[0]
                    date = date[4:]

                    day = date.split()[1].zfill(2)
                    month = MONTH_TO_NUMBER[(date.split()[2])]
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
            url = SENSOR_LOCATIONS_TO_URL[city][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")

            mainDiv = soup.find("div", {"id": ['content']})

            tBody = mainDiv.find("tbody")

            tr = tBody.find_all("tr")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(tr, "restafval", "restafval")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(tr, "plastic", "pbd")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(tr, "oudpapier", "papier")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(tr, "gft", "gft")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False