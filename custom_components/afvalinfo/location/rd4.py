from ..const.const import (
    MONTH_TO_NUMBER,
    NUMBER_TO_MONTH,
    SENSOR_LOCATIONS_TO_URL,
    _LOGGER,
)
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

class Rd4Afval(object):
    def get_date_from_afvaltype(self, data, afvaltype, afvalnaam):
        try:
            afvaltype = afvaltype.lower()
            thisMonth = datetime.today().month

            if datetime.today().month <= 11:
                nextMonth = datetime.today().month + 1
            else:
                nextMonth = 1

            data = BeautifulSoup(str(data).lower(), "html.parser")
            html = data.find_all("table", {"class": "plaintextmonth"})

            htmlThisMonth = html[thisMonth - 1]
            tdsThisMonth = htmlThisMonth.find_all("td")

            for index, td in enumerate(tdsThisMonth):
                if str(td).find(afvaltype) != -1:
                    date = tdsThisMonth[index - 1].string
                    day = int(date.split()[1])
                    #if today is later than the found date, erase the date and day
                    if datetime.today().day > day:
                        date = None
                        day = None
                    #a valid date is found, break the loop
                    else:
                        break

            #If no valid date for this month is found, check next monthToNumber
            #But not when the next month is next year
            if date is None and nextMonth != 1:
                htmlNextMonth = html[nextMonth - 1]
                tdsNextMonth = htmlNextMonth.find_all("td")
                for index, td in enumerate(tdsNextMonth):
                    if str(td).find(afvaltype) != -1:
                        #valid date found
                        date = tdsNextMonth[index - 1].string
                        break

            day = date.split()[1]
            month = MONTH_TO_NUMBER[date.split()[2]]
            year = date.split()[3]
            return year + "-" + month + "-" + day
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["rd4"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find(id="Afvalkalender1_pnlAfvalKalender")

            #ToDo: Check calendar for the next year...
            #need to send _VIEWSTATE and that kind of stuff

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "GFT", "gft")
            if "textiel" in resources:
                waste_dict["textiel"] = self.get_date_from_afvaltype(ophaaldata, "BEST-tas", "textiel")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "Oud papier", "papier")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "PMD-afval", "pbd")
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "Restafval", "restafval")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
