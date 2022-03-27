#!/usr/bin/env python3
from datetime import datetime, date, timedelta
from .const.const import (
    _LOGGER,
    ATTR_LAST_UPDATE,
    ATTR_FRIENDLY_NAME,
    ATTR_YEAR_MONTH_DAY_DATE,
    SENSOR_TYPES,
    SENSOR_PREFIX,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


class AfvalInfoTomorrowSensor(Entity):
    def __init__(
        self, data, sensor_type, sensor_friendly_name, entities, id_name, no_trash_text
    ):
        self.data = data
        self.type = sensor_type
        self.friendly_name = sensor_friendly_name
        self._last_update = None
        self._name = sensor_friendly_name
        self.entity_id = "sensor." + (
            (
                SENSOR_PREFIX
                + (id_name + " " if len(id_name) > 0 else "")
                + sensor_friendly_name
            )
            .lower()
            .replace(" ", "_")
        )
        self._attr_unique_id = (
            SENSOR_PREFIX
            + (id_name + " " if len(id_name) > 0 else "")
            + sensor_friendly_name
        )
        self._no_trash_text = no_trash_text
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
    def extra_state_attributes(self):
        return {ATTR_LAST_UPDATE: self._last_update}

    @Throttle(timedelta(minutes=1))
    def update(self):
        self.data.update()
        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
        # use a tempState to change the real state only on a change...
        tempState = self._no_trash_text
        numberOfMatches = 0
        tomorrow = str((date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
        for entity in self._entities:
            if entity.extra_state_attributes.get(ATTR_YEAR_MONTH_DAY_DATE) == tomorrow:
                # reset tempState to empty string
                if numberOfMatches == 0:
                    tempState = ""
                numberOfMatches = numberOfMatches + 1
                # add trash name to string
                tempState = (
                    (
                        tempState
                        + ", "
                        + entity.extra_state_attributes.get(ATTR_FRIENDLY_NAME)
                    )
                ).strip()
        if tempState.startswith(", "):
            tempState = tempState[2:]
        # only change state if the new state is different than the last state
        if tempState != self._state:
            self._state = tempState
