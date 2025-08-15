import json
import pandas as pd
from pathlib import Path

# ==== 路径配置 ====
input_path = Path("../Data_samples/results/4000tokens_150requests_15num/deepseekr1_4000_1500_individual_responses.json")
tpot_json_path = Path("../Data_output/deepseekr1_tpot_list.json")
tpot_excel_path = Path("../Data_output/deepseekr1_tpot_list.xlsx")
tpot_summary_excel_path = Path("../Data_output/deepseekr1_tpot_summary.xlsx")
tpot_summary_json_path = Path("../Data_output/deepseekr1_tpot_summary.json")


# ==== 函数 1：计算 TPOT 列表（排序） ====
def calculate_tpot_sorted(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    tpot_entries = []
    for idx, entry in enumerate(data):
        try:
            output_tokens = entry.get("number_output_tokens", 0)
            e2e_latency = entry.get("end_to_end_latency_s", None)
            ttft = entry.get("ttft_s", None)

            if output_tokens and e2e_latency is not None and ttft is not None:
                decode_time = e2e_latency - ttft
                if decode_time > 0:
                    tpot = decode_time / output_tokens
                    tpot_entries.append({
                        "request_index": idx,
                        "tpot": tpot
                    })
        except Exception:
            continue

    # 按 TPOT 升序排序
    sorted_entries = sorted(tpot_entries, key=lambda x: x["tpot"])

    # 保存结果
    with open(tpot_json_path, "w") as f:
        json.dump(sorted_entries, f, indent=2)

    pd.DataFrame(sorted_entries).to_excel(tpot_excel_path, index=False)

    return [entry["tpot"] for entry in sorted_entries]


# ==== 函数 2：根据 TPOT 列表计算统计 ====
def calculate_tpot_summary(tpot_list):
    df = pd.DataFrame(tpot_list, columns=["TPOT"])
    percentiles = df.quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

    summary = {
        "mean": df.mean()["TPOT"],
        "std": df.std()["TPOT"],
        "min": df.min()["TPOT"],
        "max": df.max()["TPOT"],
        "p25": percentiles.loc[0.25, "TPOT"],
        "p50": percentiles.loc[0.5, "TPOT"],
        "p75": percentiles.loc[0.75, "TPOT"],
        "p90": percentiles.loc[0.9, "TPOT"],
        "p95": percentiles.loc[0.95, "TPOT"],
        "p99": percentiles.loc[0.99, "TPOT"]
    }

    # 保存结果
    with open(tpot_summary_json_path, "w") as f:
        json.dump(summary, f, indent=2)

    pd.DataFrame([summary]).to_excel(tpot_summary_excel_path, index=False)

    return summary


# ==== 主流程 ====
tpot_sorted = calculate_tpot_sorted(input_path)
calculate_tpot_summary(tpot_sorted)
