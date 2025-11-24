from yaml import safe_load
import os


class Config:
    def __init__(self):
        with open('config.yml', encoding='utf8') as f:
            self.c = safe_load(f)

        self.log_level = self.env_or_yaml("LOG_LEVEL", None, "log_level", "INFO")

        # Miniflux
        self.miniflux_base_url = self.env_or_yaml("MINIFLUX_BASE_URL", "miniflux", "base_url")
        self.miniflux_api_key = self.env_or_yaml("MINIFLUX_API_KEY", "miniflux", "api_key")
        self.miniflux_webhook_secret = self.env_or_yaml("MINIFLUX_WEBHOOK_SECRET", "miniflux", "webhook_secret")

        # LLM
        self.llm_base_url = self.env_or_yaml("LLM_BASE_URL", "llm", "base_url")
        self.llm_api_key = self.env_or_yaml("LLM_API_KEY", "llm", "api_key")
        self.llm_model = self.env_or_yaml("LLM_MODEL", "llm", "model")
        self.llm_timeout = self.env_or_yaml("LLM_TIMEOUT", "llm", "timeout", 60)
        self.llm_max_workers = self.env_or_yaml("LLM_MAX_WORKERS", "llm", "max_workers", 4)
        self.llm_RPM = self.env_or_yaml("LLM_RPM", "llm", "RPM", 1000)

        # AI News
        self.ai_news_url = self.env_or_yaml("AI_NEWS_URL", "ai_news", "url")
        self.ai_news_schedule = self.env_or_yaml("AI_NEWS_SCHEDULE", "ai_news", "schedule")
        self.ai_news_prompts = self.env_or_yaml("AI_NEWS_PROMPTS", "ai_news", "prompts")

        # Agents (usually not environment-based)
        self.agents = self.c.get("agents", {})

    def env_or_yaml(self, env_key, section=None, key=None, default=None):
        """
        Priority:
        1. Environment variable (ENV_KEY)
        2. YAML config: section.key
        3. Default value
        """
        if env_key in os.environ:
            return os.environ[env_key]

        if section and key:
            return self.c.get(section, {}).get(key, default)

        # For top-level items like log_level
        return self.c.get(env_key.lower(), default)
