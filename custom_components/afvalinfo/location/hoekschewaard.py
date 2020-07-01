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


class HoekscheWaardAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                result = data.find("span", {"class": "my-icons-" + afvaltype})
                result2 = data.find("span", {"class": "my-icons-" + afvaltype + "-icon"})
                if result or result2:
                    date = data.find("span", {"class": "datum"}).string

                    day = date.split()[1].zfill(2)
                    month = MONTH_TO_NUMBER[(date.split()[2])]
                    year = date.split()[3]
                    return year + "-" + month + "-" + day
            return ""
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["hoekschewaard"][0].format(
                postcode[:4] + "+" + postcode[4:], street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ul = soup.find("ul", {"class": "downloads"})
            ophaaldata = ul.find_all("li")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "gft", "gft")
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "rest", "restafval")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "papier", "papier")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "pmd", "pbd")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False
