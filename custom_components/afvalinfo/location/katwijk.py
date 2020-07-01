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


class KatwijkAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            for data in ophaaldata:
                match = data["class"][1]
                if match == afvaltype:
                    dates = data.find("div", {"class": "dates"})
                    date = dates.find("div", {"class": "date"}).string

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
            # Storing cookies in cj variable
            cj = http.cookiejar.CookieJar()

            # Defining a handler for later http operations with cookies(cj).
            op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            url = SENSOR_LOCATIONS_TO_URL["katwijk"][0]

            data = {
                "tx_windwastecalendar_pi1[zipcode]": postcode[:4] + "+" + postcode[4:],
                "tx_windwastecalendar_pi1[housenumber]": street_number,
            }

            postdata = urllib.parse.urlencode(data).encode()

            # sending post request and saving response as response object
            request = urllib.request.Request(url, postdata)
            #open the response object
            response = op.open(request)

            #read the data
            html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")

            mainDiv = soup.find("div", {"class": ['tx-wind-waste-calendar']})

            wasteCalendar = mainDiv.find_all("div", {"class": ['waste-calendar']})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(wasteCalendar, "grijzecontainer", "restafval")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(wasteCalendar, "groenecontainer", "gft")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False