
import math
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from typing import Any, Final, Literal, TypedDict, final
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
# from .switch import CozyLifeSwitch
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.info('sensor')

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
    
    sensors = []
    sensors.extend(hass.data[DOMAIN]['sensors'])

    add_entities(sensors)
    
class CozyLifeSwitchSensor(SensorEntity):
    _attr_should_poll=False
    _switch=None
    
    def __init__(self,switch) -> None:
        self._switch=switch
        super().__init__()
        
    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.available:
            return None
        raw_value=self.raw_value
        return raw_value if isinstance(raw_value,float) and math.isfinite(raw_value) else None

    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return None
class PowerSensor(CozyLifeSwitchSensor):
    device_class = SensorDeviceClass.POWER
    native_unit_of_measurement = "W"
    def __init__(self, switch) -> None:
        self._unique_id=f"{switch._unique_id}_power"
        self._name=f"{switch._name} Power"
        super().__init__(switch)
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._switch._state.get(POWER,None)
class EnergySensor(CozyLifeSwitchSensor):
    device_class = SensorDeviceClass.ENERGY
    native_unit_of_measurement = "Wh"
    def __init__(self, switch) -> None:
        self._unique_id=f"{switch._unique_id}_energy"
        self._name=f"{switch._name} Energy"
        super().__init__(switch)
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._switch._state.get(ENERGY,None)