"""Tests for the Afvalinfo provider clients."""

import asyncio
import unittest
from datetime import date
from unittest.mock import patch

import requests

from custom_components.afvalinfo.location.trashapi import (
    AfvalinfoConnectionError,
    AfvalinfoResponseError,
    TrashApiAfval,
)


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(response=self)


class TrashApiTests(unittest.TestCase):
    def run_async(self, coroutine):
        return asyncio.run(coroutine)

    def test_gad_provider_restores_gooise_meren_data(self):
        responses = [
            FakeResponse([{"bagid": "bag-1", "huisletter": "", "toevoeging": ""}]),
            FakeResponse(
                [
                    {"id": 1, "icon": "gad-appel-gft", "title": "GFE+T"},
                    {"id": 3, "icon": "gad-papier-karton", "title": "Papier"},
                    {"id": 27, "icon": "gad-rest-pmd", "title": "Rest+pmd"},
                ]
            ),
            FakeResponse(
                [
                    {"afvalstroom_id": 1, "ophaaldatum": "2026-01-23"},
                    {"afvalstroom_id": 3, "ophaaldatum": "2026-01-15"},
                    {"afvalstroom_id": 27, "ophaaldatum": "2026-07-17"},
                    {"afvalstroom_id": 1, "ophaaldatum": "2026-10-12"},
                    {"afvalstroom_id": 3, "ophaaldatum": "2026-10-13"},
                    {"afvalstroom_id": 27, "ophaaldatum": "2026-10-14"},
                ]
            ),
            FakeResponse(
                [{"afvalstroom_id": 27, "ophaaldatum": "2026-10-14"}]
            ),
        ]

        with patch(
            "custom_components.afvalinfo.location.trashapi.requests.get",
            side_effect=responses,
        ) as request, patch(
            "custom_components.afvalinfo.location.trashapi.date"
        ) as mocked_date:
            mocked_date.today.return_value = date(2026, 10, 9)
            result = self.run_async(
                TrashApiAfval().get_data(
                    "Gooise Meren",
                    "0000AA",
                    1,
                    "",
                    "",
                    True,
                    ["gft", "papier", "restafval", "pbd"],
                    False,
                )
            )

        self.assertEqual(
            result,
            [
                {"gft": "2026-10-12"},
                {"papier": "2026-10-13"},
                {"restafval": "2026-10-14"},
                {"pbd": "2026-10-14"},
            ],
        )
        self.assertEqual(request.call_count, 4)
        for call in request.call_args_list:
            self.assertEqual(call.kwargs["timeout"], 15)

    def test_trashapi_404_is_reported_as_upstream_failure(self):
        with patch(
            "custom_components.afvalinfo.location.trashapi.requests.get",
            return_value=FakeResponse({"postcode": "redacted"}, status_code=404),
        ):
            with self.assertRaisesRegex(
                AfvalinfoResponseError, "temporarily unavailable or unsupported"
            ):
                self.run_async(
                    TrashApiAfval().get_data(
                        "other", "0000AA", 1, "", "", True, ["gft"], False
                    )
                )

    def test_timeout_is_reported_as_connection_failure(self):
        with patch(
            "custom_components.afvalinfo.location.trashapi.requests.get",
            side_effect=requests.Timeout,
        ):
            with self.assertRaises(AfvalinfoConnectionError):
                self.run_async(
                    TrashApiAfval().get_data(
                        "other", "0000AA", 1, "", "", True, ["gft"], False
                    )
                )

    def test_invalid_schema_is_rejected(self):
        with patch(
            "custom_components.afvalinfo.location.trashapi.requests.get",
            return_value=FakeResponse({"message": "not a collection list"}),
        ):
            with self.assertRaisesRegex(
                AfvalinfoResponseError, "unexpected response"
            ):
                self.run_async(
                    TrashApiAfval().get_data(
                        "other", "0000AA", 1, "", "", True, ["gft"], False
                    )
                )
