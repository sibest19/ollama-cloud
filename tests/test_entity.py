"""Unit tests for the Ollama Cloud entity helpers."""

from __future__ import annotations

from unittest.mock import MagicMock

import ollama
import pytest
import voluptuous as vol
from homeassistant.components import conversation
from homeassistant.helpers import llm

from custom_components.ollama_cloud.entity import (
    _convert_content,
    _fix_invalid_arguments,
    _format_tool,
    _parse_tool_args,
)
from custom_components.ollama_cloud.models import MessageHistory, MessageRole


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ('["a", "b"]', ["a", "b"]),
        ('{"k": 1}', {"k": 1}),
        ("plain string", "plain string"),
        ("[not json]", "[not json]"),
        (42, 42),
        (None, None),
    ],
)
def test_fix_invalid_arguments(value: object, expected: object) -> None:
    """JSON-looking strings are parsed, everything else is passed through."""
    assert _fix_invalid_arguments(value) == expected


def test_parse_tool_args_drops_empty_and_repairs_json() -> None:
    """Empty/None args are dropped and JSON-looking strings repaired."""
    result = _parse_tool_args(
        {
            "name": "kitchen",
            "empty": "",
            "missing": None,
            "list": '["x"]',
        }
    )
    assert result == {"name": "kitchen", "list": ["x"]}


def test_format_tool_converts_parameters_to_json_schema() -> None:
    """Tool parameters become a JSON schema the Ollama client accepts."""
    tool = MagicMock(spec=llm.Tool)
    tool.name = "set_brightness"
    tool.description = "Set a light's brightness"
    tool.parameters = vol.Schema(
        {
            vol.Required("name"): str,
            vol.Optional("brightness"): vol.All(vol.Coerce(int), vol.Range(0, 100)),
        }
    )

    spec = _format_tool(tool, llm.selector_serializer)

    assert spec["type"] == "function"
    assert spec["function"]["name"] == "set_brightness"
    assert spec["function"]["description"] == "Set a light's brightness"
    assert spec["function"]["parameters"] == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
        },
        "required": ["name"],
        "additionalProperties": False,
    }
    # The Ollama client validates tools with pydantic; this must not raise.
    ollama.Tool.model_validate(spec)


def test_convert_content_roundtrips_roles() -> None:
    """Each HA content type maps to the matching Ollama message role."""
    user = _convert_content(conversation.UserContent(content="hello"))
    assert user["role"] == MessageRole.USER.value
    assert user["content"] == "hello"

    system = _convert_content(conversation.SystemContent(content="be nice"))
    assert system["role"] == MessageRole.SYSTEM.value

    tool_result = _convert_content(
        conversation.ToolResultContent(
            agent_id="agent",
            tool_call_id="call-1",
            tool_name="get_state",
            tool_result={"state": "on"},
        )
    )
    assert tool_result["role"] == MessageRole.TOOL.value
    assert '"state": "on"' in tool_result["content"]


def test_message_history_counts_user_messages() -> None:
    """num_user_messages counts only user-role messages."""
    history = MessageHistory(
        messages=[
            ollama.Message(role="system", content="prompt"),
            ollama.Message(role="user", content="hi"),
            ollama.Message(role="assistant", content="hello"),
            ollama.Message(role="user", content="bye"),
        ]
    )
    assert history.num_user_messages == 2
