import logging
import time

from homeassistant.components import bluetooth
from homeassistant.exceptions import HomeAssistantError

from pyacaia_async import AcaiaScale

INACTIVITY_TIMEOUT = 120

_LOGGER = logging.getLogger(__name__)

class AcaiaClient(AcaiaScale):

    def __init__(self, hass, mac, name, is_new_style_scale=True):
        self._last_action_timestamp = None
        self.hass = hass
        self._name = name
        super().__init__(mac=mac, is_new_style_scale=is_new_style_scale)


    @property 
    def mac(self):
        return self._mac.upper()
    
    @property
    def name(self):
        return self._name

    async def connect(self, callback=None):
        try:
            if not self._connected:
                """ Get a new client and connect to the scale."""
                ble_device = bluetooth.async_ble_device_from_address(self.hass,
                                                                    self._mac,
                                                                    connectable=True)
                self.new_client_from_ble_device(ble_device)    

                await super().connect(callback=callback)
                self.hass.async_create_task(self._send_heartbeats())
                self.hass.async_create_task(self._process_queue())
                
                
            self._last_action_timestamp = time.time()
        except Exception as ex:
            _LOGGER.warn(f"Couldn't connect to device {self.name} with MAC {self.mac}")


    async def tare(self):
        await self.connect()
        try:
            await super().tare()
        except Exception as ex:
            raise HomeAssistantError("Error taring device") from ex


    async def startStopTimer(self):
        await self.connect()
        try:
            await super().startStopTimer()
        except Exception as ex:
            raise HomeAssistantError("Error starting/stopping timer") from ex
    

    async def resetTimer(self):
        await self.connect()
        try:
            await super().resetTimer()
        except Exception as ex:
            raise HomeAssistantError("Error resetting timer") from ex
