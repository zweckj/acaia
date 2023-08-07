import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

BINARY_SENSORS = {
    "timer_running": {
        "name": "Timer running",
        "device_class": BinarySensorDeviceClass.RUNNING,
        "icon": "mdi:timer",
        "value_attr": "_timer_running"
    },
    "connected": {
        "name": "Connected",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "icon": "mdi:bluetooth",
        "value_attr": "_connected"
    }
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [AcaiaSensor(coordinator, sensor_type) for sensor_type in BINARY_SENSORS]
    )


class AcaiaSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, sensor_type):
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._scale = coordinator.acaia_client
        self._attr_unique_id = f"{self._scale.mac}_{sensor_type}"
        self._attr_name = BINARY_SENSORS[sensor_type]["name"]
        self._attr_device_class = BINARY_SENSORS[sensor_type]["device_class"]
        self._attr_icon = BINARY_SENSORS[sensor_type]["icon"]
        self._value_attr = BINARY_SENSORS[sensor_type]["value_attr"]

        self._sensor_type = sensor_type

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._scale.mac)},
            name=self._scale.name,
            manufacturer="acaia"
        )

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return getattr(self._scale, self._value_attr)