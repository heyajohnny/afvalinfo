import logging
import asyncio
from datetime import datetime, timedelta, date
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.util import dt as dt_util
from .const.const import (
    DOMAIN,
    SENSOR_TYPES,
    SENSOR_PREFIX,
    CONF_CALENDAR_START_TIME,
    CONF_CALENDAR_ALL_DAY,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    try:
        _LOGGER.info(
            "[afvalinfo.calendar] Setting up calendar for entry: %s",
            config_entry.entry_id,
        )

        # Check if calendar is enabled
        if not config_entry.data.get("calendar", False):
            _LOGGER.info(
                "[afvalinfo.calendar] Calendar disabled for entry: %s",
                config_entry.entry_id,
            )
            return

        # Wacht tot de sensor het data object heeft aangemaakt
        data = None
        for attempt in range(20):  # max 2 seconden wachten (verlaagd van 50 naar 20)
            data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {}).get("data")
            if data is not None:
                _LOGGER.info(
                    "[afvalinfo.calendar] Data object found after %d attempts for entry: %s",
                    attempt + 1,
                    config_entry.entry_id,
                )
                break
            await asyncio.sleep(0.1)
        else:
            # Alleen foutmelding als het echt niet lukt
            _LOGGER.error(
                "[afvalinfo.calendar] No data object found after 20 attempts for entry: %s",
                config_entry.entry_id,
            )
            return

        name = config_entry.data.get("id", "Afvalinfo")
        calendar_start_time = config_entry.data.get(CONF_CALENDAR_START_TIME, "20:00")
        calendar_all_day = config_entry.data.get(CONF_CALENDAR_ALL_DAY, False)

        _LOGGER.info(
            "[afvalinfo.calendar] Creating calendar entity for entry: %s with start time: %s, all_day: %s",
            config_entry.entry_id,
            calendar_start_time,
            calendar_all_day,
        )

        async_add_entities(
            [
                AfvalinfoCalendarEntity(
                    hass, data, name, calendar_start_time, calendar_all_day
                )
            ]
        )

        _LOGGER.info(
            "[afvalinfo.calendar] Successfully added calendar entity for entry: %s",
            config_entry.entry_id,
        )

    except Exception as ex:
        _LOGGER.error("[afvalinfo.calendar] Error in async_setup_entry: %s", ex)


class AfvalinfoCalendarEntity(CalendarEntity):
    def __init__(self, hass, data, name, calendar_start_time, calendar_all_day):
        self.hass = hass
        self.data = data
        self._name = f"{SENSOR_PREFIX}{name} calendar"
        self._events = []
        self._attr_unique_id = f"afvalinfo_calendar_{name}"
        self._attr_available = True
        self.calendar_start_time = calendar_start_time
        self.calendar_all_day = calendar_all_day

    async def async_added_to_hass(self):
        """Called when entity is added to hass."""
        await self.async_update()
        # Force Home Assistant to recognize the calendar entity immediately
        self.async_write_ha_state()
        # Trigger a state refresh to ensure UI updates
        self.async_schedule_update_ha_state(True)

    @property
    def name(self):
        return self._name

    async def async_update(self):
        try:
            await self.data.async_update()
            self._events = self._get_events_from_data()
        except Exception as ex:
            _LOGGER.error("[afvalinfo.calendar] Error in async_update: %s", ex)

    def _get_events_from_data(self):
        events = []
        if not self.data.data:
            return events
        for afvaldict in self.data.data:
            for afvaltype, date_str in afvaldict.items():
                try:
                    if not date_str:
                        continue

                    if self.calendar_all_day:
                        # For all-day events, use date objects instead of datetime
                        start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        end_date = start_date  # All-day events end on the same day

                        summary = SENSOR_TYPES.get(afvaltype, [afvaltype])[0]
                        events.append(
                            CalendarEvent(
                                summary=summary,
                                start=start_date,
                                end=end_date,
                            )
                        )
                    else:
                        # For timed events, use datetime objects
                        start = dt_util.as_local(
                            datetime.strptime(date_str, "%Y-%m-%d")
                        )

                        # Parse the configured start time (HH:MM format)
                        try:
                            hour, minute = map(int, self.calendar_start_time.split(":"))
                            start = start.replace(
                                hour=hour, minute=minute, second=0, microsecond=0
                            )
                        except (ValueError, AttributeError):
                            # Fallback to default 20:00 if parsing fails
                            start = start.replace(
                                hour=20, minute=0, second=0, microsecond=0
                            )

                        # End time is start time + 10 minutes
                        end = start + timedelta(minutes=10)

                        summary = SENSOR_TYPES.get(afvaltype, [afvaltype])[0]
                        events.append(
                            CalendarEvent(
                                summary=summary,
                                start=start,
                                end=end,
                            )
                        )
                except Exception as ex:
                    _LOGGER.error(
                        f"[afvalinfo.calendar] Error parsing event for {afvaltype}: {ex}"
                    )
        return events

    def _compare_dates(self, event_start, compare_datetime, reverse=False):
        """Helper function to compare dates and datetimes safely"""
        # Convert both to date objects for comparison
        if isinstance(event_start, datetime):
            event_date = event_start.date()
        else:
            event_date = event_start

        if isinstance(compare_datetime, datetime):
            compare_date = compare_datetime.date()
        else:
            compare_date = compare_datetime

        # Now compare dates
        if reverse:
            return event_date <= compare_date
        else:
            return event_date >= compare_date

    async def async_get_events(self, hass, start_date, end_date):
        await self.async_update()
        filtered = [
            event
            for event in self._events
            if self._compare_dates(event.start, start_date)
            and self._compare_dates(event.start, end_date, reverse=True)
        ]
        return filtered

    @property
    def event(self):
        now = dt_util.now().replace(hour=0, minute=0, second=0, microsecond=0)
        future_events = [e for e in self._events if self._compare_dates(e.start, now)]
        return future_events[0] if future_events else None
