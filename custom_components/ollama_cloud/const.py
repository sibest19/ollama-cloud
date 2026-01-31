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

# Cloud models available on Ollama Cloud
# See: https://ollama.com/search?c=cloud
MODEL_NAMES = [
    "cogito-2.1:671b",
    "deepseek-v3.1:671b",
    "deepseek-v3.2",
    "devstral-2:123b",
    "devstral-small-2:24b",
    "gemini-3-flash-preview",
    "gemini-3-pro-preview",
    "gemma3:4b",
    "gemma3:12b",
    "gemma3:27b",
    "glm-4.6",
    "glm-4.7",
    "gpt-oss:20b",
    "gpt-oss:120b",
    "kimi-k2:1t",
    "kimi-k2.5",
    "kimi-k2-thinking",
    "minimax-m2",
    "minimax-m2.1",
    "ministral-3:3b",
    "ministral-3:8b",
    "ministral-3:14b",
    "mistral-large-3:675b",
    "nemotron-3-nano:30b",
    "qwen3-coder:480b",
    "qwen3-next:80b",
    "qwen3-vl:235b",
    "qwen3-vl:235b-instruct",
    "rnj-1:8b",
]
DEFAULT_MODEL = "deepseek-v3.2"

DEFAULT_CONVERSATION_NAME = "Ollama Cloud Conversation"
DEFAULT_AI_TASK_NAME = "Ollama Cloud AI Task"

RECOMMENDED_CONVERSATION_OPTIONS = {
    CONF_MAX_HISTORY: DEFAULT_MAX_HISTORY,
}
