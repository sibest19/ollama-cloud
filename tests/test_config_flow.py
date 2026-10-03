"""Tests for the Ollama Cloud config flow."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ollama_cloud.const import CONF_MODEL, DOMAIN

from .conftest import TEST_API_KEY, make_http_status_error


async def test_user_flow_success(
    hass: HomeAssistant,
    mock_ollama_client: MagicMock,
) -> None:
    """A valid API key creates an entry with the two default subentries."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: TEST_API_KEY}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Ollama Cloud"
    assert result["data"] == {CONF_API_KEY: TEST_API_KEY}

    subentry_types = sorted(sub["subentry_type"] for sub in result["subentries"])
    assert subentry_types == ["ai_task_data", "conversation"]
    mock_ollama_client.list.assert_awaited()


@pytest.mark.parametrize(
    ("side_effect", "expected_error"),
    [
        (make_http_status_error(401), "invalid_auth"),
        (make_http_status_error(500), "cannot_connect"),
        (httpx.ConnectError("boom"), "cannot_connect"),
        (TimeoutError(), "cannot_connect"),
        (ValueError("unexpected"), "unknown"),
    ],
)
async def test_user_flow_errors_then_recovers(
    hass: HomeAssistant,
    mock_ollama_client: MagicMock,
    side_effect: Exception,
    expected_error: str,
) -> None:
    """Each failure surfaces the right error and the form recovers afterwards."""
    mock_ollama_client.list.side_effect = side_effect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: TEST_API_KEY}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": expected_error}

    # Clearing the error lets the user retry successfully.
    mock_ollama_client.list.side_effect = None
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: TEST_API_KEY}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_user_flow_duplicate_aborts(
    hass: HomeAssistant,
    mock_ollama_client: MagicMock,
) -> None:
    """Configuring the same API key twice aborts as already configured."""
    MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_KEY: TEST_API_KEY},
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: TEST_API_KEY}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reauth_flow_success(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """Reauth updates the stored API key."""
    mock_config_entry.add_to_hass(hass)

    result = await mock_config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: "new-key"}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert mock_config_entry.data[CONF_API_KEY] == "new-key"


async def test_reauth_flow_invalid_auth(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """A bad key during reauth surfaces invalid_auth."""
    mock_config_entry.add_to_hass(hass)
    mock_ollama_client.list.side_effect = make_http_status_error(401)

    result = await mock_config_entry.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_KEY: "bad-key"}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_conversation_subentry_flow(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ollama_client: MagicMock,
) -> None:
    """Adding a conversation subentry lists models and creates the entry."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.subentries.async_init(
        (mock_config_entry.entry_id, "conversation"),
        context={"source": SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "set_options"
    mock_ollama_client.list.assert_awaited()

    result = await hass.config_entries.subentries.async_configure(
        result["flow_id"],
        {CONF_NAME: "My Agent", CONF_MODEL: "gpt-oss:120b"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My Agent"
    assert result["data"][CONF_MODEL] == "gpt-oss:120b"
