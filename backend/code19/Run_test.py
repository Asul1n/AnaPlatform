import os
import time

from cvc_test import test


def out_result(flag_stop, flag_analyse, round_i, Sbox_num_min, result_list):
    if flag_stop == 0:
        result_list.append("成功！" + str(round_i) + "轮达到最少的S盒个数，个数为" + str(Sbox_num_min))
        print("成功！" + str(round_i) + "轮达到最少的S盒个数，个数为" + str(Sbox_num_min))
    elif flag_stop == 1:
        result_list.append(
            "运行超时！ 运行到" + str(round_i) + "轮，最少的活跃S盒个数为" + str(Sbox_num_min)
        )
        print("运行超时！ 运行到" + str(round_i) + "轮，最少S盒个数为" + str(Sbox_num_min))
    elif flag_stop == 2:
        result_list.append(
            "运行成功，运行到"
            + str(round_i)
            + "轮，最少的活跃S盒个数为"
            + str(Sbox_num_min)
            + "\n查看详情差分路线或掩码路线，请下载报告文档查看"
        )
        print(
            "运行成功，运行到"
            + str(round_i)
            + "轮，最少的活跃S盒个数为"
            + str(Sbox_num_min)
            + "\n查看详情差分路线或掩码路线，请下载报告文档查看"
        )
    elif flag_stop == 3:  # 模加差分概率
        result_list.append(
            "运行成功，运行到"
            + str(round_i)
            + "轮，差分路线的最高差分概率为2^{-"
            + str(Sbox_num_min)
            + "}"
            + "\n查看详情差分路线，请下载报告文档查看"
        )
        print(
            "运行成功，运行到"
            + str(round_i)
            + "轮，差分路线的最高差分概率为2^{-"
            + str(Sbox_num_min)
            + "}"
            + "\n查看详情差分路线，请下载报告文档查看"
        )
    elif flag_stop == 4:  # 模加掩码概率
        result_list.append(
            "运行成功，截止运行到"
            + str(round_i)
            + "轮，线性掩码路线的最高相关度为2^{-"
            + str(Sbox_num_min)
            + "}，"
            + "\n查看详情掩码路线，请下载报告文档查看"
        )
        print(
            "运行成功，截止运行到"
            + str(round_i)
            + "轮，线性掩码路线的最高相关度为2^{-"
            + str(Sbox_num_min)
            + "}，"
            + "\n查看详情掩码路线，请下载报告文档查看"
        )

    else:
        print("Unknown error")
        return


