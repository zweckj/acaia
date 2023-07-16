import logging

from homeassistant.components.sensor import (SensorDeviceClass,
                                             RestoreSensor,
                                             SensorStateClass)
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    BATTERY_LEVEL,
    DOMAIN,
    OUNCES,
    UNITS,
    WEIGHT,
)

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "battery": {
        "name": "Battery",
        "device_class": SensorDeviceClass.BATTERY,
        "unit_of_measurement": "%",
        "state_class": SensorStateClass.MEASUREMENT,
        "property": BATTERY_LEVEL,
        "icon": "mdi:battery"
    },
    "weight": {
        "name": "Weight",
        "device_class": SensorDeviceClass.WEIGHT,
        "unit_of_measurement": "g",
        "state_class": SensorStateClass.MEASUREMENT,
        "property": WEIGHT,
        "icon": "mdi:scale"
    },
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [AcaiaSensor(coordinator, sensor_type) for sensor_type in SENSORS]
    )


class AcaiaSensor(CoordinatorEntity, RestoreSensor):
    def __init__(self, coordinator, sensor_type):
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._scale = coordinator.acaia_client
        self._attr_unique_id = f"{self._scale.mac}_{sensor_type}"
        self._attr_name = SENSORS[sensor_type]["name"]
        self._attr_device_class = SENSORS[sensor_type]["device_class"]
        self._attr_state_class = SENSORS[sensor_type]["state_class"]
        self._attr_icon = SENSORS[sensor_type]["icon"]

        self._sensor_type = sensor_type

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._scale.mac)},
            name=self._scale.name,
            manufacturer="acaia"
        )

        self._native_unit_of_measurement = SENSORS[sensor_type]["unit_of_measurement"]
        self._data = {}
        self._restored = False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._data = self._coordinator.data
        self.async_write_ha_state()


    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._data[SENSORS[self._sensor_type]["property"]] = last_sensor_data.native_value
            self._native_unit_of_measurement  = last_sensor_data.native_unit_of_measurement
            self._restored = True

    @property
    def native_unit_of_measurement(self):
        if not self._sensor_type == WEIGHT or self._restored:
            return self._native_unit_of_measurement
        else:
            units = self._data.get(UNITS)
            return "oz" if units == OUNCES else "g"

    @property
    def native_value(self):
        return self._data.get(SENSORS[self._sensor_type]["property"])