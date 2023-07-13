import logging

from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button entities and services."""

    scale = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            TareButton(scale),
            ResetTimerButton(scale),
            StartStopTimerButton(scale)
        ]
    )


class TareButton(ButtonEntity):
    def __init__(self, scale):
        self._scale = scale
        self._attr_unique_id = f"{self._scale.mac}_" + "tare_button"
        self._attr_name = "Tare"
        self._attr_icon = "mdi:scale-balance"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._scale.tare()


class ResetTimerButton(ButtonEntity):
    def __init__(self, scale):
        self._scale = scale
        self._attr_unique_id = f"{self._scale.mac}_" + "reset_button"
        self._attr_name = "Reset Timer"

    @property
    def icon(self) -> str:
        return "mdi:timer-refresh"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._scale.resetTimer()


class StartStopTimerButton(ButtonEntity):
    def __init__(self, scale):
        self._scale = scale
        self._attr_unique_id = f"{self._scale.mac}_" + "start_stop_button"
        self._attr_name = "Start/Stop Timer"

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