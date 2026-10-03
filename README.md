<p align="center">
  <img src="images/icon.png" alt="Ollama" width="100">
</p>

# Ollama Cloud Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This custom integration allows you to use [Ollama Cloud](https://ollama.com) as a conversation agent and AI task provider in Home Assistant.

## Features

- **Conversation Agent**: Use Ollama Cloud models as your Home Assistant voice assistant
- **AI Task Support**: Generate structured data using Ollama Cloud models
- **Multiple Models**: Choose from every model currently available on Ollama Cloud
- **Streaming Responses**: Real-time streaming for responsive conversations
- **Tool Calling**: Control Home Assistant devices through natural language
- **Thinking Mode**: Optional reasoning mode for improved response quality

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sibest19&repository=ollama-cloud&category=integration)
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Add"
7. Search for "Ollama Cloud" and install it
8. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ollama_cloud` directory to your Home Assistant `custom_components` folder
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Ollama Cloud"
4. Enter your Ollama Cloud API key (get one at https://ollama.com/settings/keys)
5. The integration will automatically create a conversation agent and AI task entity

## Available Models

When you add or configure an agent, the model list is loaded live from Ollama Cloud,
so new models show up without updating the integration.

The default model is `gpt-oss:20b`, which is included in Ollama Cloud's free usage.
Other models may need paid usage credits; if a model isn't included in your plan,
requests fail with an error asking you to add credits at https://ollama.com/settings.

## Options

Each conversation agent/AI task can be configured with:

- **Model**: Select which cloud model to use
- **Instructions**: Custom prompt to guide the LLM behavior
- **Control Home Assistant**: Enable tool calling to control devices
- **Max History Messages**: Number of conversation turns to keep in context
- **Think Before Responding**: Enable reasoning mode for improved responses

## Requirements

- Home Assistant 2025.8.0 or later
- An Ollama Cloud API key

## Development

A `Makefile` wraps the common tasks (run `make help` to list them).

Run a local Home Assistant with the integration mounted (requires Docker):

```bash
make up      # start Home Assistant at http://localhost:8123
make logs    # follow the logs
make restart # reload after editing the integration
make down    # stop and remove the container
```

`make dev` starts the container and tails the logs in one step. Home Assistant's
runtime files are written to `config/` (git-ignored except `configuration.yaml`).

Install the dev/test dependencies and run the checks:

```bash
make setup   # pip install -r requirements.test.txt
make lint    # ruff check + format --check
make test    # pytest with coverage
```

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Ollama, Inc. The Ollama name and logo are trademarks of Ollama, Inc. This integration is an independent, community-driven project that uses the publicly available Ollama Cloud API.
