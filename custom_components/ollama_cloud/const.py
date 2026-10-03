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
    "deepseek-v4-flash",
    "deepseek-v4.1-flash",
    "deepseek-v4-pro",
    "gemma4:12b",
    "gemma4:26b",
    "gemma4:31b",
    "glm-5.1",
    "glm-5.2",
    "glm-5.3",
    "glm-5.3-flash",
    "gpt-oss:20b",
    "gpt-oss:120b",
    "kimi-k2.6",
    "kimi-k2.7-code",
    "kimi-k3",
    "minimax-m2.7",
    "minimax-m3",
    "mistral-large-3",
    "nemotron-3-nano:4b",
    "nemotron-3-nano:30b",
    "nemotron-3-super:120b",
    "nemotron-3-ultra",
    "qwen3.5:0.8b",
    "qwen3.5:2b",
    "qwen3.5:4b",
    "qwen3.5:9b",
    "qwen3.5:27b",
    "qwen3.5:35b",
    "qwen3.5:122b",
]
DEFAULT_MODEL = "deepseek-v4.1-flash"

DEFAULT_CONVERSATION_NAME = "Ollama Cloud Conversation"
DEFAULT_AI_TASK_NAME = "Ollama Cloud AI Task"

RECOMMENDED_CONVERSATION_OPTIONS = {
    CONF_MAX_HISTORY: DEFAULT_MAX_HISTORY,
}
