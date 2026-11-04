<p align="center">
  <img src="images/icon.png" alt="Ollama" width="100">
</p>

# Ollama Cloud for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Use [Ollama Cloud](https://ollama.com) models as a **conversation agent** (Assist / voice) and an
**AI Task** provider in Home Assistant. It supports streaming replies, device control through tool
calling, an optional thinking mode, and a live list of every model on Ollama Cloud.

**You need** Home Assistant 2025.9 or newer and an [Ollama Cloud API key](https://ollama.com/settings/keys).

## Install

Click the button, or follow the steps for your Home Assistant version:

[![Open in your Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sibest19&repository=ollama-cloud&category=integration)

<details open>
<summary><b>Home Assistant 2026.11 and newer: Marketplace</b></summary>

1. Go to **Settings → Marketplace**. If this is your first time, accept the warning.
2. Top right, select **Add from link**.
3. Under **GitHub link**, enter `sibest19/ollama-cloud`, then select **Add**. If you are asked
   for a type, choose **Integration**.
4. Open **Ollama Cloud** in the list, install it, then restart Home Assistant.

Upgrading from HACS? You don't need to do anything. The Marketplace takes over your HACS install
and keeps updating it.
</details>

<details>
<summary><b>Home Assistant 2026.10 and older: HACS</b></summary>

1. Open **HACS**, then **⋮ → Custom repositories**.
2. Add `https://github.com/sibest19/ollama-cloud` with the **Integration** type.
3. Search for **Ollama Cloud**, download it, then restart Home Assistant.
</details>

<details>
<summary><b>Manual</b></summary>

Copy `custom_components/ollama_cloud` into your Home Assistant `config/custom_components/`
folder, then restart Home Assistant. You will have to update it by hand.
</details>

## Set up

1. Go to **Settings → Devices & services → Add integration**, then pick **Ollama Cloud**.
2. Paste your API key. This creates a conversation agent and an AI Task entity.
3. To use the agent in Assist, go to **Settings → Voice assistants**, open your assistant and set
   **Conversation agent** to Ollama Cloud.

## Options

On the integration page, select **Reconfigure** on an agent or AI Task to change it. You can also
add more of either, for example one per model.

| Option | What it does |
| --- | --- |
| Model | The Ollama Cloud model to use. The list is loaded live, so new models appear without an update. |
| Instructions | A custom prompt that guides the model. Conversation agent only. |
| Control Home Assistant | Lets the model call Home Assistant tools to control your devices. Conversation agent only. |
| Max history messages | How many conversation turns stay in the context. |
| Think before responding | Turns on reasoning mode, which is slower but often gives better answers. |

The default model, `gpt-oss:20b`, is included in Ollama Cloud's free usage. Other models may need
paid credits. If your plan doesn't include a model, its requests fail with an error asking you to
add credits at [ollama.com/settings](https://ollama.com/settings).

## Help and contributing

Found a bug or want a feature? [Open an issue](https://github.com/sibest19/ollama-cloud/issues/new/choose).
To work on the code, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

This project isn't affiliated with, endorsed by or sponsored by Ollama, Inc. Ollama and its logo
are trademarks of Ollama, Inc.
