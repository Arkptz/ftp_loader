from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cdn_url:str = "https://cdn.vitrinagram.ru"
    path_with_images:str = './images'

SETTINGS = Settings()
