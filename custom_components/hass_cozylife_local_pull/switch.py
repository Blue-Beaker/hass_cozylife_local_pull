"""Platform for sensor integration."""
from __future__ import annotations
from datetime import timedelta

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from typing import Any
from .const import (
    DOMAIN
)
from .outlet import OutletDevice
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.info('switch')

SCAN_INTERVAL = timedelta(seconds=10)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    # logging.info('setup_platform', hass, config, add_entities, discovery_info)
    _LOGGER.info('setup_platform')
    _LOGGER.info(f'ip={hass.data[DOMAIN]}')
    
    if discovery_info is None:
        return

    switchs = []
    for item in hass.data[DOMAIN]['outlets']:
        assert isinstance(item,OutletDevice)
        switch=CozyLifeSwitch(item)
        switchs.append(switch)
    
    add_entities(switchs)


class CozyLifeSwitch(SwitchEntity):
    _outlet:OutletDevice
    
    def __init__(self, outlet:OutletDevice) -> None:
        """Initialize the sensor."""
        _LOGGER.info('__init__')
        self._outlet = outlet
        self._unique_id = f"{outlet._id}"
        self._name = f"{outlet._name}"
    
    def _refresh_state(self):
        self._state = self._outlet._refresh_state()
        self._attr_is_on = 0 != self._state['1']
        
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return True
    
    @property
    def is_on(self) -> bool:
        return self._outlet._attr_is_on
    
    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self._unique_id
    
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self._outlet.turn_on()
        return None
    
    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self._outlet.turn_off()
        return None
    
# class CozyLifeSwitch(SwitchEntity):
#     _tcp_client = None
#     _attr_is_on = True
#     _sensors:list[SensorEntity] = []
    
#     def __init__(self, tcp_client:tcp_client) -> None:
#         """Initialize the sensor."""
#         _LOGGER.info('__init__')
#         self._tcp_client = tcp_client
#         self._unique_id = tcp_client.device_id
#         self._name = tcp_client.device_model_name + ' ' + tcp_client.device_id[-4:]
#         self._refresh_state()
#         if(POWER in self._state.keys()):
#             self._sensors.append(PowerSensor(self))
#         if(ENERGY in self._state.keys()):
#             self._sensors.append(EnergySensor(self))
    
#     def _refresh_state(self):
#         self._state = self._tcp_client.query()
#         self._attr_is_on = 0 != self._state['1']
    
#     @property
#     def name(self) -> str:
#         return self._name
    
#     @property
#     def available(self) -> bool:
#         """Return if the device is available."""
#         return True
    
#     @property
#     def is_on(self) -> bool:
#         """Return True if entity is on."""
#         self._attr_is_on = True

#         self._refresh_state()
#         return self._attr_is_on
    
#     @property
#     def unique_id(self) -> str | None:
#         """Return a unique ID."""
#         return self._unique_id
    
#     def turn_on(self, **kwargs: Any) -> None:
#         """Turn the entity on."""
#         self._attr_is_on = True
#         _LOGGER.info(f'turn_on:{kwargs}')
#         self._tcp_client.control({'1': 255})
#         return None
#         raise NotImplementedError()
    
#     def turn_off(self, **kwargs: Any) -> None:
#         """Turn the entity off."""
#         self._attr_is_on = False
#         _LOGGER.info('turn_off')
#         self._tcp_client.control({'1': 0})
#         return None
        
#         raise NotImplementedError()
    