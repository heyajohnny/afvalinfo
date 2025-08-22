from .const.const import _LOGGER, DOMAIN

from homeassistant import config_entries
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]


async def async_setup_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up from a config entry."""
    _LOGGER.info("Setting up Afvalinfo for entry: %s", entry.entry_id)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    # Determine which platforms to activate
    platforms = []
    if entry.data.get("sensors", []):
        platforms.append(Platform.SENSOR)

    if entry.data.get("calendar", False):
        platforms.append(Platform.CALENDAR)

    # Fallback to sensor if no platforms enabled
    if not platforms:
        platforms = [Platform.SENSOR]
        _LOGGER.warning(
            "No platforms enabled for entry %s, falling back to sensor only",
            entry.entry_id,
        )

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(
        entry, [p.value for p in platforms]
    )

    _LOGGER.info(
        "Successfully loaded platforms for %s: %s",
        entry.entry_id,
        [p.value for p in platforms],
    )
    return True


async def async_remove_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Remove a config entry."""
    _LOGGER.info("Removing Afvalinfo entry: %s", entry.entry_id)

    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)


async def async_unload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Afvalinfo entry: %s", entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Reload a config entry."""
    _LOGGER.info("Reloading Afvalinfo entry: %s", entry.entry_id)

    # Unload and reload
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    await async_setup_entry(hass, entry)
