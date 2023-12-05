from .const.const import (
    MIN_TIME_BETWEEN_UPDATES,
    _LOGGER,
    CONF_ENABLED_SENSORS,
    CONF_CITY,
    CONF_DISTRICT,
    CONF_LOCATION,
    CONF_POSTCODE,
    CONF_STREET_NUMBER,
    CONF_STREET_NUMBER_SUFFIX,
    CONF_GET_WHOLE_YEAR,
    CONF_DATE_FORMAT,
    CONF_TIMESPAN_IN_DAYS,
    CONF_NO_TRASH_TEXT,
    CONF_DIFTAR_CODE,
    CONF_LOCALE,
    CONF_ID)

from .sensor import (AfvalinfoData,AfvalinfoSensor)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor" ))
    _LOGGER.debug("__init__ set up")
    return True

