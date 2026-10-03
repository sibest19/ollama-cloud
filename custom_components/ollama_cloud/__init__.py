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
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.helpers.typing import ConfigType
from homeassistant.util.ssl import get_default_context

from .const import DEFAULT_TIMEOUT, DOMAIN, OLLAMA_CLOUD_HOST

_LOGGER = logging.getLogger(__name__)

__all__ = [
    "CONF_API_KEY",
    "DOMAIN",
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = (Platform.AI_TASK, Platform.CONVERSATION)

type OllamaCloudConfigEntry = ConfigEntry[ollama.AsyncClient]


def create_client(api_key: str) -> ollama.AsyncClient:
    """
    Create an Ollama Cloud client.

    Home Assistant's shared SSL context is passed in so httpx does not load
    certificates (a blocking call) inside the event loop.
    """
    return ollama.AsyncClient(
        host=OLLAMA_CLOUD_HOST,
        headers={"Authorization": f"Bearer {api_key}"},
        verify=get_default_context(),
    )


async def async_validate_api_key(hass: HomeAssistant, api_key: str) -> None:
    """
    Check the API key by asking Ollama Cloud which account it belongs to.

    Listing models is public and listing running models rejects every API key,
    so neither can tell a valid key from a bad one. The ollama client has no
    method for this endpoint, so it is called directly. Errors are raised as
    ollama.ResponseError, like every other Ollama Cloud request.
    """
    async with asyncio.timeout(DEFAULT_TIMEOUT):
        response = await get_async_client(hass).post(
            f"{OLLAMA_CLOUD_HOST}/api/me",
            headers={"Authorization": f"Bearer {api_key}"},
            json={},
        )
    if response.is_error:
        raise ollama.ResponseError(response.text, response.status_code)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Ollama Cloud."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: OllamaCloudConfigEntry) -> bool:
    """Set up Ollama Cloud from a config entry."""
    api_key = entry.data[CONF_API_KEY]

    try:
        await async_validate_api_key(hass, api_key)
    except ollama.ResponseError as err:
        if err.status_code == 401:
            raise ConfigEntryAuthFailed("Invalid API key") from err
        raise ConfigEntryNotReady(f"Error connecting to Ollama Cloud: {err}") from err
    except (TimeoutError, ConnectionError, httpx.HTTPError) as err:
        raise ConfigEntryNotReady(f"Timeout connecting to Ollama Cloud: {err}") from err

    entry.runtime_data = create_client(api_key)
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
