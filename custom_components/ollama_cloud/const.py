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
    "gpt-oss:120b",
    "gpt-oss:120b-cloud",
    "llama3.3",
    "llama3.3:70b",
    "llama3.3:70b-cloud",
    "llama3.1",
    "llama3.1:405b",
    "llama3.1:405b-cloud",
    "qwen3",
    "qwen3:235b",
    "qwen3:235b-cloud",
    "qwq",
    "qwq:32b",
    "qwq:32b-cloud",
    "deepseek-r1",
    "deepseek-r1:671b",
    "deepseek-r1:671b-cloud",
    "mistral-large",
    "mistral-large:123b",
    "mistral-large:123b-cloud",
    "command-r-plus",
    "command-r-plus:104b",
    "command-r-plus:104b-cloud",
]
DEFAULT_MODEL = "llama3.3:70b-cloud"

DEFAULT_CONVERSATION_NAME = "Ollama Cloud Conversation"
DEFAULT_AI_TASK_NAME = "Ollama Cloud AI Task"

RECOMMENDED_CONVERSATION_OPTIONS = {
    CONF_MAX_HISTORY: DEFAULT_MAX_HISTORY,
}
