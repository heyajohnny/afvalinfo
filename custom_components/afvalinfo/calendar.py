import logging
import asyncio
from datetime import datetime, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.util import dt as dt_util
from .const.const import DOMAIN, SENSOR_TYPES, SENSOR_PREFIX


async def async_setup_entry(hass, config_entry, async_add_entities):
    try:
        # Wacht tot de sensor het data object heeft aangemaakt
        for _ in range(20):  # max 2 seconden wachten
            data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {}).get("data")
            if data is not None:
                break
            await asyncio.sleep(0.1)
        else:
            # Alleen foutmelding als het echt niet lukt
            logging.getLogger(__name__).error(
                "[afvalinfo.calendar] No data object found for entry: %s",
                config_entry.entry_id,
            )
            return
        name = config_entry.data.get("id", "Afvalinfo")
        async_add_entities([AfvalinfoCalendarEntity(hass, data, name)])
    except Exception as ex:
        logging.getLogger(__name__).error(
            "[afvalinfo.calendar] Error in async_setup_entry: %s", ex
        )


class AfvalinfoCalendarEntity(CalendarEntity):
    def __init__(self, hass, data, name):
        self.hass = hass
        self.data = data
        self._name = f"{SENSOR_PREFIX}{name} calendar"
        self._events = []
        self._attr_unique_id = f"afvalinfo_calendar_{name}"
        self._attr_available = True

    async def async_added_to_hass(self):
        await self.async_update()

    @property
    def name(self):
        return self._name

    async def async_update(self):
        try:
            await self.data.async_update()
            self._events = self._get_events_from_data()
        except Exception as ex:
            logging.getLogger(__name__).error(
                "[afvalinfo.calendar] Error in async_update: %s", ex
            )

    def _get_events_from_data(self):
        events = []
        if not self.data.data:
            return events
        for afvaldict in self.data.data:
            for afvaltype, date_str in afvaldict.items():
                try:
                    if not date_str:
                        continue
                    start = dt_util.as_local(datetime.strptime(date_str, "%Y-%m-%d"))
                    end = start + timedelta(days=1)
                    summary = SENSOR_TYPES.get(afvaltype, [afvaltype])[0]
                    events.append(
                        CalendarEvent(
                            summary=summary,
                            start=start,
                            end=end,
                        )
                    )
                except Exception as ex:
                    logging.getLogger(__name__).error(
                        f"[afvalinfo.calendar] Error parsing event for {afvaltype}: {ex}"
                    )
        return events

    async def async_get_events(self, hass, start_date, end_date):
        await self.async_update()
        filtered = [
            event
            for event in self._events
            if event.start >= start_date and event.start < end_date
        ]
        return filtered

    @property
    def event(self):
        now = dt_util.now().replace(hour=0, minute=0, second=0, microsecond=0)
        future_events = [e for e in self._events if e.start >= now]
        return future_events[0] if future_events else None
