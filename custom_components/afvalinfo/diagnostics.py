"""Diagnostics support for Afvalinfo."""

from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const.const import DOMAIN

REDACTED = "**REDACTED**"
SENSITIVE_FIELDS = {
    "postcode",
    "streetnumber",
    "streetnumbersuffix",
    "diftarcode",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> dict[str, Any]:
    """Return redacted configuration and provider status."""
    data = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get("data")
    config = {
        key: REDACTED if key in SENSITIVE_FIELDS and value else value
        for key, value in entry.data.items()
    }
    return {
        "config": config,
        "provider": {
            "available": getattr(data, "available", False),
            "last_error": getattr(data, "last_error", None),
            "last_error_type": getattr(data, "last_error_type", None),
        },
    }
