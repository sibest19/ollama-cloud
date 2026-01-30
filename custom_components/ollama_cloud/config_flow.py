"""Config flow for Ollama Cloud integration."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
import logging
from typing import Any

import httpx
import ollama
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigEntryState,
    ConfigFlow,
    ConfigFlowResult,
    ConfigSubentryFlow,
    SubentryFlowResult,
)
from homeassistant.const import CONF_API_KEY, CONF_LLM_HASS_API, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import llm
from homeassistant.helpers.selector import (
    BooleanSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    TemplateSelector,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from . import OllamaCloudConfigEntry
from .const import (
    CONF_MAX_HISTORY,
    CONF_MODEL,
    CONF_PROMPT,
    CONF_THINK,
    DEFAULT_AI_TASK_NAME,
    DEFAULT_CONVERSATION_NAME,
    DEFAULT_MAX_HISTORY,
    DEFAULT_MODEL,
    DEFAULT_THINK,
    DEFAULT_TIMEOUT,
    DOMAIN,
    MODEL_NAMES,
    OLLAMA_CLOUD_HOST,
    RECOMMENDED_CONVERSATION_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): TextSelector(
            TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
    }
)


async def validate_api_key(api_key: str) -> None:
    """Validate the API key by making a test request."""
    client = ollama.AsyncClient(
        host=OLLAMA_CLOUD_HOST,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with asyncio.timeout(DEFAULT_TIMEOUT):
        await client.list()


class OllamaCloudConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ollama Cloud."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._async_abort_entries_match(user_input)

            try:
                await validate_api_key(user_input[CONF_API_KEY])
            except httpx.HTTPStatusError as err:
                if err.response.status_code == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            except (TimeoutError, httpx.ConnectError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Ollama Cloud",
                    data=user_input,
                    subentries=[
                        {
                            "subentry_type": "conversation",
                            "data": RECOMMENDED_CONVERSATION_OPTIONS,
                            "title": DEFAULT_CONVERSATION_NAME,
                            "unique_id": None,
                        },
                        {
                            "subentry_type": "ai_task_data",
                            "data": {},
                            "title": DEFAULT_AI_TASK_NAME,
                            "unique_id": None,
                        },
                    ],
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                STEP_USER_DATA_SCHEMA, user_input
            ),
            errors=errors,
            description_placeholders={
                "api_key_url": "https://ollama.com/settings/keys",
            },
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Dialog that informs the user that reauth is required."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_api_key(user_input[CONF_API_KEY])
            except httpx.HTTPStatusError as err:
                if err.response.status_code == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            except (TimeoutError, httpx.ConnectError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    self._get_reauth_entry(), data_updates=user_input
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "api_key_url": "https://ollama.com/settings/keys",
            },
        )

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Return subentries supported by this integration."""
        return {
            "conversation": OllamaCloudSubentryFlowHandler,
            "ai_task_data": OllamaCloudSubentryFlowHandler,
        }


