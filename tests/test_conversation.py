"""Tests for the Ollama Cloud conversation agent."""

from __future__ import annotations

from collections.abc import AsyncIterator
from unittest.mock import MagicMock

import ollama
from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import intent
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ollama_cloud.const import DEFAULT_MODEL


def _stream(*chunks: ollama.Message) -> AsyncIterator[ollama.ChatResponse]:
    """Build an async iterator of streaming chat responses."""

    async def _gen() -> AsyncIterator[ollama.ChatResponse]:
        for message in chunks:
            yield ollama.ChatResponse(model=DEFAULT_MODEL, message=message)

    return _gen()


async def test_conversation_returns_streamed_reply(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A streamed assistant reply is assembled into the conversation result."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    mock_ollama_client.chat.return_value = _stream(
        ollama.Message(role="assistant", content="Hello"),
        ollama.Message(role="assistant", content=" world"),
    )

    result = await conversation.async_converse(
        hass,
        "hi there",
        conversation_id=None,
        context=Context(),
        agent_id="conversation.ollama_cloud_conversation",
    )

    assert result.response.response_type == intent.IntentResponseType.ACTION_DONE
    assert result.response.speech["plain"]["speech"] == "Hello world"

    # The model configured on the subentry was the one queried.
    assert mock_ollama_client.chat.await_args.kwargs["model"] == DEFAULT_MODEL
    assert mock_ollama_client.chat.await_args.kwargs["stream"] is True
