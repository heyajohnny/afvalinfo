#!/usr/bin/env python3

"""Waste collection provider clients for Afvalinfo."""

import asyncio
from datetime import date, datetime
from functools import partial
from typing import Any

import requests

from ..const.const import _LOGGER, SENSOR_LOCATIONS_TO_URL

REQUEST_TIMEOUT = 15
GAD_API_URL = "https://inzamelkalender.gad.nl"
GAD_LOCATIONS = {"gooise meren"}

GAD_ICON_TO_RESOURCES = {
    "appel-gft": ("gft",),
    "doos-karton-papier": ("papier",),
    "gad-appel-gft": ("gft",),
    "gad-grof-rest": ("grofvuil",),
    "gad-kerstboom": ("kerstboom",),
    "gad-klein-chemisch-afval-": ("kca",),
    "gad-papier-karton": ("papier",),
    "gad-rest-pmd": ("restafval", "pbd"),
    "gad-shirt-textiel": ("textiel",),
    "gad-tak-snoeiafval": ("takken",),
    "kliko-grijs-rest": ("restafval",),
    "petfles-blik-drankpak-pmd": ("pbd",),
}


class AfvalinfoProviderError(Exception):
    """Base exception for provider failures."""

    error_type = "provider_error"

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class AfvalinfoConnectionError(AfvalinfoProviderError):
    """Raised when a provider cannot be reached."""

    error_type = "connection_error"


class AfvalinfoInvalidAddressError(AfvalinfoProviderError):
    """Raised when a provider does not recognize an address."""

    error_type = "invalid_address"


class AfvalinfoResponseError(AfvalinfoProviderError):
    """Raised when a provider returns an invalid response."""

    error_type = "invalid_response"


