"""Constants for the Ollama Cloud integration."""

DOMAIN = "ollama_cloud"

DEFAULT_NAME = "Ollama Cloud"

CONF_MODEL = "model"
CONF_PROMPT = "prompt"
CONF_THINK = "think"
CONF_MAX_HISTORY = "max_history"

DEFAULT_TIMEOUT = 30.0  # seconds (longer timeout for cloud API)
DEFAULT_THINK = False

DEFAULT_MAX_HISTORY = 20
MAX_HISTORY_SECONDS = 60 * 60  # 1 hour

OLLAMA_CLOUD_HOST = "https://ollama.com"

# Cloud models available on Ollama Cloud, as listed by https://ollama.com/api/tags.
# The config flow shows the live list; this is the fallback when it can't be fetched.
MODEL_NAMES = [
    "deepseek-v4-pro:0813",
    "deepseek-v4.1-flash",
    "gemma4:31b",
    "glm-5.2",
    "glm-5.3",
    "glm-5.3-flash",
    "gpt-oss:120b",
    "gpt-oss:20b",
    "kimi-k2.6",
    "kimi-k2.7-code",
    "kimi-k3",
    "minimax-m2.7",
    "minimax-m3",
    "mistral-large-3:675b",
    "nemotron-3-nano:30b",
    "nemotron-3-super",
    "nemotron-3-ultra",
]
# Included in Ollama Cloud's free usage, so it works without paid credits.
DEFAULT_MODEL = "gpt-oss:20b"

DEFAULT_CONVERSATION_NAME = "Ollama Cloud Conversation"
DEFAULT_AI_TASK_NAME = "Ollama Cloud AI Task"

RECOMMENDED_CONVERSATION_OPTIONS = {
    CONF_MAX_HISTORY: DEFAULT_MAX_HISTORY,
}
