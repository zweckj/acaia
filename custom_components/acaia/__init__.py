"""Initialize the Acaia component."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import CONF_MAC_ADDRESS, DOMAIN
from .coordinator import AcaiaApiCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS = ["button", "sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Acaia as config entry."""

    hass.data.setdefault(DOMAIN, {})[
        config_entry.entry_id
    ] = coordinator = AcaiaApiCoordinator(hass, config_entry)

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""

    if config_entry.version == 1:
        new = {**config_entry.data}
        new[CONF_MAC] = new[CONF_MAC_ADDRESS]

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    return True
