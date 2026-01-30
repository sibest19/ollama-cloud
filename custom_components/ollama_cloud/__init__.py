"""The Ollama Cloud integration."""

from __future__ import annotations

import asyncio
import logging

import httpx
import ollama

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DEFAULT_TIMEOUT, DOMAIN, OLLAMA_CLOUD_HOST

_LOGGER = logging.getLogger(__name__)

__all__ = [
    "CONF_API_KEY",
    "DOMAIN",
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = (Platform.AI_TASK, Platform.CONVERSATION)

type OllamaCloudConfigEntry = ConfigEntry[ollama.AsyncClient]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Ollama Cloud."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: OllamaCloudConfigEntry) -> bool:
    """Set up Ollama Cloud from a config entry."""
    api_key = entry.data[CONF_API_KEY]

    client = ollama.AsyncClient(
        host=OLLAMA_CLOUD_HOST,
        headers={"Authorization": f"Bearer {api_key}"},
    )

    try:
        async with asyncio.timeout(DEFAULT_TIMEOUT):
            await client.list()
    except httpx.HTTPStatusError as err:
        if err.response.status_code == 401:
            raise ConfigEntryAuthFailed("Invalid API key") from err
        raise ConfigEntryNotReady(f"Error connecting to Ollama Cloud: {err}") from err
    except (TimeoutError, httpx.ConnectError) as err:
        raise ConfigEntryNotReady(f"Timeout connecting to Ollama Cloud: {err}") from err

    entry.runtime_data = client
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Ollama Cloud."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_update_options(
    hass: HomeAssistant, entry: OllamaCloudConfigEntry
) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)
