from .const.const import _LOGGER, DOMAIN

from homeassistant import config_entries
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
import asyncio

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

    # Load sensors first if present
    if Platform.SENSOR in platforms:
        await hass.config_entries.async_forward_entry_setup(entry, Platform.SENSOR)
        _LOGGER.info("Sensors loaded for entry: %s", entry.entry_id)

        # Wait a moment for sensors to initialize and create data
        await asyncio.sleep(0.5)

    # Load calendar after sensors if present
    if Platform.CALENDAR in platforms:
        await hass.config_entries.async_forward_entry_setup(entry, Platform.CALENDAR)
        _LOGGER.info("Calendar loaded for entry: %s", entry.entry_id)

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

    # Determine which platforms were actually loaded for this entry
    platforms_to_unload = []
    if entry.data.get("sensors", []):
        platforms_to_unload.append(Platform.SENSOR)

    if entry.data.get("calendar", False):
        platforms_to_unload.append(Platform.CALENDAR)

    # Fallback to sensor if no platforms were specified
    if not platforms_to_unload:
        platforms_to_unload = [Platform.SENSOR]

    # Unload platforms individually to avoid "never loaded" errors
    unload_ok = True
    for platform in platforms_to_unload:
        try:
            platform_unload_ok = await hass.config_entries.async_unload_platforms(
                entry, [platform]
            )
            if not platform_unload_ok:
                unload_ok = False
                _LOGGER.warning(
                    "Failed to unload platform %s for entry %s",
                    platform,
                    entry.entry_id,
                )
        except Exception as e:
            _LOGGER.warning(
                "Error unloading platform %s for entry %s: %s",
                platform,
                entry.entry_id,
                e,
            )
            unload_ok = False

    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Reload a config entry."""
    _LOGGER.info("Reloading Afvalinfo entry: %s", entry.entry_id)

    # Determine which platforms were actually loaded for this entry
    platforms_to_unload = []
    if entry.data.get("sensors", []):
        platforms_to_unload.append(Platform.SENSOR)

    if entry.data.get("calendar", False):
        platforms_to_unload.append(Platform.CALENDAR)

    # Fallback to sensor if no platforms were specified
    if not platforms_to_unload:
        platforms_to_unload = [Platform.SENSOR]

    # Unload platforms individually to avoid "never loaded" errors
    for platform in platforms_to_unload:
        try:
            await hass.config_entries.async_unload_platforms(entry, [platform])
        except Exception as e:
            _LOGGER.warning(
                "Error unloading platform %s for entry %s during reload: %s",
                platform,
                entry.entry_id,
                e,
            )

    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    await async_setup_entry(hass, entry)