class OllamaCloudSubentryFlowHandler(ConfigSubentryFlow):
    """Flow for managing Ollama Cloud subentries."""

    def __init__(self) -> None:
        """Initialize the subentry flow."""
        super().__init__()
        self._name: str | None = None
        self._model: str | None = None
        self._config_data: dict[str, Any] | None = None

    @property
    def _is_new(self) -> bool:
        """Return if this is a new subentry."""
        return self.source == "user"

    @property
    def _client(self) -> ollama.AsyncClient:
        """Return the Ollama client."""
        entry: OllamaCloudConfigEntry = self._get_entry()
        return entry.runtime_data

    async def async_step_set_options(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """Handle model selection and configuration step."""
        if self._get_entry().state != ConfigEntryState.LOADED:
            return self.async_abort(reason="entry_not_loaded")

        if user_input is None:
            # Get available models from Ollama Cloud
            try:
                async with asyncio.timeout(DEFAULT_TIMEOUT):
                    response = await self._client.list()

                available_models: set[str] = {
                    model_info["model"] for model_info in response.get("models", [])
                }
            except (TimeoutError, httpx.ConnectError, httpx.HTTPError):
                _LOGGER.exception("Failed to get models from Ollama Cloud")
                return self.async_abort(reason="cannot_connect")

            # Show available cloud models, highlight those available on the API
            models_to_list = [
                SelectOptionDict(label=f"{m} (available)", value=m)
                for m in sorted(available_models)
                if m in MODEL_NAMES or "cloud" in m.lower()
            ] + [
                SelectOptionDict(label=m, value=m)
                for m in sorted(MODEL_NAMES)
                if m not in available_models
            ]

            # If no models found, just show known cloud models
            if not models_to_list:
                models_to_list = [
                    SelectOptionDict(label=m, value=m) for m in sorted(MODEL_NAMES)
                ]

            if self._is_new:
                options = {}
            else:
                options = self._get_reconfigure_subentry().data.copy()

            return self.async_show_form(
                step_id="set_options",
                data_schema=vol.Schema(
                    ollama_cloud_config_option_schema(
                        self.hass,
                        self._is_new,
                        self._subentry_type,
                        options,
                        models_to_list,
                    )
                ),
            )

        self._model = user_input[CONF_MODEL]
        if self._is_new:
            self._name = user_input.pop(CONF_NAME)

        # Model is available on cloud, create/update the entry
        if self._is_new:
            return self.async_create_entry(
                title=self._name,
                data=user_input,
            )

        return self.async_update_and_abort(
            self._get_entry(),
            self._get_reconfigure_subentry(),
            data=user_input,
        )

    async_step_user = async_step_set_options
    async_step_reconfigure = async_step_set_options


def filter_invalid_llm_apis(hass: HomeAssistant, selected_apis: list[str]) -> list[str]:
    """Accept a list of LLM API IDs and filter against those currently available."""
    valid_llm_apis = [api.id for api in llm.async_get_apis(hass)]
    return [api for api in selected_apis if api in valid_llm_apis]


def ollama_cloud_config_option_schema(
    hass: HomeAssistant,
    is_new: bool,
    subentry_type: str,
    options: Mapping[str, Any],
    models_to_list: list[SelectOptionDict],
) -> dict:
    """Ollama Cloud options schema."""
    if is_new:
        if subentry_type == "ai_task_data":
            default_name = DEFAULT_AI_TASK_NAME
        else:
            default_name = DEFAULT_CONVERSATION_NAME

        schema: dict = {
            vol.Required(CONF_NAME, default=default_name): str,
        }
    else:
        schema = {}

    selected_llm_apis = filter_invalid_llm_apis(
        hass, options.get(CONF_LLM_HASS_API, [])
    )

    schema.update(
        {
            vol.Required(
                CONF_MODEL,
                description={"suggested_value": options.get(CONF_MODEL, DEFAULT_MODEL)},
            ): SelectSelector(
                SelectSelectorConfig(options=models_to_list, custom_value=True)
            ),
        }
    )

    if subentry_type == "conversation":
        schema.update(
            {
                vol.Optional(
                    CONF_PROMPT,
                    description={
                        "suggested_value": options.get(
                            CONF_PROMPT, llm.DEFAULT_INSTRUCTIONS_PROMPT
                        )
                    },
                ): TemplateSelector(),
                vol.Optional(
                    CONF_LLM_HASS_API,
                    description={"suggested_value": selected_llm_apis},
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(
                                label=api.name,
                                value=api.id,
                            )
                            for api in llm.async_get_apis(hass)
                        ],
                        multiple=True,
                    )
                ),
            }
        )

    schema.update(
        {
            vol.Optional(
                CONF_MAX_HISTORY,
                description={
                    "suggested_value": options.get(
                        CONF_MAX_HISTORY, DEFAULT_MAX_HISTORY
                    )
                },
            ): NumberSelector(
                NumberSelectorConfig(
                    min=0, max=100, step=1, mode=NumberSelectorMode.BOX
                )
            ),
            vol.Optional(
                CONF_THINK,
                description={
                    "suggested_value": options.get(CONF_THINK, DEFAULT_THINK),
                },
            ): BooleanSelector(),
        }
    )

    return schema
