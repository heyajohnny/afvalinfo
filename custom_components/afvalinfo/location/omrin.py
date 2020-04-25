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


class OmrinAfval(object):
    def get_date_from_afvaltype(self, year, data, afvaltype):
        try:
            dataFilteredByType = data[afvaltype]
            dates = dataFilteredByType["dates"]

            thisMonth = datetime.today().month
            thisDay = datetime.today().day

            #for next year, start searching from month 1, day 1
            if year > datetime.today().year:
                for month in range(1, 13):
                    for day in range(1, 32):
                        res = dates["%s" % month]
                        if '{:02d}'.format(day) in res:
                            return str(year) + "-" + '{:02d}'.format(month) + "-" + '{:02d}'.format(day)
            else:
                for month in range(thisMonth, 13):
                    #this month start searching from the current day
                    if month == thisMonth:
                        for day in range(thisDay, 32):
                            res = dates["%s" % month]
                            if '{:02d}'.format(day) in res:
                                return str(year) + "-" + '{:02d}'.format(month) + "-" + '{:02d}'.format(day)
                    #next month start searching from day 1
                    else:
                        for day in range(1, 32):
                            res = dates["%s" % month]
                            if '{:02d}'.format(day) in res:
                                return str(year) + "-" + '{:02d}'.format(month) + "-" + '{:02d}'.format(day)
        except:
            return ""

    def get_data(self, city, postcode, street_number):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            # Storing cookies in cj variable
            cj = http.cookiejar.CookieJar()

            # Defining a handler for later http operations with cookies(cj).
            op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            # first call to save cookie
            url = SENSOR_LOCATIONS_TO_URL["omrin"][0]

            data = {
                "zipcode": postcode[:4],
                "zipcodeend": postcode[4:],
                "housenumber": street_number,
                "addition": "",
                "send": "Mijn overzicht",
            }

            postdata = urllib.parse.urlencode(data).encode()

            # sending post request and saving response as response object
            request = urllib.request.Request(url, postdata)
            #open the response object
            response = op.open(request)

            #make a second call with the just retrieved cookie
            response = op.open(url)

            #read the data
            html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            frame = soup.find("div", {"id": "frame"})
            script = frame.find("script", {"type": "text/javascript"}).string
            omrinDataGroups = script[script.index("{"):]
            omrinDataGroupsJson = json.loads(omrinDataGroups[:len(omrinDataGroups) - 1])

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            thisYear = datetime.today().year
            nextYear = (datetime.today() + relativedelta(years=1)).year

            omrinThisYear = omrinDataGroupsJson["%s" % thisYear]

            try:
                omrinNextYear = omrinDataGroupsJson["%s" % nextYear]
            except KeyError:
                omrinNextYear = None

            #restafval = Sortibak or Restafval
            waste_dict["restafval"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Sortibak")
            if omrinNextYear and len(waste_dict["restafval"]) == 0:
                waste_dict["restafval"] = self.get_date_from_afvaltype(nextYear, omrinNextYear, "Sortibak")
            if len(waste_dict["restafval"]) == 0:
                waste_dict["restafval"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Restafval")
            if omrinNextYear and len(waste_dict["restafval"]) == 0:
                waste_dict["restafval"] = self.get_date_from_afvaltype(thisYear, omrinNextYear, "Restafval")
            #gft = Biobak or Tuinafval or Extra Tuinafval
            waste_dict["gft"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Biobak")
            if omrinNextYear and len(waste_dict["gft"]) == 0:
                waste_dict["gft"] = self.get_date_from_afvaltype(nextYear, omrinNextYear, "Biobak")
            #see which one is earlier
            if len(waste_dict["gft"]) == 0:
                if len(waste_dict["gft"]) == 0:
                    tuinafval = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Tuinafval")
                if omrinNextYear and len(tuinafval) == 0:
                    tuinafval = self.get_date_from_afvaltype(thisYear, omrinNextYear, "Tuinafval")
                if len(waste_dict["gft"]) == 0:
                    extratuinafval = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Extra Tuinafval")
                if omrinNextYear and len(extratuinafval) == 0:
                    extratuinafval = self.get_date_from_afvaltype(thisYear, omrinNextYear, "Extra Tuinafval")
                if len(tuinafval) != 0 or len(extratuinafval) != 0:
                    if len(tuinafval) != 0 and len(extratuinafval) == 0:
                        waste_dict["gft"] = tuinafval
                    if len(tuinafval) == 0 and len(extratuinafval) != 0:
                        waste_dict["gft"] = extratuinafval
                    if len(tuinafval) != 0 and len(extratuinafval) != 0:
                        if tuinafval < extratuinafval:
                            waste_dict["gft"] = tuinafval
                        if extratuinafval < tuinafval:
                            waste_dict["gft"] = extratuinafval
            #papier = Oud papier en karton.. or Oud papier en karton
            waste_dict["papier"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Oud papier en karton..")
            if omrinNextYear and len(waste_dict["papier"]) == 0:
                waste_dict["papier"] = self.get_date_from_afvaltype(nextYear, omrinNextYear, "Oud papier en karton..")
            if len(waste_dict["papier"]) == 0:
                waste_dict["papier"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Oud papier en karton")
            if omrinNextYear and len(waste_dict["papier"]) == 0:
                waste_dict["papier"] = self.get_date_from_afvaltype(thisYear, omrinNextYear, "Oud papier en karton")
            #textiel = textiel
            waste_dict["textiel"] = self.get_date_from_afvaltype(thisYear, omrinThisYear, "Textiel")
            if omrinNextYear and len(waste_dict["textiel"]) == 0:
                waste_dict["textiel"] = self.get_date_from_afvaltype(nextYear, omrinNextYear, "Textiel")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False