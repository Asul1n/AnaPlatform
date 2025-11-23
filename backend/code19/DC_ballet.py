import sys
from cvc_test import test

def usage():
    print("用法: python3 run_gathered.py <blocksize> <round> <con> <input_diff_hex> <output_diff_hex> [Branch_number] [Sbox_bit] [NonlinearType]")
    sys.exit(1)

if len(sys.argv) < 6:
    usage()

blocksize = int(sys.argv[1])
rounds = int(sys.argv[2])
power = int(sys.argv[3])
con = int(sys.argv[4])
input_hex = int(str(sys.argv[5]),16)
output_hex = int(str(sys.argv[6]),16)

Branch_number = int(sys.argv[7]) if len(sys.argv) > 7 else 2
Sbox_bit = int(sys.argv[8]) if len(sys.argv) > 8 else 8
NonlinearType = str(sys.argv[9]) if len(sys.argv) > 9 else "modulo"



t = test(
    Blocksize=blocksize,
    Round=rounds,
    Branch_number=Branch_number,
    Sbox_bit=Sbox_bit,
    Sbox_content=[],
    Matrix=None,
    NonlinearType=NonlinearType,
)

t.DIFgathered(blocksize, rounds, con, input_hex, output_hex)
print("生成文件: backend/static/cvc/DIFgathered.cvc")
