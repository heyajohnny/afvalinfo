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


class WesterwoldeAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            tables = ophaaldata.find_all("table")

            for table in tables:
                thead = table.find("thead")
                thDate = thead.find("th").string

                thMonth = MONTH_TO_NUMBER[(thDate.lower().split()[0])]
                thYear = thDate.split()[1]

                currentMonth = str(datetime.today().month).zfill(2)
                currentYear = str(datetime.today().year)

                tbody = table.find("tbody")
                trs = tbody.find_all("tr")

                for tr in trs:
                    match = tr.find("img", {"alt": afvaltype})
                    if match:
                        date = tr.find("td", {"class": "trash-date"})
                        day = str(date).split()[2].strip()

                        #Search in the current month
                        if thMonth == currentMonth and thYear == currentYear:
                            currentDay = datetime.today().day
                            if int(day) >= currentDay:
                                return thYear + "-" + thMonth + "-" + day
                        #If it's a month in the future
                        else:
                            return thYear + "-" + thMonth + "-" + day
            return ""
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["westerwolde"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")

            content = soup.find("div", {"id": ['block-system-main']})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(content, "Rest", "restafval")
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(content, "GFT", "gft")
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(content, "Oud papier", "papier")
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(content, "PMD", "pbd")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False
