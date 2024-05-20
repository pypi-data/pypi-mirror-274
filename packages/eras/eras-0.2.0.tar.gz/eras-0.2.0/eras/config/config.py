import os


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def get_open_ai_key(self):
        return os.getenv('OPEN_AI_KEY')

    def get_eras_open_ai_key(self):
        return os.getenv('ERAS_OPENAI_KEY')

    def get_eras_base_url(self):
        return os.getenv('ERAS_BASE_URL')


config = Config()
