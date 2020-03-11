#!/usr/bin/env python3
from datetime import datetime, date, timedelta
from .const.const import (
    _LOGGER,
    ATTR_LAST_UPDATE,
    SENSOR_TYPES,
    SENSOR_PREFIX
)
from homeassistant.helpers.entity import Entity


class AfvalInfoTomorrowSensor(Entity):
    def __init__(self, data, sensor_type, date_format, entities):
        self.data = data
        self.type = sensor_type
        self.date_format = date_format
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

    def update(self):
        self.data.update()
        self._last_update = date.today().strftime("%d-%m-%Y %H:%M")
        self._state = ""  # reset the state
        tomorrow = (date.today() + timedelta(days=1)).strftime(self.date_format)
        for entity in self._entities:
            if entity.state == tomorrow:
                self._state = (self._state + " " + entity.name.split()[1]).strip().lower()