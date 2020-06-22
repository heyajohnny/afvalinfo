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


class BeeselAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                result = data.find("th", {"class": "icon-" + afvaltype})
                if result:
                    date = str(data.td)

                    day = date.split()[1].zfill(2)
                    try:
                        month = MONTH_TO_NUMBER[(date.split()[2]).split("<br/>")[0]]
                    except Exception as exc:
                        month = MONTH_TO_NUMBER[(date.split()[2]).split("<span>")[0]]
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
            thisYear = datetime.today().year

            url = SENSOR_LOCATIONS_TO_URL["beesel"][0].format(
                postcode, street_number, thisYear
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            div = soup.find("div", {"class": "main-content"})
            tbody = div.find("tbody")
            ophaaldata = tbody.find_all("tr")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "restafval", "restafval")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "gft", "gft")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "oudpapier", "papier")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False
