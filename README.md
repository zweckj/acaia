# Acaia Scales Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)  
[![issues_badge](https://img.shields.io/github/issues-raw/zweckj/acaia-hass-integration?style=for-the-badge)](https://github.com/patrickhilker/tedee_hass_integration/issues)  

This is an integration to control your Acaia Scales. Currently starting/stopping/resetting the timer and taring the scale is supported.

## Installation
### Manually
Copy the contents of the `custom_components` folder to a `acaia` folder in your Home Assistant's `custom_components` folder.

## Setup
This integration requires a Bluetooth connection from HA to your scale. You can use a Bluetooth Proxy if you're not close enough.

After you added the integration to your HA, when you turn your scale on, it should be discovered automatically from Home Assistant