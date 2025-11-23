from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import admin, analyze, check

app = FastAPI()

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 挂载路由
app.include_router(admin.router, prefix="/api/v1")
app.include_router(analyze.router, prefix="/api/v1")
app.include_router(check.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