def testDIFanalyse(
    Blocksize,       # 分组长度（比如 64 bit）
    Round,           # 总轮数
    Branch_number,   # 线性层的分支数
    Sbox_bit,        # S盒输入/输出位宽
    Sbox_content,    # S盒具体映射内容（如 [0x6,0x5,0xC,...]）
    Matrix,          # 线性变换矩阵（比如 MDS 矩阵）
    NonlinearType,   # 非线性类型（'Sbox' 或 其他）
    Sbox_num_min,    # 最小 S盒个数或差分幂次的上限
):
    result_list = []

    for round_i in range(1, Round + 1):
        left = 0    # left 表示当前已验证的最小活跃数起点
        """ test 是一个类（未在本段代码中定义），它负责：
            根据当前轮数 round_i 构造差分传播模型；
            生成 .cvc 约束文件供 STP 求解。 """
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        # 注意这里创建Mytest对象的时候第二个参数为本轮的round_i
        # 每一轮都建立一个对象

        for S_num_i in range(left, Sbox_num_min):  # 从小到大开始试
            Mytest.DIFanalyze(S_num_i)

            time_start = time.time()
            re = os.popen("'stp' 'static/cvc/DIF.cvc'")
            re = re.readlines()
            # print(re)
            time_end = time.time()
            timeuse = time_end - time_start

            if re[-1] == "Invalid.\n":
                left = S_num_i
                if NonlinearType == "Sbox":
                    print(
                        str(round_i)
                        + "轮，最少活跃S盒个数为"
                        + str(S_num_i)
                        + "    STP求解用时".ljust(10)
                        + str(format(timeuse, ".3f"))
                        + "秒"
                    )
                    result_list.append(str(round_i) + "轮，最少活跃S盒个数为" + str(S_num_i))
                else:
                    print(
                        str(round_i)
                        + "轮加密算法，差分路线的最高差分概率为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                    result_list.append(
                        str(round_i)
                        + "轮加密算法，差分路线的最高差分概率为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                if left == Sbox_num_min or timeuse >= 3000:
                    f = open(
                        "static/result/差分.txt",
                        "w",
                    )
                    # print(f)
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if left == Sbox_num_min:
                        out_result(0, "DIF", round_i, Sbox_num_min, result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif timeuse >= 3000:
                        out_result(1, "DIF", round_i, S_num_i, result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    return result_list
                break
        if round_i == Round:
            if NonlinearType == "Sbox":
                f = open(
                    "static/result/差分.txt",
                    "w",
                )
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(2, "DIF", round_i, S_num_i, result_list)
            else:
                f = open(
                    "static/result/差分.txt",
                    "w",
                )
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(3, "DIF", round_i, S_num_i, result_list)
    return result_list


def testLinearanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        left = 0
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )

        for S_num_i in range(left, Sbox_num_min):  # 从小到大开始试
            Mytest.Linearanalyze(S_num_i)

            time_start = time.time()
            re = os.popen("'stp' 'static/cvc/Linear.cvc'")
            re = re.readlines()
            # print(re)
            time_end = time.time()
            timeuse = time_end - time_start

            if re[-1] == "Invalid.\n":
                left = S_num_i
                if NonlinearType == "Sbox":
                    # print(str(round_i) + "轮加密算法，最少活跃S盒个数为" + str(S_num_i) + "    STP求解用时" + str(timeuse) + "秒")
                    print(
                        str(round_i)
                        + "轮加密算法，最少活跃S盒个数为"
                        + str(S_num_i)
                        + "    STP求解用时"
                        + str(format(timeuse, ".3f"))
                        + "秒"
                    )
                    result_list.append(str(round_i) + "轮加密算法，最少活跃S盒个数为" + str(S_num_i))
                else:
                    print(
                        str(round_i)
                        + "轮加密算法，线性掩码路线的最高相关度为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                    # print(str(round_i) + "轮加密算法，差分路线的最高差分概率为2^{-" + str(S_num_i) + "}    STP求解用时" + str(timeuse) +
                    # "秒")
                    result_list.append(
                        str(round_i)
                        + "轮加密算法，线性掩码路线的最高相关度为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )

                if left == Sbox_num_min or timeuse >= 3000:
                    f = open("static/result/线性.txt", "w")
                    # print(f)
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if left == Sbox_num_min:
                        out_result(0, "Linear", round_i, Sbox_num_min, result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif timeuse >= 3000:
                        out_result(1, "Linear", round_i, S_num_i, result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    return result_list
                break
        if round_i == Round:
            if NonlinearType == "Sbox":
                f = open("static/result/线性.txt", "w")
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(2, "Linear", round_i, S_num_i, result_list)
            else:
                f = open("static/result/线性.txt", "w")
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(4, "Linear", round_i, S_num_i, result_list)
    return result_list



def DifferentialAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    Sbox_num_min = 100
    result_context = []
    print("==========差分分析==========")
    DIF_context = testDIFanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )
    # print(DIF_context)

    result_context.append("========差分分析=======")
    result_context += DIF_context

    return result_context  # 这个return可以给分析报告用


def LinearAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    Sbox_num_min = 100
    result_context = []
    print("==========线性分析==========")
    Linear_context = testLinearanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )
    # print(Linear_context)

    result_context.append("========线性分析=======")
    result_context += Linear_context

    return result_context
