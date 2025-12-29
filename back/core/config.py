import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    @property
    def mysql_configured(self) -> bool:
        return all([
            self.DB_HOST,
            self.DB_NAME,
            self.DB_USER,
            self.DB_PASSWORD
        ])

settings = Settings()
