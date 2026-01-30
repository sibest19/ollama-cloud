# Ollama Cloud Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sibest19&repository=ollama-cloud&category=integration)

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

1. Open HACS in your Home Assistant instance
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

- LLaMA 3.3 (70B)
- LLaMA 3.1 (405B)
- Qwen 3 (235B)
- QwQ (32B)
- DeepSeek R1 (671B)
- Mistral Large (123B)
- Command R+ (104B)
- GPT-OSS (120B)

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
