from .const.const import _LOGGER, DOMAIN, CONF_MANUAL_DATES

from homeassistant import config_entries
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import asyncio
import voluptuous as vol

PLATFORMS = [Platform.CALENDAR, Platform.SENSOR]


async def async_setup_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up from a config entry."""
    _LOGGER.info("Setting up Afvalinfo for entry: %s", entry.entry_id)

    # Check if entry is already set up to prevent duplicates
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        _LOGGER.warning(
            "Entry %s is already set up, skipping duplicate setup",
            entry.entry_id,
        )
        return True

    # Initialize the entry data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault("setup_time", {})
    hass.data[DOMAIN][entry.entry_id] = {
        "entry": entry,
        "platforms_loaded": [],
    }

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

    _LOGGER.info(
        "Attempting to load platforms: %s for entry: %s",
        [p.value for p in platforms],
        entry.entry_id,
    )

    # Load sensors first if present
    sensors_loaded = False
    if Platform.SENSOR in platforms:
        try:
            await hass.config_entries.async_forward_entry_setups(
                entry, [Platform.SENSOR]
            )
            _LOGGER.info("Sensors loaded successfully for entry: %s", entry.entry_id)
            sensors_loaded = True
            hass.data[DOMAIN][entry.entry_id]["platforms_loaded"].append(
                Platform.SENSOR
            )

            # Wait a moment for sensors to initialize and create data
            await asyncio.sleep(0.5)
        except Exception as e:
            _LOGGER.error("Failed to load sensors for entry %s: %s", entry.entry_id, e)
            # Don't return False here, try to continue with calendar if possible

    # Load calendar after sensors if present
    calendar_loaded = False
    if Platform.CALENDAR in platforms:
        try:
            await hass.config_entries.async_forward_entry_setups(
                entry, [Platform.CALENDAR]
            )
            _LOGGER.info("Calendar loaded successfully for entry: %s", entry.entry_id)
            calendar_loaded = True
            hass.data[DOMAIN][entry.entry_id]["platforms_loaded"].append(
                Platform.CALENDAR
            )
        except Exception as e:
            _LOGGER.error("Failed to load calendar for entry %s: %s", entry.entry_id, e)
            # Don't fail completely if calendar fails, sensors might still work

    # Check if at least one platform loaded successfully
    if not sensors_loaded and not calendar_loaded:
        _LOGGER.error("No platforms loaded successfully for entry %s", entry.entry_id)
        return False

    # Mark setup as complete
    hass.data[DOMAIN][entry.entry_id]["setup_complete"] = True
    hass.data[DOMAIN]["setup_time"][entry.entry_id] = (
        hass.data[DOMAIN]["setup_time"].get(entry.entry_id, 0) + 1
    )

    _LOGGER.info(
        "Successfully loaded platforms for %s: Sensors: %s, Calendar: %s",
        entry.entry_id,
        "✓" if sensors_loaded else "✗",
        "✓" if calendar_loaded else "✗",
    )

    # Registreer services voor handmatige datums
    await _register_services(hass)

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

    # First, clear the data to force a clean state
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _LOGGER.info("Cleared data for entry %s", entry.entry_id)

    # Unload platforms individually to avoid "never loaded" errors
    for platform in platforms_to_unload:
        try:
            await hass.config_entries.async_unload_platforms(entry, [platform])
            _LOGGER.info(
                "Successfully unloaded platform %s for entry %s",
                platform,
                entry.entry_id,
            )
        except Exception as e:
            _LOGGER.warning(
                "Error unloading platform %s for entry %s during reload: %s",
                platform,
                entry.entry_id,
                e,
            )

    # Wait a moment to ensure cleanup is complete and Home Assistant
    # processes the unload
    await asyncio.sleep(0.5)

    # Force Home Assistant to process the unload before reloading
    await hass.async_block_till_done()

    # Now reload the entry by using the config_entries API to properly reload
    try:
        # Use the proper reload method instead of calling async_setup_entry directly
        # This ensures the config entry state is properly managed
        await hass.config_entries.async_reload(entry.entry_id)
        _LOGGER.info("Successfully reloaded entry %s", entry.entry_id)

        # Force Home Assistant to process the new setup
        await hass.async_block_till_done()

        # Trigger a UI refresh by updating the config entry state
        hass.bus.async_fire("config_entry_reloaded", {"entry_id": entry.entry_id})

    except Exception as e:
        _LOGGER.error("Failed to reload entry %s: %s", entry.entry_id, e)
        # Try to recover by doing a manual setup of the entry
        try:
            # First ensure the entry is properly initialized in hass.data
            hass.data.setdefault(DOMAIN, {})
            hass.data[DOMAIN].setdefault("setup_time", {})
            hass.data[DOMAIN][entry.entry_id] = {
                "entry": entry,
                "platforms_loaded": [],
            }

            # Then manually setup the platforms
            if Platform.SENSOR in platforms_to_unload:
                try:
                    await hass.config_entries.async_forward_entry_setups(
                        entry, [Platform.SENSOR]
                    )
                    _LOGGER.info(
                        "Recovered sensors for entry %s after reload failure",
                        entry.entry_id,
                    )
                except Exception as setups_e:
                    # Fallback to old API if new API fails due to state issues
                    _LOGGER.warning(
                        "async_forward_entry_setups failed, trying async_forward_entry_setup: %s",
                        setups_e,
                    )
                    try:
                        await hass.config_entries.async_forward_entry_setup(
                            entry, Platform.SENSOR
                        )
                        _LOGGER.info(
                            "Recovered sensors using fallback API for entry %s",
                            entry.entry_id,
                        )
                    except Exception as fallback_e:
                        _LOGGER.error(
                            "Both setup methods failed for entry %s: %s",
                            entry.entry_id,
                            fallback_e,
                        )
        except Exception as recovery_e:
            _LOGGER.error(
                "Failed to recover sensors for entry %s: %s",
                entry.entry_id,
                recovery_e,
            )


async def _register_services(hass: HomeAssistant):
    """Registreer services voor handmatige datums"""

    async def add_manual_date(call: ServiceCall):
        """Service om handmatige datum toe te voegen"""
        entry_id = call.data.get("entry_id")
        waste_type = call.data.get("waste_type")
        date_str = call.data.get("date")

        if not entry_id or not waste_type or not date_str:
            _LOGGER.error("Missing required parameters for add_manual_date")
            return

        # Zoek de config entry
        entry = hass.config_entries.async_get_entry(entry_id)
        if not entry:
            _LOGGER.error(f"Config entry {entry_id} not found")
            return

        # Haal huidige handmatige datums op
        import json

        manual_dates_str = entry.data.get(CONF_MANUAL_DATES, "{}")
        try:
            current_manual_dates = (
                json.loads(manual_dates_str) if manual_dates_str else {}
            )
        except (json.JSONDecodeError, TypeError):
            current_manual_dates = {}

        # Voeg nieuwe datum toe
        if waste_type not in current_manual_dates:
            current_manual_dates[waste_type] = []

        if date_str not in current_manual_dates[waste_type]:
            current_manual_dates[waste_type].append(date_str)
            current_manual_dates[waste_type].sort()

            # Update de config entry
            new_data = {
                **entry.data,
                CONF_MANUAL_DATES: json.dumps(current_manual_dates),
            }
            hass.config_entries.async_update_entry(entry, data=new_data)

            # Herlaad de entry
            await hass.config_entries.async_reload(entry.entry_id)

            _LOGGER.info(f"Added manual date {date_str} for {waste_type}")
        else:
            _LOGGER.warning(f"Date {date_str} already exists for {waste_type}")

    async def remove_manual_date(call: ServiceCall):
        """Service om handmatige datum te verwijderen"""
        entry_id = call.data.get("entry_id")
        waste_type = call.data.get("waste_type")
        date_str = call.data.get("date")

        if not entry_id or not waste_type or not date_str:
            _LOGGER.error("Missing required parameters for remove_manual_date")
            return

        # Zoek de config entry
        entry = hass.config_entries.async_get_entry(entry_id)
        if not entry:
            _LOGGER.error(f"Config entry {entry_id} not found")
            return

        # Haal huidige handmatige datums op
        import json

        manual_dates_str = entry.data.get(CONF_MANUAL_DATES, "{}")
        try:
            current_manual_dates = (
                json.loads(manual_dates_str) if manual_dates_str else {}
            )
        except (json.JSONDecodeError, TypeError):
            current_manual_dates = {}

        # Verwijder datum
        if (
            waste_type in current_manual_dates
            and date_str in current_manual_dates[waste_type]
        ):
            current_manual_dates[waste_type].remove(date_str)

            # Verwijder lege lijst
            if not current_manual_dates[waste_type]:
                del current_manual_dates[waste_type]

            # Update de config entry
            new_data = {
                **entry.data,
                CONF_MANUAL_DATES: json.dumps(current_manual_dates),
            }
            hass.config_entries.async_update_entry(entry, data=new_data)

            # Herlaad de entry
            await hass.config_entries.async_reload(entry.entry_id)

            _LOGGER.info(f"Removed manual date {date_str} for {waste_type}")
        else:
            _LOGGER.warning(f"Date {date_str} not found for {waste_type}")

    async def list_manual_dates(call: ServiceCall):
        """Service om handmatige datums op te lijsten"""
        entry_id = call.data.get("entry_id")

        if not entry_id:
            _LOGGER.error("Missing entry_id parameter for list_manual_dates")
            return

        # Zoek de config entry
        entry = hass.config_entries.async_get_entry(entry_id)
        if not entry:
            _LOGGER.error(f"Config entry {entry_id} not found")
            return

        # Haal handmatige datums op
        import json

        manual_dates_str = entry.data.get(CONF_MANUAL_DATES, "{}")
        try:
            manual_dates = json.loads(manual_dates_str) if manual_dates_str else {}
        except (json.JSONDecodeError, TypeError):
            manual_dates = {}

        _LOGGER.info(f"Manual dates for entry {entry_id}: {manual_dates}")
        return manual_dates

    # Registreer services
    hass.services.async_register(
        DOMAIN,
        "add_manual_date",
        add_manual_date,
        schema=vol.Schema(
            {
                vol.Required("entry_id"): str,
                vol.Required("waste_type"): str,
                vol.Required("date"): str,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        "remove_manual_date",
        remove_manual_date,
        schema=vol.Schema(
            {
                vol.Required("entry_id"): str,
                vol.Required("waste_type"): str,
                vol.Required("date"): str,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        "list_manual_dates",
        list_manual_dates,
        schema=vol.Schema(
            {
                vol.Required("entry_id"): str,
            }
        ),
    )
