"""Common fixtures for the Ollama Cloud tests."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ollama_cloud.const import (
    CONF_MODEL,
    DEFAULT_AI_TASK_NAME,
    DEFAULT_CONVERSATION_NAME,
    DEFAULT_MODEL,
    DOMAIN,
    RECOMMENDED_CONVERSATION_OPTIONS,
)

TEST_API_KEY = "test-api-key"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None]:
    """Enable loading of the custom integration in every test."""
    yield


@pytest.fixture(autouse=True)
async def setup_core_components(hass: HomeAssistant) -> None:
    """Set up core components the integration depends on.

    The integration depends on ``conversation``, whose setup in turn requires
    the ``homeassistant`` component (exposed entities). Setting it up here keeps
    every test from tripping over that dependency chain.
    """
    assert await async_setup_component(hass, "homeassistant", {})


def make_http_status_error(status_code: int) -> httpx.HTTPStatusError:
    """Build an httpx.HTTPStatusError with the given status code."""
    request = httpx.Request("GET", "https://ollama.com/api/tags")
    response = httpx.Response(status_code, request=request)
    return httpx.HTTPStatusError(
        f"HTTP {status_code}", request=request, response=response
    )


@pytest.fixture
def mock_ollama_client() -> Generator[MagicMock]:
    """Mock the ollama.AsyncClient used across the integration."""
    with patch("ollama.AsyncClient", autospec=True) as mock_client_cls:
        client = mock_client_cls.return_value
        client.list = AsyncMock(
            return_value={
                "models": [
                    {"model": DEFAULT_MODEL},
                    {"model": "gpt-oss:120b"},
                ]
            }
        )
        client.chat = AsyncMock()
        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry with conversation and AI task subentries."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Ollama Cloud",
        data={CONF_API_KEY: TEST_API_KEY},
        subentries_data=[
            ConfigSubentryData(
                data={**RECOMMENDED_CONVERSATION_OPTIONS, CONF_MODEL: DEFAULT_MODEL},
                subentry_type="conversation",
                title=DEFAULT_CONVERSATION_NAME,
                unique_id=None,
            ),
            ConfigSubentryData(
                data={CONF_MODEL: DEFAULT_MODEL},
                subentry_type="ai_task_data",
                title=DEFAULT_AI_TASK_NAME,
                unique_id=None,
            ),
        ],
    )
