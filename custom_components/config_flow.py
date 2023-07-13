import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_MAC_ADDRESS,
    DOMAIN,
)


class AcaiaonfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    reauth_entry: ConfigEntry = None

    def __init__(self):
        self._errors = {}
        self._reload = False

    async def async_step_user(self, user_input=None):
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(
                    title="Setup Acaia", 
                    data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {vol.Required(CONF_MAC_ADDRESS): str})
            )
