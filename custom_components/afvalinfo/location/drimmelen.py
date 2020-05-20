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


class DrimmelenAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                result = data.find("img", {"alt": afvaltype})
                if result:
                    date = data.find("td", {"class": "trash-date"})
                    day = str(date).split()[2]
                    month = data.find("span", {"class": "element-invisible"}).string
                    month = MONTH_TO_NUMBER[month]
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
            url = SENSOR_LOCATIONS_TO_URL["drimmelen"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(str(html).lower(), "html.parser")
            ophaaldata = soup.find(id="main-wrapper")
            ophaaldata = ophaaldata.find_all("tr", {"class": ["odd", "even"]})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # GFT
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "gft", "gft")
            # Textiel
            if "textiel" in resources:
                waste_dict["textiel"] = self.get_date_from_afvaltype(ophaaldata, "textiel", "textiel")
            # Papier
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "papier", "papier")
            # Restafval
            if "papier" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "restafval", "papier")
            # Plastic
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "plastic", "pbd")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
