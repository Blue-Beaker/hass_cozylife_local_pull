
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
from .outlet import OutletDevice
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
    for item in hass.data[DOMAIN]['outlets']:
        assert isinstance(item,OutletDevice)
        if(item.has_power_sensor):
            sensors.append(PowerSensor(item))
        if(item.has_energy_sensor):
            sensors.append(EnergySensor(item))
    
    add_entities(sensors)
    
class CozyLifeSwitchSensor(SensorEntity):
    _attr_should_poll=False
    _outlet:OutletDevice
    
    def __init__(self,outlet:OutletDevice) -> None:
        self._outlet=outlet
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
    def __init__(self, outlet) -> None:
        self._unique_id=f"{outlet._id}_power"
        self._name=f"{outlet._name} Power"
        super().__init__(outlet)
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._outlet.power
class EnergySensor(CozyLifeSwitchSensor):
    device_class = SensorDeviceClass.ENERGY
    native_unit_of_measurement = "Wh"
    def __init__(self, outlet) -> None:
        self._unique_id=f"{outlet._id}_energy"
        self._name=f"{outlet._name} Energy"
        super().__init__(outlet)
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._outlet.energy