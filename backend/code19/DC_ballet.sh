#!/bin/bash
a=Valid.         #设置一个变量 a，用于和 stp 输出结果做比较，表示某个约束成立。
Prob=0 # 计算总概率

echo "===== block_size : $1 ; round number : $2 =====" >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt

#$3 为 constrain_flag 表示是否约束差分形式
if [[ "$3" = "1" ]]; then
    echo "                       " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
    echo "======= STATE_0 = $4 =======   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt        #写入输入差分
    echo "======= STATE_$2 = $5 =======   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt       #写入输出差分
fi    

for ((p=0;p<128;p++)) do
    # 获得限定概率为2^(-p)情况下(Δin--->Δout)成立的情况
    echo "                                   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
    echo "=====case that prob = 2^(-$p) =====" >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
    # python3 DC_ballet.py [分组长度v] [轮数r] [约束概率指数p] [是否约束差分形式] [头部差分] [尾部差分]
    python3 DC_ballet.py $1 $2 $p $3 $4 $5
    stp DC_ballet.cvc > current_result.txt
    result=`sed -n "1p" current_result.txt`

    count=0
        while [ "$result" != "$a" ]
    do
        let count+=1
        echo "                       " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
        echo "===== result_$count ===== " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
        echo "                       " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
        
    	cat current_result.txt >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt

        line=`grep -rn "whole_STATE = " current_result.txt`
        wh_res=${line##*=}
        
        In_line=`grep -rn "QUERY" DC_ballet.cvc`
    	var=${In_line%:*}             # 在文件 DC_ballet.cvc 中查找包含 "QUERY" 的行，并提取出那一行的行号
    	
        sed -i "$(($var))i ASSERT( whole_STATE /=$wh_res" DC_ballet.cvc   #insert，在指定行之前插入一行，这里表示在 QUERY 这行前插入一句 ASSERT( whole_STATE /= $wh_res)
        # 其实就是剔除已有的差分路径，找到尽可能多的路径
        stp DC_ballet.cvc > current_result.txt
    	result=`sed -n "1p" current_result.txt`
    done

    echo "                                   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
    echo "===== total $count result ===== " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt

    #如果当前找到的路径数量 count 不为 0，就更新总概率 Prob
    #scale=16 表示小数精度为 16 位；
    #bc -l 启动 bc 的数学库（支持浮点）
    if [[ "$count" != "0" ]]; then
        # 总概率+限定概率为2^(-p)情况下(Δin--->Δout)成立的情况数*2^(-p)
        Prob=`echo "scale=16; $Prob + (1 / ($count*$((2**$p))))" | bc -l`
    fi

    echo "                                   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
    echo "====current power is $p and the sum-Probability is  0$Prob====" >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
done

echo "                                   " >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
echo "====the whole Probability is 0$Prob====" >> DC_result_$1_Blocksize_$2_R_inDiff_is_$4_and_outDiff_is_$5.txt
