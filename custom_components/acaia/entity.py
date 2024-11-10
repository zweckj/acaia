"""Base class for acaia entities."""

from collections.abc import Callable
from dataclasses import dataclass

from pyacaia_async.acaiascale import AcaiaScale

from homeassistant.const import CONF_NAME, CONF_MAC
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AcaiaCoordinator


@dataclass(kw_only=True, frozen=True)
class AcaiaEntityDescription(EntityDescription):
    """Description for acaia entities."""

    available_fn: Callable[[AcaiaScale], bool] = lambda scale: scale.connected


@dataclass
class AcaiaEntity(CoordinatorEntity[AcaiaCoordinator]):
    """Common elements for all entities."""

    _attr_has_entity_name = True
    entity_description: AcaiaEntityDescription

    def __init__(
        self,
        coordinator: AcaiaCoordinator,
        entity_description: AcaiaEntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        mac = coordinator.config_entry.data[CONF_MAC]
        self.entity_description = entity_description
        self._scale = coordinator.scale
        self._attr_unique_id = f"{mac}_{entity_description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, mac)},
            name=coordinator.config_entry.data.get(CONF_NAME)
            or coordinator.config_entry.title,
            manufacturer="acaia",
        )

    @property
    def available(self) -> bool:
        """Returns whether entity is available."""
        return super().available and self.entity_description.available_fn(self._scale)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._scale = self.coordinator.scale
        self.async_write_ha_state()
