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


class MijnAfvalWijzerAfval(object):
    def get_date_from_afvaltype(self, html, afvaltype):
        try:
            results = html.findAll("p", {"class": afvaltype})

            for result in results:
                date = result.find("span", {"class": "span-line-break"})

                # get the value of the span
                date = date.string

                day = date.split()[1]
                month = MONTH_TO_NUMBER[date.split()[2]]
                # the year is always this year because it's a 'jaaroverzicht'
                year = datetime.today().year

                if int(month) >= datetime.today().month:
                    if int(month) == datetime.today().month:
                        if int(day) >= datetime.today().day:
                            return str(year) + "-" + str(month) + "-" + str(day)
                    else:
                        return str(year) + "-" + str(month) + "-" + str(day)
            # if nothing was found
            return ""
        except Exception as exc:
            _LOGGER.error("Error occurred while splitting data: %r", exc)
            return ""

    def get_data(self, city, postcode, street_number):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["mijnafvalwijzer"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            jaaroverzicht = soup.find(id="jaaroverzicht")

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}

            # find gft. In some locations it's 'gft' and in other locations it's 'restgft'
            waste_dict["gft"] = self.get_date_from_afvaltype(jaaroverzicht, "gft")
            if len(waste_dict["gft"]) == 0:
                waste_dict["gft"] = self.get_date_from_afvaltype(jaaroverzicht, "restgft")
            # find papier
            waste_dict["papier"] = self.get_date_from_afvaltype(jaaroverzicht, "papier")
            # find pbd. In some locations it's 'pd' and in other locations it's 'pmb' or 'plastic'
            waste_dict["pbd"] = self.get_date_from_afvaltype(jaaroverzicht, "pd")
            if len(waste_dict["pbd"]) == 0:
                waste_dict["pbd"] = self.get_date_from_afvaltype(jaaroverzicht, "pmd")
            if len(waste_dict["pbd"]) == 0:
                waste_dict["pbd"] = self.get_date_from_afvaltype(jaaroverzicht, "plastic")
            # find restafval. In some locations it's 'restafval' and in other locations it's 'restgft'
            waste_dict["restafval"] = self.get_date_from_afvaltype(jaaroverzicht, "restafval")
            if len(waste_dict["restafval"]) == 0:
                waste_dict["restafval"] = self.get_date_from_afvaltype(jaaroverzicht, "restgft")
            # find textiel
            waste_dict["textiel"] = self.get_date_from_afvaltype(jaaroverzicht, "textiel")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
