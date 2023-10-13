"""Acaia Scale Client for Home Assistant."""
import logging
import time

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from pyacaia_async import AcaiaScale


_LOGGER = logging.getLogger(__name__)

class AcaiaClient(AcaiaScale):
    """Client to interact with Acaia Scales."""

    def __init__(self, hass: HomeAssistant, mac: str, name: str, is_new_style_scale: bool=True):
        """Initialize the client."""
        self._last_action_timestamp = None
        self.hass = hass
        self._name = name
        super().__init__(mac=mac, is_new_style_scale=is_new_style_scale)


    @property 
    def mac(self) -> str:
        """Return the mac address of the scale in upper case."""
        return self._mac.upper()
    
    @property
    def name(self) -> str:
        """Return the name of the scale."""
        return self._name

    async def connect(self, callback=None) -> None:
        """Connect to the scale."""
        try:
            if not self._connected:
                # Get a new client and connect to the scale.
                ble_device = bluetooth.async_ble_device_from_address(self.hass,
                                                                    self._mac,
                                                                    connectable=True)
                self.new_client_from_ble_device(ble_device)    

                await super().connect(callback=callback)
                interval = 1 if self._is_new_style_scale else 5
                self.hass.async_create_task(
                    self._send_heartbeats(
                        interval=interval, 
                        new_style_heartbeat=self._is_new_style_scale
                        )
                    )
                self.hass.async_create_task(self._process_queue())
                               
            self._last_action_timestamp = time.time()
        except Exception as ex:
            _LOGGER.warning(f"Couldn't connect to device {self.name} with MAC {self.mac}")
            _LOGGER.debug("Full error: %s", str(ex))


    async def tare(self) -> None:
        """Tare the scale."""
        await self.connect()
        try:
            await super().tare()
        except Exception as ex:
            raise HomeAssistantError("Error taring device") from ex


    async def startStopTimer(self) -> None:
        """Start/Stop the timer."""
        await self.connect()
        try:
            await super().startStopTimer()
        except Exception as ex:
            raise HomeAssistantError("Error starting/stopping timer") from ex
    

    async def resetTimer(self) -> None:
        """Reset the timer."""
        await self.connect()
        try:
            await super().resetTimer()
        except Exception as ex:
            raise HomeAssistantError("Error resetting timer") from ex
