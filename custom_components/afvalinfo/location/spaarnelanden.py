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


class SpaarnelandenAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            html = ophaaldata.find(href="/afvalstroom/" + str(afvaltype))
            date = html.i.string[3:]
            day = date.split()[0]
            month = MONTH_TO_NUMBER[date.split()[1]]
            year = str(
                datetime.today().year
                if datetime.today().month <= int(month)
                else datetime.today().year + 1
            )
            return year + "-" + month + "-" + day
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["spaarnelanden"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find(id="ophaaldata")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find afvalstroom/1 = pbd/papier
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, 1, "pbd")
            # find afvalstroom/21 = papier
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, 1, "papier")
                if len(waste_dict["papier"]) == 0:
                    waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, 21, "papier")
            # find afvalstroom/3 = gft
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, 3, "gft")
                # find afvalstroom/23 = gft
                if len(waste_dict["gft"]) == 0:
                    waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, 23, "gft")
            # find afvalstroom/26 = restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, 26, "restafval")
                if len(waste_dict["restafval"]) == 0:
                    waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, 7, "restafval")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
