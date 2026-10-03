"""Tests for the Ollama Cloud integration setup."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import make_http_status_error


async def test_setup_and_unload_entry(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A valid API key sets up the entry and its platform entities."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED
    mock_ollama_client.list.assert_awaited()

    # One conversation entity and one AI task entity were created.
    assert hass.states.get("conversation.ollama_cloud_conversation") is not None
    assert hass.states.get("ai_task.ollama_cloud_ai_task") is not None

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_invalid_auth_triggers_reauth(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A 401 during setup puts the entry into an auth-error state."""
    mock_ollama_client.list.side_effect = make_http_status_error(401)
    mock_config_entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    flows = hass.config_entries.flow.async_progress()
    assert any(flow["context"].get("source") == "reauth" for flow in flows)


async def test_setup_cannot_connect_is_retried(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A connection error during setup schedules a retry."""
    mock_ollama_client.list.side_effect = httpx.ConnectError("boom")
    mock_config_entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_http_error_is_retried(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A non-401 HTTP error during setup schedules a retry."""
    mock_ollama_client.list.side_effect = make_http_status_error(500)
    mock_config_entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
