
from datetime import timedelta
import math
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import (
    DOMAIN
)
from .outlet import OutletDevice
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.info('sensor')

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
    
    sensors = []
    for item in hass.data[DOMAIN]['outlets']:
        assert isinstance(item,OutletDevice)
        if(item.has_power_sensor):
            sensors.append(PowerSensor(item))
        if(item.has_energy_sensor):
            sensors.append(EnergySensor(item))
    
    add_entities(sensors)
    
class OutletSensor(SensorEntity):
    _outlet:OutletDevice
    
    def __init__(self,outlet:OutletDevice) -> None:
        self._outlet=outlet
        self._attr_unique_id=f"{outlet._id}_{self.type_suffix.lower()}"
        self._attr_name=f"{outlet._name} {self.type_suffix}"
        super().__init__()
        
    @property
    def native_value(self):
        """Return the state of the sensor."""
        raw_value=self.raw_value
        _LOGGER.info(f'reading sensor {self.__class__},{self._outlet._state} value={raw_value}')
        self._outlet._refresh_state()
        return raw_value if isinstance(raw_value,int) else None
    
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return None
    @property
    def type_suffix(self):
        return ""
    
    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._outlet.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._outlet.remove_callback(self.async_write_ha_state)
        
class PowerSensor(OutletSensor):
    device_class = SensorDeviceClass.POWER
    native_unit_of_measurement = "W"
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._outlet.power
    @property
    def type_suffix(self):
        return "Power"
class EnergySensor(OutletSensor):
    device_class = SensorDeviceClass.ENERGY
    native_unit_of_measurement = "Wh"
    @property
    def raw_value(self):
        """Return the state of the sensor."""
        return self._outlet.energy
    @property
    def type_suffix(self):
        return "Energy"