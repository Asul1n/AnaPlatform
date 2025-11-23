import time
import zipfile
import shutil
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependencies import get_current_user
from utils.str_util import *

router = APIRouter(dependencies=[Depends(get_current_user)])


class Form(BaseModel):
    blockLength: int  # 分组长度
    # round: int  # 轮数
    branchNumber: int  # 分支数
    bitPermutation: str  # 比特级置换
    # branchPermutation: str  # 分支置换
    sBoxLength: Union[int, None] = None  # S盒长度
    sBoxContent: Union[str, None] = None  # S盒内容
    linearMatrix: Union[str, None] = None  # 线性矩阵
    nonLinearComponent: list  # 非线性组件
    # code: str  # 代码
    # analyzeType: str  # 分析类型


@router.post("/check/step1")
async def check_step1(data: Form):
    # 如果form.blockLength<=0，则返回错误信息
    if data.blockLength <= 0:
        return JSONResponse(
            {
                "msg": "分组长度输入错误，请检查输入",
                "code": 1,
                "data": {},
            }
        )
    # 如果form.branchNumber<=0，则返回错误信息
    if data.branchNumber <= 0:
        return JSONResponse(
            {
                "msg": "分支数输入错误，请检查输入",
                "code": 1,
                "data": {},
            }
        )
    # 如果form.LinearMatrix不为空，则将form.LinearMatrix转换为一维列表
    if data.linearMatrix is not None:
        linearMatrix = str2list(data.linearMatrix)
        # 如果linerMatrix中存在除0和1以外的元素，则返回错误信息
        for e in linearMatrix:
            if e != 0 and e != 1:
                return JSONResponse(
                    {
                        "msg": "线性矩阵输入错误，请检查输入",
                        "code": 1,
                        "data": {},
                    }
                )
    # form.sBoxContent不为空，则将form.sBoxContent转换为一维列表
    if data.sBoxContent is not None:
        sBoxContent = str2list(data.sBoxContent)
        # 如果sBoxContent中最大值大于等于2^sBoxLength，同时sBoxLength元素个数不等于2^sBoxLength，则返回错误信息
        if (
            max(sBoxContent) >= 2**data.sBoxLength
            or len(sBoxContent) != 2**data.sBoxLength
        ):
            return JSONResponse(
                {
                    "msg": "S盒输入错误，请检查输入",
                    "code": 1,
                    "data": {},
                }
            )

    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {},
        }
    )


@router.post("/check/step2")
async def check_step2(data: dict):
    if data["analyzeType"] == "dc":
        # 1. 读取static/DIF.py.bak文件，将其内容写入static/DIF.py文件
        shutil.copyfile("static/DIF.py.bak", "static/DIF.py")
        # 2. 将data["code"]的每一行前添加4个空格，写入追加static/DIF.py文件
        with open("static/DIF.py", "a") as f:
            lines = data["code"].split("\n")
            f.write("\n")
            for line in lines:
                f.write("    " + line + "\n")
        # 3. 将static/DIF.py文件复制到code/DIF.py文件
        shutil.copyfile("static/DIF.py", "code19/DIF.py")
    elif data["analyzeType"] == "idc":
        shutil.copyfile("static/Impossible.py.bak", "static/Impossible.py")
        with open("static/Impossible.py", "a") as f:
            lines = data["code"].split("\n")
            f.write("\n")
            for line in lines:
                f.write("    " + line + "\n")
        shutil.copyfile("static/Impossible.py", "code19/Impossible.py")
    elif data["analyzeType"] == "lc":
        shutil.copyfile("static/Linear.py.bak", "static/Linear.py")
        with open("static/Linear.py", "a") as f:
            lines = data["code"].split("\n")
            f.write("\n")
            for line in lines:
                f.write("    " + line + "\n")
        shutil.copyfile("static/Linear.py", "code19/Linear.py")
    elif data["analyzeType"] == "zlc":
        shutil.copyfile("static/ZeroCorrelation.py.bak", "static/ZeroCorrelation.py")
        with open("static/ZeroCorrelation.py", "a") as f:
            lines = data["code"].split("\n")
            f.write("\n")
            for line in lines:
                f.write("    " + line + "\n")
        shutil.copyfile("static/ZeroCorrelation.py", "code19/ZeroCorrelation.py")
    else:
        shutil.copyfile("static/Integral.py.bak", "static/Integral.py")
        with open("static/Integral.py", "a") as f:
            lines = data["code"].split("\n")
            f.write("\n")
            for line in lines:
                f.write("    " + line + "\n")
        shutil.copyfile("static/Integral.py", "code19/Integral.py")
    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {},
        }
    )
