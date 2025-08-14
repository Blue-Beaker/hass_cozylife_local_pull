"""Example Load Platform integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType
import logging
import time
from .const import (
    DOMAIN,
    LANG
)
from .utils import get_pid_list
from .udp_discover import get_ip
from .tcp_client import tcp_client
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady,ConfigEntryAuthFailed
from homeassistant.core import HomeAssistant
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


_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    
    """
    TODO:timer discover
    config:{'lang': 'zh', 'ip': ['192.168.5.201', '192.168.5.202', '192.168.5.1']}
}
    """
    ip = get_ip()
    ip_from_config = config[DOMAIN].get('ip') if config[DOMAIN].get('ip') is not None else []    
    
    _LOGGER.info(f'discovered: {ip}, from config: {ip_from_config}')
    ip += ip_from_config
    ip_list = []
    [ip_list.append(i) for i in ip if i not in ip_list]

    if 0 == len(ip_list):
        _LOGGER.info('discover nothing')
        return True

    _LOGGER.info('try conncet ip_list:', ip_list)
    lang_from_config = (config[DOMAIN].get('lang') if config[DOMAIN].get('lang') is not None else LANG)
    get_pid_list(lang_from_config)

    hass.data[DOMAIN] = {
        'temperature': 24,
        'ip': ip_list,
        'tcp_client': [tcp_client(item) for item in ip_list],
        'outlets': []
    }
    _LOGGER.info(f'ip_list={ip_list}, tcp_clients={hass.data[DOMAIN]['tcp_client']}')
    
    time.sleep(3)
    
    for item in hass.data[DOMAIN]['tcp_client']:
        _LOGGER.info(f'ip_list={item}, dict={item.__dict__}')
        if SWITCH_TYPE_CODE == item.device_type_code:
            hass.data[DOMAIN]['outlets'].append(OutletDevice(item))
            
    #wait for get device info from tcp conncetion
    #but it is bad
    # _LOGGER.info('setup', hass, config)
    # hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    hass.loop.call_soon_threadsafe(hass.async_create_task, async_load_platform(hass, 'light', DOMAIN, {}, config))
    hass.loop.call_soon_threadsafe(hass.async_create_task, async_load_platform(hass, 'switch', DOMAIN, {}, config))
    hass.loop.call_soon_threadsafe(hass.async_create_task, async_load_platform(hass, 'sensor', DOMAIN, {}, config))
    return True