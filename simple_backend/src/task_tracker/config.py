from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_token: str = 'GITHUB_TOKEN'
    gist_id: str = 'GIST_ID'
    cloudflare_account_id: str = 'CLOUDFLARE_ACCOUNT_ID'
    cloudflare_token: str = 'CLOUDFLARE_AUTH_TOKEN'
    cloudflare_model : str = 'CLOUDFLARE_MODEL'

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
