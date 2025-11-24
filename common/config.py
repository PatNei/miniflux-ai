from yaml import safe_load
import os


class Config:
    def __init__(self):
        with open('config.yml', encoding='utf8') as f:
            # safe_load can return None if the file is empty / comments only
            data = safe_load(f)
            # ensure we always have a dict
            self.c = data or {}

        self.log_level = self.c.get('log_level', 'INFO')

        self.miniflux_base_url = self.get_config_value('miniflux', 'base_url', None)
        self.miniflux_api_key = self.get_config_value('miniflux', 'api_key', None)
        self.miniflux_webhook_secret = self.get_config_value('miniflux', 'webhook_secret', None)

        self.llm_base_url = self.get_config_value('llm', 'base_url', None)
        self.llm_api_key = self.get_config_value('llm', 'api_key', None)
        self.llm_model = self.get_config_value('llm', 'model', None)
        self.llm_timeout = self.get_config_value('llm', 'timeout', 60)
        self.llm_max_workers = self.get_config_value('llm', 'max_workers', 4)
        self.llm_RPM = self.get_config_value('llm', 'RPM', 1000)

        self.ai_news_url = self.get_config_value('ai_news', 'url', None)
        self.ai_news_schedule = self.get_config_value('ai_news', 'schedule', None)
        self.ai_news_prompts = self.get_config_value('ai_news', 'prompts', None)

        self.agents = self.c.get('agents', {})

    def get_config_value(self, section, key, default=None):
        """
        Priority:
        1. ENV: SECTION_KEY (uppercased)
        2. YAML: c[section][key]
        3. default
        """
        env_key = f"{section}_{key}".upper()

        # 1) Environment variable
        if env_key in os.environ:
            return os.environ[env_key]

        # 2) YAML (guard against self.c being None)
        cfg = self.c or {}
        section_dict = cfg.get(section) or {}

        # 3) default if not found
        return section_dict.get(key, default)
