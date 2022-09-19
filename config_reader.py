from pydantic import BaseSettings
from typing import List, Any


class Settings(BaseSettings):
    bot_token: str
    admin_ids: List[int]
    db_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'admin_ids':
                return [int(x) for x in raw_val.split(',')]
            return cls.json_loads(raw_val)


config = Settings()






