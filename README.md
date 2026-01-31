<p align="center">
  <img src="images/icon.png" alt="Ollama" width="100">
</p>

# Ollama Cloud Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This custom integration allows you to use [Ollama Cloud](https://ollama.com) as a conversation agent and AI task provider in Home Assistant.

## Features

- **Conversation Agent**: Use Ollama Cloud models as your Home Assistant voice assistant
- **AI Task Support**: Generate structured data using Ollama Cloud models
- **Multiple Models**: Access cloud-hosted models including LLaMA 3.3, Qwen 3, DeepSeek R1, Mistral Large, and more
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

The integration supports various cloud models hosted on Ollama Cloud:

- Cogito 2.1 (671B)
- DeepSeek v3.1 (671B), v3.2
- Devstral 2 (123B), Small 2 (24B)
- Gemini 3 Pro/Flash Preview
- Gemma 3 (4B, 12B, 27B)
- GLM 4.6, 4.7
- GPT-OSS (20B, 120B)
- Kimi K2 (1T), K2.5, K2-Thinking
- MiniMax M2, M2.1
- Ministral 3 (3B, 8B, 14B)
- Mistral Large 3 (675B)
- Nemotron 3 Nano (30B)
- Qwen 3 Coder (480B), Next (80B), VL (235B)
- RNJ-1 (8B)

## Options

Each conversation agent/AI task can be configured with:

- **Model**: Select which cloud model to use
- **Instructions**: Custom prompt to guide the LLM behavior
- **Control Home Assistant**: Enable tool calling to control devices
- **Max History Messages**: Number of conversation turns to keep in context
- **Think Before Responding**: Enable reasoning mode for improved responses

## Requirements

- Home Assistant 2025.2.4 or later
- An Ollama Cloud API key

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Ollama, Inc. The Ollama name and logo are trademarks of Ollama, Inc. This integration is an independent, community-driven project that uses the publicly available Ollama Cloud API.
