# 字符串转换为布尔值
def str2bool(v: str):
    return v.lower() in ("yes", "true", "t", "1")


# 字符串转换为一维列表
def str2list(v: str):
    return [int(e) for e in v.replace(",", " ").split()]


# 字符串转换为二维列表
def str2list2(v: str):
    return [
        list(map(int, x.split())) if " " in x else list(map(int, x.split(",")))
        for x in v.split("\n")
    ]
