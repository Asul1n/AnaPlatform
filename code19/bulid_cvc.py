import json
import subprocess
import os
from RoundFunction import RoundGraphParser
from DIF import Difference


def build_cvc(json_path, output_path):

    with open(json_path, "r") as f:
        data = json.load(f)

    params = data["basicParams"]

    block_size = params["blockSize"]
    branch_num = params["branchNum"]
    round_num = params["roundNum"]

    cg = Difference(
        Blocksize=block_size,
        Round=round_num,
        Branch_number=branch_num,
        Sbox_bit=0,
        Sbox_content=[],
        Matrix=None,
        NonlinearType="ARX"
    )

    parser = RoundGraphParser(data, cg)

    all_constraints = []
    all_vars = set()

    for r in range(1, round_num + 1):
        cons, vars_r = parser.gen_constraints(r)
        all_constraints.extend(cons)
        all_vars.update(vars_r)

    parser = RoundGraphParser(data, cg)

    all_constraints = []
    all_vars = set()

    for r in range(1, round_num + 1):
        cons, vars_r = parser.gen_constraints(r)
        all_constraints.extend(cons)
        all_vars.update(vars_r)

    # ===== Write CVC =====

    with open(output_path, "w") as f:

        f.write("%% ===== Auto-generated CVC for LEA =====\n\n")

        # Variables
        f.write("%% ===== Variables =====\n")
        for v in sorted(all_vars):
            f.write(v + ";\n")
        f.write("\n")

        # Constraints
        f.write("%% ===== Constraints =====\n")
        for c in all_constraints:
            if not c.endswith(";"):
                f.write(c + ";\n")
            else:
                f.write(c + "\n")
        f.write("\n")

        f.write("QUERY(FALSE);\n")
        f.write("COUNTEREXAMPLE;\n")

    print(f"[OK] Generated: {output_path}")


def run_stp(cvc_path, stp_path="stp"):

    result = subprocess.run(
        [stp_path, cvc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("======= STP OUTPUT =======")
    print(result.stdout)

    return result.stdout


if __name__ == "__main__":
    JSON_PATH = "./round.json"
    OUTPUT_CVC = "./dif.cvc"

    R = 8  # 从你的 basicParams.roundNum 得到

    build_cvc(JSON_PATH,  OUTPUT_CVC)
    run_stp(OUTPUT_CVC, stp_path="stp")
