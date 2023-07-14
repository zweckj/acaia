"""
Acaia Integration
"""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .acaiaclient import AcaiaClient
from .coordinator import AcaiaApiCoordinator

from .const import (
    CONF_IS_PYXIS_STYLE,
    CONF_NAME,
    CONF_MAC_ADDRESS, 
    DOMAIN,
)


PLATFORMS = ["button"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Acaia component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass, config_entry):
    """Set up Acaia as config entry."""

    name = config_entry.data[CONF_NAME]
    mac = config_entry.data[CONF_MAC_ADDRESS]
    is_pyxis_style = config_entry.data.get(CONF_IS_PYXIS_STYLE, False)

    acaia_client = AcaiaClient(hass, mac=mac, name=name, is_pyxis_style=is_pyxis_style)

    hass.data[DOMAIN][config_entry.entry_id] = coordinator = AcaiaApiCoordinator(hass, config_entry, acaia_client)

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(
        config_entry,
        PLATFORMS
    )

    return True


async def async_unload_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry
        ):
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry,
        PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok
