"""Tests for the Ollama Cloud AI task entity."""

from __future__ import annotations

from unittest.mock import MagicMock

import ollama
import voluptuous as vol
from homeassistant.components import ai_task
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .test_conversation import _stream


async def test_generate_structured_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A task structure is sent as a JSON schema and the reply parsed into it."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    mock_ollama_client.chat.return_value = _stream(
        ollama.Message(
            role="assistant", content='{"capital": "Rome", "population_millions": 2.8}'
        ),
    )

    result = await ai_task.async_generate_data(
        hass,
        task_name="capital",
        entity_id="ai_task.ollama_cloud_ai_task",
        instructions="Give the capital of Italy and its population in millions.",
        structure=vol.Schema(
            {
                vol.Required("capital"): selector.TextSelector(),
                vol.Required("population_millions"): selector.NumberSelector(),
            }
        ),
    )

    expected_schema = {
        "type": "object",
        "properties": {
            "capital": {"type": "string"},
            "population_millions": {"type": "number"},
        },
        "required": ["capital", "population_millions"],
        "additionalProperties": False,
    }
    assert result.data == {"capital": "Rome", "population_millions": 2.8}
    assert mock_ollama_client.chat.await_args.kwargs["format"] == expected_schema
