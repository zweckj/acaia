import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


BUTTONS = {
    "tare": {
        "name": "Tare",
        "icon": "mdi:scale-balance",
    },
    "reset": {
        "name": "Reset Timer",
        "icon": "mdi:timer-refresh",
    },
    "start_stop": {
        "name": "Start/Stop Timer",
        "icon": "mdi:timer-play",
    }
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            TareButton(coordinator),
            ResetTimerButton(coordinator),
            StartStopTimerButton(coordinator)
        ]
    )


class AcaiaButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, button):
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._scale = coordinator.acaia_client
        self._button = button
        self._attr_unique_id = f"{self._scale.mac}_" + f"{self._button}_button"
        self._attr_name = BUTTONS[self._button]["name"]
        self._attr_icon = BUTTONS[self._button]["icon"]

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._scale.mac)},
            name=self._scale.name,
            manufacturer="acaia"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()



class TareButton(AcaiaButton):

    def __init__(self, scale):
        super().__init__(scale, "tare")

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._scale.tare()



class ResetTimerButton(AcaiaButton):

    def __init__(self, scale):
        super().__init__(scale, "reset")

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._scale.resetTimer()


class StartStopTimerButton(AcaiaButton):

    def __init__(self, scale):
        super().__init__(scale, "start_stop")

    @property
    def icon(self) -> str:
        if not self._scale._timer_running:
            return "mdi:timer-play"
        else:
            return "mdi:timer-pause"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._scale.startStopTimer()
        self.async_write_ha_state()