"""Collection of useful functions for the HomeKit component."""
import logging

import voluptuous as vol

from homeassistant.core import split_entity_id
from homeassistant.const import (
    ATTR_CODE, TEMP_CELSIUS)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.temperature as temp_util
from .const import HOMEKIT_NOTIFY_ID

_LOGGER = logging.getLogger(__name__)


def validate_entity_config(values):
    """Validate config entry for CONF_ENTITY."""
    entities = {}
    for key, config in values.items():
        entity = cv.entity_id(key)
        params = {}
        if not isinstance(config, dict):
            raise vol.Invalid('The configuration for "{}" must be '
                              ' an dictionary.'.format(entity))

        domain, _ = split_entity_id(entity)

        if domain == 'alarm_control_panel':
            code = config.get(ATTR_CODE)
            params[ATTR_CODE] = cv.string(code) if code else None

        entities[entity] = params
    return entities


def show_setup_message(bridge, hass):
    """Display persistent notification with setup information."""
    pin = bridge.pincode.decode()
    message = 'To setup Home Assistant in the Home App, enter the ' \
              'following code:\n### {}'.format(pin)
    hass.components.persistent_notification.create(
        message, 'HomeKit Setup', HOMEKIT_NOTIFY_ID)


def dismiss_setup_message(hass):
    """Dismiss persistent notification and remove QR code."""
    hass.components.persistent_notification.dismiss(HOMEKIT_NOTIFY_ID)


def convert_to_float(state):
    """Return float of state, catch errors."""
    try:
        return float(state)
    except (ValueError, TypeError):
        return None


def temperature_to_homekit(temperature, unit):
    """Convert temperature to Celsius for HomeKit."""
    return round(temp_util.convert(temperature, unit, TEMP_CELSIUS), 1)


def temperature_to_states(temperature, unit):
    """Convert temperature back from Celsius to Home Assistant unit."""
    return round(temp_util.convert(temperature, TEMP_CELSIUS, unit), 1)
