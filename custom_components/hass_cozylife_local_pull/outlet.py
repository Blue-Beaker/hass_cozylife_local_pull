from __future__ import annotations
import logging
import asyncio
import time
import traceback
from typing import Any, Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.sensor import SensorEntity
from .tcp_client import tcp_client
from .const import (
    DOMAIN,
    SWITCH_TYPE_CODE,
    LIGHT_TYPE_CODE,
    LIGHT_DPID,
    SWITCH,
    WORK_MODE,
    TEMP,
    BRIGHT,
    HUE,
    SAT,
    ENERGY,
    POWER
)

import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.info('outlet')

class OutletDevice:
    _state=None
    _tcp_client = None
    _attr_is_on = True
    # switch: SwitchEntity
    # power_sensor:SensorEntity
    # energy_sensor:SensorEntity
    def __init__(self, tcp_client:tcp_client):
        self._tcp_client = tcp_client
        self._id=tcp_client.device_id
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self.model = ""
        self._state={}
        self._name = f"{tcp_client.device_model_name} {tcp_client.device_id[-4:]}"
        self._refresh_state()
        """Initialize the sensor."""
        _LOGGER.info('__init__')
        
    @property
    def has_power_sensor(self):
        return POWER in self._state.keys()
    @property
    def has_energy_sensor(self):
        return ENERGY in self._state.keys()
            
    def _refresh_state(self):
        self._state = self._tcp_client.query()
        self._attr_is_on = 0 != self._state['1']

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self._attr_is_on = True
        _LOGGER.info(f'turn_on:{kwargs}')
        self._tcp_client.control({'1': 255})
        return None
    
    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self._attr_is_on = False
        _LOGGER.info('turn_off')
        self._tcp_client.control({'1': 0})
        return None


    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)    
        
    @property
    def power(self) -> float|None:
        return self._state.get(POWER,None)
    @property
    def energy(self) -> float|None:
        return self._state.get(ENERGY,None)
