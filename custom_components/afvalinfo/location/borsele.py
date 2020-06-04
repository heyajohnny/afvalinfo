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

class BorseleAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                result = data.find("th", {"class": afvaltype})
                if result:
                    date = data.find("td")
                    date = str(date).split("<br/>")[0]
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
            url = SENSOR_LOCATIONS_TO_URL["borsele"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find(id="garbage-dates")
            ophaaldata = ophaaldata.find_all("tr")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find afvalstroom/3 = gft
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "icon-groene-container", "gft")
            # find afvalstroom/7 = restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "icon-grijze-container", "restafval")
            # find afvalstroom/87 = papier
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "icon-blauwe-container", "papier")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False