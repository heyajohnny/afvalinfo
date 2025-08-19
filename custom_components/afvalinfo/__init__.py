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

    # Bepaal welke platforms geactiveerd moeten worden
    platforms = []
    enabled_sensors = entry.data.get("sensors", [])
    if enabled_sensors:
        platforms.append(Platform.SENSOR)
        _LOGGER.info(
            "Sensors enabled for entry %s: %s", entry.entry_id, enabled_sensors
        )

    if entry.data.get("calendar", False):
        platforms.append(Platform.CALENDAR)
        _LOGGER.info("Calendar enabled for entry %s", entry.entry_id)

    if not platforms:
        platforms = [Platform.SENSOR]  # fallback
        _LOGGER.warning(
            "No platforms enabled for entry %s, falling back to sensor only",
            entry.entry_id,
        )

    # Load all required platforms
    _LOGGER.info(
        "Loading platforms for entry %s: %s",
        entry.entry_id,
        [p.value for p in platforms],
    )
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
    try:
        _LOGGER.info("Removing Afvalinfo entry: %s", entry.entry_id)

        # Clear the data for this entry
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            _LOGGER.info("Cleared data for entry %s", entry.entry_id)

        _LOGGER.info("Successfully removed entry %s", entry.entry_id)

    except Exception as ex:
        _LOGGER.error("Error removing entry %s: %s", entry.entry_id, ex)


async def async_unload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    try:
        _LOGGER.info("Unloading Afvalinfo entry: %s", entry.entry_id)

        # Unload all platforms for this entry
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, [Platform.SENSOR, Platform.CALENDAR]
        )

        if unload_ok:
            if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
                hass.data[DOMAIN].pop(entry.entry_id, None)
                _LOGGER.info("Cleared data for entry %s", entry.entry_id)
            _LOGGER.info("Successfully unloaded entry %s", entry.entry_id)
        else:
            _LOGGER.warning(
                "Some platforms failed to unload for entry %s", entry.entry_id
            )

        return unload_ok

    except Exception as ex:
        _LOGGER.error("Error unloading entry %s: %s", entry.entry_id, ex)
        return False


async def async_reload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Reload a config entry."""
    try:
        _LOGGER.info("Reloading Afvalinfo entry: %s", entry.entry_id)

        # First unload all platforms
        _LOGGER.info("Unloading platforms for entry %s", entry.entry_id)
        await hass.config_entries.async_unload_platforms(
            entry, [Platform.SENSOR, Platform.CALENDAR]
        )

        # Clear the data for this entry
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            _LOGGER.info("Cleared data for entry %s", entry.entry_id)

        # Then set up again
        _LOGGER.info("Setting up entry %s again", entry.entry_id)
        await async_setup_entry(hass, entry)

        _LOGGER.info("Successfully reloaded entry %s", entry.entry_id)

    except Exception as ex:
        _LOGGER.error("Error reloading entry %s: %s", entry.entry_id, ex)
        raise