class TrashApiAfval:
    """Fetch and normalize waste collection data."""

    async def get_data(
        self,
        location,
        postcode,
        street_number,
        street_number_suffix,
        diftar_code,
        get_whole_year,
        resources,
        get_cleanprofs_data,
    ):
        """Return normalized collection data for an address."""
        _LOGGER.debug("Updating waste collection dates for municipality %s", location)

        if location.casefold() in GAD_LOCATIONS:
            return await self._get_gad_data(
                postcode,
                street_number,
                street_number_suffix,
                get_whole_year,
                resources,
            )

        endpoint = SENSOR_LOCATIONS_TO_URL["trashapi"][0].format(
            location,
            postcode,
            street_number,
            street_number_suffix,
            diftar_code,
            get_whole_year,
            get_cleanprofs_data,
        )
        payload = await self._request_json(endpoint, "TrashAPI")
        return self._parse_trashapi_payload(payload, resources)

    async def _get_gad_data(
        self,
        postcode,
        street_number,
        street_number_suffix,
        get_whole_year,
        resources,
    ):
        address_payload = await self._request_json(
            f"{GAD_API_URL}/adressen/{postcode}:{street_number}",
            "GAD address service",
        )
        if not isinstance(address_payload, list):
            raise AfvalinfoResponseError(
                "GAD returned an unexpected address response."
            )
        if not address_payload:
            raise AfvalinfoInvalidAddressError(
                "GAD could not find this postcode and house number."
            )

        address = self._select_gad_address(address_payload, street_number_suffix)
        if not isinstance(address, dict):
            raise AfvalinfoResponseError("GAD returned an invalid address item.")
        bag_id = address.get("bagid")
        if not bag_id:
            raise AfvalinfoResponseError(
                "GAD returned an address without a waste collection identifier."
            )

        waste_flows = await self._request_json(
            f"{GAD_API_URL}/rest/adressen/{bag_id}/afvalstromen",
            "GAD waste stream service",
        )
        if not isinstance(waste_flows, list):
            raise AfvalinfoResponseError(
                "GAD returned an unexpected waste stream response."
            )

        years = [date.today().year]
        if get_whole_year:
            years.append(date.today().year + 1)
        today = date.today()

        calendar_items = []
        for year in years:
            calendar_payload = await self._request_json(
                f"{GAD_API_URL}/rest/adressen/{bag_id}/kalender/{year}",
                "GAD calendar service",
            )
            if not isinstance(calendar_payload, list):
                raise AfvalinfoResponseError(
                    "GAD returned an unexpected calendar response."
                )
            calendar_items.extend(calendar_payload)

        flow_resources = self._get_gad_flow_resources(waste_flows)
        waste_array = []
        seen_collections = set()
        for item in calendar_items:
            if not isinstance(item, dict):
                raise AfvalinfoResponseError(
                    "GAD returned an invalid calendar item."
                )
            item_resources = flow_resources.get(
                str(item.get("afvalstroom_id")), ()
            )
            collection_date = item.get("ophaaldatum")
            if not self._is_iso_date(collection_date):
                continue
            if datetime.strptime(collection_date, "%Y-%m-%d").date() < today:
                continue
            for resource in item_resources:
                collection = (resource, collection_date)
                if resource in resources and collection not in seen_collections:
                    waste_array.append({resource: collection_date})
                    seen_collections.add(collection)

        return waste_array

    async def _request_json(self, endpoint: str, provider_name: str) -> Any:
        try:
            response = await asyncio.get_running_loop().run_in_executor(
                None,
                partial(requests.get, endpoint, timeout=REQUEST_TIMEOUT),
            )
        except requests.Timeout as exc:
            raise AfvalinfoConnectionError(
                f"{provider_name} timed out after {REQUEST_TIMEOUT} seconds."
            ) from exc
        except requests.RequestException as exc:
            raise AfvalinfoConnectionError(
                f"{provider_name} could not be reached."
            ) from exc

        if response.status_code == 404:
            raise AfvalinfoResponseError(
                f"{provider_name} returned HTTP 404. The municipality may be "
                "temporarily unavailable or unsupported by the upstream service.",
                status_code=404,
            )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise AfvalinfoResponseError(
                f"{provider_name} returned HTTP {response.status_code}.",
                status_code=response.status_code,
            ) from exc

        try:
            return response.json()
        except (requests.exceptions.JSONDecodeError, ValueError) as exc:
            raise AfvalinfoResponseError(
                f"{provider_name} returned invalid JSON."
            ) from exc

    @staticmethod
    def _select_gad_address(addresses, suffix):
        normalized_suffix = str(suffix or "").strip().casefold()
        if not normalized_suffix:
            return addresses[0]

        for address in addresses:
            if not isinstance(address, dict):
                continue
            address_suffix = "".join(
                str(address.get(field) or "").strip()
                for field in ("huisletter", "toevoeging")
            ).casefold()
            if address_suffix == normalized_suffix:
                return address

        raise AfvalinfoInvalidAddressError(
            "GAD found the postcode and house number, but not the supplied suffix."
        )

    @staticmethod
    def _get_gad_flow_resources(waste_flows):
        resources = {}
        for flow in waste_flows:
            if not isinstance(flow, dict) or "id" not in flow:
                raise AfvalinfoResponseError(
                    "GAD returned an invalid waste stream item."
                )
            flow_resources = GAD_ICON_TO_RESOURCES.get(
                str(flow.get("icon", "")).casefold()
            )
            if flow_resources is None:
                title = str(flow.get("title") or flow.get("menu_title") or "").casefold()
                if "papier" in title or "karton" in title:
                    flow_resources = ("papier",)
                elif "gft" in title or "gfe" in title:
                    flow_resources = ("gft",)
                elif "rest" in title and "pmd" in title:
                    flow_resources = ("restafval", "pbd")
                elif "pmd" in title or "plastic" in title:
                    flow_resources = ("pbd",)
                elif "rest" in title:
                    flow_resources = ("restafval",)
                elif "textiel" in title:
                    flow_resources = ("textiel",)
                elif "kerst" in title:
                    flow_resources = ("kerstboom",)
                elif "chemisch" in title:
                    flow_resources = ("kca",)
                elif "tuinafval" in title or "snoei" in title:
                    flow_resources = ("takken",)
                elif "grof" in title:
                    flow_resources = ("grofvuil",)
            if flow_resources:
                resources[str(flow["id"])] = flow_resources
        return resources

    @staticmethod
    def _parse_trashapi_payload(payload, resources):
        if not isinstance(payload, list):
            raise AfvalinfoResponseError(
                "TrashAPI returned an unexpected response instead of a collection list."
            )

        waste_array = []
        for item in payload:
            if not isinstance(item, dict):
                raise AfvalinfoResponseError(
                    "TrashAPI returned an invalid collection item."
                )

            name = item.get("name")
            collection_date = item.get("date")
            if not isinstance(name, str) or not TrashApiAfval._is_iso_datetime(
                collection_date
            ):
                raise AfvalinfoResponseError(
                    "TrashAPI returned a collection item with missing or invalid fields."
                )

            resource = name.casefold()
            normalized_date = collection_date.split("T", maxsplit=1)[0]
            if resource in resources:
                if resource != "restafval" or date.today() <= datetime.strptime(
                    normalized_date, "%Y-%m-%d"
                ).date():
                    waste_array.append({resource: normalized_date})
                    continue

            if resource == "restafval" and "restafval" in resources:
                waste_array.append({"restafvaldiftardate": normalized_date})
                if "totalThisYear" in item:
                    waste_array.append(
                        {"restafvaldiftarcollections": item["totalThisYear"]}
                    )

        return waste_array

    @staticmethod
    def _is_iso_datetime(value):
        if not isinstance(value, str):
            return False
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return False
        return True

    @staticmethod
    def _is_iso_date(value):
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False
        return True
