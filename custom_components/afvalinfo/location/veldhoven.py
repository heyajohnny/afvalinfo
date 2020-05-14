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


class VeldhovenAfval(object):
    def get_date_from_afvaltype(self, ophaaldata, afvaltype, afvalnaam):
        try:
            # get index of the <h3> element, which is just before our <td> element with the date
            searchString = "id=\"" + afvaltype + "\">"
            i = str(ophaaldata).index(searchString) + len(searchString)

            # get the <p> element with the date in it
            dates = BeautifulSoup(str(ophaaldata)[i:], "html.parser").find(
                "td"
            )

            insdate = dates.find("ins")

            #no insdate, return normal date
            if insdate == None:
                date = str(dates).split("<br/>")[0]
                day = date.split()[1]
                month = MONTH_TO_NUMBER[date.split()[2]]
                year = str(
                    datetime.today().year
                    if datetime.today().month <= int(month)
                    else datetime.today().year + 1
                )
                return year + "-" + month + "-" + day
            else:
                #get insdate
                date = str(insdate).split("</ins>")[0].zfill(2)
                day = date.split()[1]
                month = MONTH_TO_NUMBER[date.split()[2]]
                year = str(
                    datetime.today().year
                    if datetime.today().month <= int(month)
                    else datetime.today().year + 1
                )
                insdate = year + "-" + month + "-" + day

                #get normal date
                date = str(dates).split("<br/>")[0]

                #if the first one is a delete, then the result is insdate
                delete = date.find("</del>")
                if delete != -1:
                    return insdate

                #else, continue to find the normal date
                day = date.split()[1].zfill(2)
                month = MONTH_TO_NUMBER[date.split()[2]]
                year = str(
                    datetime.today().year
                    if datetime.today().month <= int(month)
                    else datetime.today().year + 1
                )

                date = year + "-" + month + "-" + day

                #compare dates and return the first
                firstdate = insdate if insdate < date else date
                return firstdate
        except Exception as exc:
            _LOGGER.warning("Something went wrong while splitting data: %r. This probably means that trash type %r is not supported on your location", exc, afvalnaam)
            return ""

    def get_data(self, city, postcode, street_number, resources):
        _LOGGER.debug("Updating Waste collection dates")

        try:
            url = SENSOR_LOCATIONS_TO_URL["veldhoven"][0].format(
                postcode, street_number
            )
            req = urllib.request.Request(url=url)
            f = urllib.request.urlopen(req)
            html = f.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            ophaaldata = soup.find(id="main")
            ophaaldata = ophaaldata.find("table", {"id": "garbage-dates"})

            # Place all possible values in the dictionary even if they are not necessary
            waste_dict = {}
            # find groene-container = gft
            if "gft" in resources:
                waste_dict["gft"] = self.get_date_from_afvaltype(ophaaldata, "groene-container", "gft")
            # find grijze-container = restafval
            if "restafval" in resources:
                waste_dict["restafval"] = self.get_date_from_afvaltype(ophaaldata, "grijze-container", "restafval")
            # find pmd-zak = pbd
            if "pbd" in resources:
                waste_dict["pbd"] = self.get_date_from_afvaltype(ophaaldata, "pmd-zak", "pbd")
            # find blauwe-container = papier
            if "papier" in resources:
                waste_dict["papier"] = self.get_date_from_afvaltype(ophaaldata, "blauwe-container", "papier")

            return waste_dict
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc.reason)
            return False
