from fastapi import FastAPI 
from config.middleware import register_cors

app = FastAPI()

# 注册中间件
register_cors(app)

# 示例路由
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# 模拟一个接口返回用户数据
@app.get("/api/users")
def get_users():
    return [
        {"id": 1, "name": "Asuka"},
        {"id": 2, "name": "Rei"},
        {"id": 3, "name": "Shinji"},
    ]

# 模拟一个登录接口
@app.post("/api/login")
def login(user: dict):
    if user["username"] == "admin" and user["password"] == "123456":
        return {"success": True, "name": "Admin", "token": "fake-jwt-token"}
    else:
        return {"success": False, "msg": "用户名或密码错误"}

@app.get("/diff-paths")
def get_diff_paths():
    paths = [
        {
            "name": "四轮路线",
            "totalProb": "2⁻6",
            "sum_probability": "0.0156250000000000",
            "rounds": [
                {"xa": "0x80000000", "xb": "0x80000000", "xc": "0x80000000", "xd": "0x80000000"},
                {"xa": "0x00000000", "xb": "0x00000000", "xc": "0x00000000", "xd": "0x80000000"},
            ],
        },
        # 你可以这里返回更多条路径
    ]
    return {"paths": paths, "total_probability": 0.8763157639378506}