from ..const.const import (
    MONTH_TO_NUMBER,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import requests
import http.cookiejar
import re


class DenHaagAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            today = date.today()
            for data in ophaaldata:
                result = data.find("h2").string
                if result.strip() == afvaltype:
                    dates = re.findall(r'[\w]+[\W]+[\d]+ [\w]+ [\d]+', str(data))
                    for dateString in dates:
                        dateString = dateString.split("\n")[1]
                        day = dateString.split()[0]
                        month = MONTH_TO_NUMBER[dateString.split()[1]]
                        year = dateString.split()[2]

                        foundDate = date(int(year), int(month), int(day))

                        if foundDate >= today:
                            return year + "-" + month + "-" + day
            return ""
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
            url = SENSOR_LOCATIONS_TO_URL["denhaag"][0]

            res = op.open(url)

            _LOGGER.warning(res.headers)

            # second call
            url = SENSOR_LOCATIONS_TO_URL["denhaag"][0]

            data = {
                "postcode": postcode,
                "huisnummer": street_number
            }

            postdata = urllib.parse.urlencode(data).encode()

            # sending post request and saving response as response object
            request = urllib.request.Request(url, postdata)

            #open the response object
            response = op.open(request)

            #read the data
            """html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")

            _LOGGER.warning(soup)

            # 3rd call
            url = SENSOR_LOCATIONS_TO_URL["denhaag"][1]

            request = urllib.request.Request(url)

            #open the response object
            response = op.open(request)
"""
            #read the data
            html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")

            #_LOGGER.warning(soup)
            _LOGGER.warning(response.headers)


            #ophaaldata = soup.find("main")
            #ophaaldata = ophaaldata.find_all("div", {"style": ["width:32%;float:left;", "width:32%;float:right;"]})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # gft
            """if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "Groene container:", "gft")
            # restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "Grijze container:", "restafval")
            # pbd
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "Oranje container:", "pbd")
            """
            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
