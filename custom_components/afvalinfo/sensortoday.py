#!/usr/bin/env python3
from datetime import datetime, date, timedelta
from .const.const import (
    _LOGGER,
    ATTR_LAST_UPDATE,
    ATTR_YEAR_MONTH_DAY_DATE,
    SENSOR_TYPES,
    SENSOR_PREFIX
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

class AfvalInfoTodaySensor(Entity):
    def __init__(self, data, sensor_type, entities):
        self.data = data
        self.type = sensor_type
        self._last_update = None
        self._name = SENSOR_PREFIX + SENSOR_TYPES[sensor_type][0]
        self._state = None
        self._icon = SENSOR_TYPES[sensor_type][1]
        self._entities = entities

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {ATTR_LAST_UPDATE: self._last_update}

    @Throttle(timedelta(minutes=1))
    def update(self):
        self.data.update()
        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
        self._state = ""  # reset the state
        today = str(date.today().strftime("%Y-%m-%d"))
        for entity in self._entities:
            if entity.device_state_attributes.get(ATTR_YEAR_MONTH_DAY_DATE) == today:
                self._state = (self._state + " " + entity.name.split()[1]).strip().lower()
        if self._state == "":
            self._state = "none"
