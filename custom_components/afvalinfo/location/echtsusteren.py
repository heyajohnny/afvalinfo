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


class EchtSusterenAfval(object):
    """def get_date_from_afvalstroom(self, ophaaldata, afvalstroom):
        html = ophaaldata.find(href="/afvalstroom/" + str(afvalstroom))
        date = html.i.string[3:]
        day = date.split(" ")[0]
        month = MONTH_TO_NUMBER[date.split(" ")[1]]
        year = str(
            datetime.today().year
            if datetime.today().month <= int(month)
            else datetime.today().year + 1
        )
        return year + "-" + month + "-" + day"""

    def get_data(self, city, postcode, street_number):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["echtsusteren"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find({"class": "ophaaldagen"})
            _LOGGER.error(ophaaldata)

            #ToDo: Save cookie and make request to
            #http://echt-susteren.deafvalapp.nl/calendar/kalender_dashboard.jsp

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find afvalstroom/3 = gft
            """waste_dict["gft"] = self.get_date_from_afvalstroom(ophaaldata, 3)
            # find afvalstroom/7 = textiel
            waste_dict["textiel"] = self.get_date_from_afvalstroom(ophaaldata, 7)
            # find afvalstroom/87 = papier
            waste_dict["papier"] = self.get_date_from_afvalstroom(ophaaldata, 87)
            # find afvalstroom/92 = pbd
            waste_dict["pbd"] = self.get_date_from_afvalstroom(ophaaldata, 92)
            """
            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
