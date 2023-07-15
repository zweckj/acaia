import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_IS_NEW_STYLE_SCALE,
    CONF_MAC_ADDRESS,
    CONF_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class AcaiaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    reauth_entry: ConfigEntry = None

    def __init__(self):
        self._errors = {}
        self._reload = False
        self._discovered = {}

    async def async_step_user(self, user_input=None):
        self._errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_MAC_ADDRESS])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                    title="Acaia", 
                    data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=self._discovered.get(CONF_NAME, "")): str,
                        vol.Required(CONF_MAC_ADDRESS, default=self._discovered.get(CONF_MAC_ADDRESS, "")): str,
                        vol.Optional(CONF_IS_NEW_STYLE_SCALE, default=True): bool,
                    }
                )
            )


    async def async_step_bluetooth(self, discovery_info):
        self._discovered[CONF_MAC_ADDRESS] = discovery_info.address
        self._discovered[CONF_NAME] = discovery_info.name

        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        
        return await self.async_step_user()
    