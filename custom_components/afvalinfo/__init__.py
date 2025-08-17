from .const.const import _LOGGER, DOMAIN

from homeassistant import config_entries
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]


async def async_setup_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    # Bepaal welke platforms geactiveerd moeten worden
    platforms = []
    enabled_sensors = entry.data.get("sensors", [])
    if enabled_sensors:
        platforms.append(Platform.SENSOR)
    if entry.data.get("calendar", False):
        platforms.append(Platform.CALENDAR)
    if not platforms:
        platforms = [Platform.SENSOR]  # fallback
    await hass.config_entries.async_forward_entry_setups(
        entry, [p.value for p in platforms]
    )
    return True


async def async_remove_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    try:
        pass
    except Exception as ex:
        _LOGGER.error("Error removing entry: %s", ex)


async def async_unload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    platforms = []
    enabled_sensors = entry.data.get("sensors", [])
    if enabled_sensors:
        platforms.append(Platform.SENSOR)
    if entry.data.get("calendar", False):
        platforms.append(Platform.CALENDAR)
    if not platforms:
        platforms = [Platform.SENSOR]
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, [p.value for p in platforms]
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
