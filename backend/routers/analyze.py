import time
import zipfile
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from code19.Run_test import (
    DifferentialAnalyse,
    ImpossibleAnalyse,
    IntegralAnalyse,
    LinearAnalyse,
    ZeroCorrelationAnalyse,
)
from dependencies import get_current_user
from utils.str_util import str2bool, str2list, str2list2

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
    code: str  # 代码
    analyzeType: str  # 分析类型 dc lc idc zlc ic


@router.post("/analyze")
async def analyze(data: Form):
    if not str2bool(data.bitPermutation):
        data.linearMatrix = "0 1\n1 0"
    if data.nonLinearComponent[0] == "modulo":
        data.sBoxLength = 2
        data.sBoxContent = "0 1 2 3"
    result = []
    if data.analyzeType == "dc":
        result = DifferentialAnalyse(
                data.blockLength,
                5,
                data.branchNumber,
                data.sBoxLength,
                str2list(data.sBoxContent),
                str2list2(data.linearMatrix),
                data.nonLinearComponent.pop(),
            )
        # time.sleep(5)
        # result = [
        #     "==========差分分析==========",
        #     "1轮加密算法，差分路线的最高差分概率为2^{-0}",
        #     "2轮加密算法，差分路线的最高差分概率为2^{-0}",
        #     "3轮加密算法，差分路线的最高差分概率为2^{-2}",
        #     "4轮加密算法，差分路线的最高差分概率为2^{-19}",
        #     "5轮加密算法，差分路线的最高差分概率为2^{-29}",
        # ]
        # 将差分.txt文件的内容写入route.txt
        with open("static/result/route.txt", "w") as f:
            f.write(open("static/result/差分.txt", "r").read())
        # 将result写入result.txt
        with open("static/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))

    elif data.analyzeType == "idc":
        result = ImpossibleAnalyse(
            data.blockLength,
            6,
            data.branchNumber,
            data.sBoxLength,
            str2list(data.sBoxContent),
            str2list2(data.linearMatrix),
            data.nonLinearComponent.pop(),
        )

        # 将result写入result.txt
        with open("static/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))
    elif data.analyzeType == "lc":
        result = LinearAnalyse(
            data.blockLength,
            5,
            data.branchNumber,
            data.sBoxLength,
            str2list(data.sBoxContent),
            str2list2(data.linearMatrix),
            data.nonLinearComponent.pop(),
        )
        # result = [
        #     "==========线性分析==========",
        #     "1轮加密算法，线性掩码路线的最优相关度为2^{-0}",
        #     "2轮加密算法，线性掩码路线的最优相关度为2^{-1}",
        #     "3轮加密算法，线性掩码路线的最优相关度为2^{-1}",
        #     "4轮加密算法，线性掩码路线的最优相关度为2^{-5}",
        #     "5轮加密算法，线性掩码路线的最优相关度为2^{-9}",
        #     "6轮加密算法，线性掩码路线的最优相关度为2^{-17}",
        # ]
        # 将result写入result.txt
        with open("static/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))
        # 将线性.txt文件的内容写入route.txt
        with open("static/result/route.txt", "w") as f:
            f.write(open("static/result/线性.txt", "r").read())

    elif data.analyzeType == "zlc":
        result = ZeroCorrelationAnalyse(
            data.blockLength,
            6,
            data.branchNumber,
            data.sBoxLength,
            str2list(data.sBoxContent),
            str2list2(data.linearMatrix),
            data.nonLinearComponent.pop(),
        )
        # 将result写入result.txt
        with open("static/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))
    else:
        result = IntegralAnalyse(
            data.blockLength,
            6,
            data.branchNumber,
            data.sBoxLength,
            str2list(data.sBoxContent),
            str2list2(data.linearMatrix),
            data.nonLinearComponent.pop(),
        )
        # 将result写入result.txt
        with open("static/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))
        # 将积分.txt文件的内容写入route.txt
        with open("static/result/route.txt", "w") as f:
            f.write(open("static/result/积分.txt", "r").read())
    # 压缩result.txt和route.txt为archive.zip
    with zipfile.ZipFile("static/result/archive.zip", "w") as z:
        z.write("static/result/result.txt")
        z.write("static/result/route.txt")

    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {
                "result": open("static/result/result.txt", "r").read(),
                "url_result": "http://127.0.0.1:8000/static/result/result.txt",
                "url_route": "http://127.0.0.1:8000/static/result/route.txt",
                "url_archive": "http://127.0.0.1:8000/static/result/archive.zip",
            },
        }
    )
