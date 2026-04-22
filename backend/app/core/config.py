from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_DB:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str

    DATABASE_URL:str | None = None

    QDRANT_URL:str
    QDRANT_API_KEY:str
    QDRANT_COLLECTION:str

    JINA_EMBED_URL:str
    JINA_API_KEY:str

    Gemini_API_KEY:str

    def model_post_init(self, __context):
        self.DATABASE_URL = (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

setting=Settings()