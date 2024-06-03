from .const.const import (_LOGGER)

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor" ))
    _LOGGER.debug("__init__ set up")
    return True

