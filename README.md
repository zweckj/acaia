# Acaia Scales Home Assistant Integration

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=zweckj&repository=acaia&category=integration)

This is an integration to control your Acaia Scales. Currently starting/stopping/resetting the timer and taring the scale is supported.

## Installation
### Manually
Copy the contents of the `custom_components` folder to a `acaia` folder in your Home Assistant's `custom_components` folder.

### HACS
You need to add it as [custom repository](https://hacs.xyz/docs/faq/custom_repositories) or click the button above.

## Setup
This integration requires a Bluetooth connection from HA to your scale. You can use an ESP Home [Bluetooth Proxy](https://esphome.github.io/bluetooth-proxies/) if you're not close enough.

After you added the integration to your HA, when you turn your scale on, it should be discovered automatically from Home Assistant.

This integration is tested so far with a Lunar (2021). If you have a different scale, please feel free to test and report back. 

For scale versions before 2021, uncheck the `is_new_style_scale` setting during setup.
