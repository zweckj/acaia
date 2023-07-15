import logging
from datetime import timedelta

from homeassistant.core import callback
from homeassistant.components import bluetooth
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator,
                                                      UpdateFailed)

from pyacaia_async.decode import Settings, Message

from .const import (
    BATTERY_LEVEL,
    GRAMS,
    UNITS,
    WEIGHT
)

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


class AcaiaApiCoordinator(DataUpdateCoordinator):
    """Class to handle fetching data from the La Marzocco API centrally"""

    def __init__(self, hass, config_entry, acaia_client):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Acaia API coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=SCAN_INTERVAL
        )
        self._device_available = False
        self._data = {
            BATTERY_LEVEL: None,
            UNITS: GRAMS,
            WEIGHT: 0.0
        }

        self._acaia_client = acaia_client

    @property
    def acaia_client(self):
        return self._acaia_client
    

    async def _async_update_data(self):
        try:
            scanner_count = bluetooth.async_scanner_count(self.hass, connectable=True)
            if scanner_count == 0:
                self.acaia_client._connected = False
                _LOGGER.debug("Update coordinator: No bluetooth scanner available")
                return
            
            self._device_available = bluetooth.async_address_present(
                    self.hass, 
                    self._acaia_client.mac, 
                    connectable=True
                )
            
            if not self.acaia_client._connected and self._device_available:
                _LOGGER.debug("Update coordinator: Connecting...")
                await self._acaia_client.connect(callback=self._on_data_received)

            elif not self._device_available:
                self.acaia_client._connected = False
                _LOGGER.debug(f"Update coordinator: Device with MAC {self._acaia_client.mac} not available")

            else:
                await self._acaia_client.auth()
        except Exception as ex:
            _LOGGER.error(ex)
            raise UpdateFailed("Error: %s", str(ex))
        
        return self._data

    @callback
    def _on_data_received(self, characteristic, data):
        """ callback which gets called whenever the websocket receives data """
        if isinstance(data, Settings):
            self._data[BATTERY_LEVEL] = data.battery
            self._data[UNITS] = data.unit
            _LOGGER.debug(f"Got battery level {self._battery_level}, units {self._units}")
            #self.async_set_updated_data(self._battery_level)
        elif isinstance(data, Message):
            self._data[WEIGHT] = data.value
            #self.async_set_updated_data(self._weight)
        self.async_update_listeners()

