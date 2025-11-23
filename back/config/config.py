from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]    # 配置 CORS（跨域资源共享） 的允许来源列表

settings = Settings()