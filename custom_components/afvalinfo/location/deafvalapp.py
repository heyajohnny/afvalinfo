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
import http.cookiejar


class DeAfvalAppAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            # get index of the <a> element, which is just before our <p> element with the date
            searchString = "=" + afvaltype + "\">"
            i = str(ophaaldata).index(searchString) + len(searchString)

            # get the <p> element with the date in it
            date = BeautifulSoup(str(ophaaldata)[i:], "html.parser").find(
                "p", {"class": "date"}
            )
            # get the content of <p>
            date = date.string

            day = date.split()[1]
            month = MONTH_TO_NUMBER[date.split()[2]]
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
            # Storing cookies in cj variable
            cj = http.cookiejar.CookieJar()

            # Defining a handler for later http operations with cookies(cj).
            op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            # first call to save cookie
            url = SENSOR_LOCATIONS_TO_URL["deafvalapp"][0].format(
                postcode, street_number
            )
            res = op.open(url)

            # second call to fetch data
            res = op.open(SENSOR_LOCATIONS_TO_URL["deafvalapp"][1])
            html = res.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find("div", {"class": "ophaaldagen"})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find gft
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "GFT", "gft")
            # find papiers
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "PAPIER", "papier")
            # find pbd / pmd
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "PMD", "pbd")
                if len(waste_dict["pbd"]) == 0:
                    waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "PLASTIC", "pbd")
                if len(waste_dict["pbd"]) == 0:
                    waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "PBP", "pbd")
            # find restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "REST", "restafval")
                if len(waste_dict["restafval"]) == 0:
                    waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "ZAK_BLAUW", "restafval")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
