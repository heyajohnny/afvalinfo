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


class GroningenAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            currentMonth = datetime.today().month
            nextMonth = datetime.today().month + 1
            for data in ophaaldata:
                result = data.parent.find("tr", {"data-lob": afvaltype})
                if result:
                    day = result.find("td", {"class": "m-" + str(currentMonth).zfill(2)}).find("li").string
                    month = str(currentMonth).zfill(2)
                    year = datetime.today().year
                    if int(day) < datetime.today().day:
                        month = str(nextMonth).zfill(2)
                        day = result.find("td", {"class": "m-" + str(nextMonth).zfill(2)}).find("li").string

                    if day:
                        return str(year) + "-" + month + "-" + day
            return ""
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            thisYear = datetime.today().year

            url = SENSOR_LOCATIONS_TO_URL["groningen"][0].format(
                postcode, street_number, thisYear
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", {"class": "afvalwijzerData"})
            tbody = table.find("tbody")
            ophaaldata = tbody.find_all("tr")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            if "textiel" in resources:
                waste_dict["textiel"] = self.get_date_from_afvaltype(ophaaldata, "TEXTL", "textiel")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "HPAP", "papier")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "HGFT", "gft")
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "HGRIJS", "restafval")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False
