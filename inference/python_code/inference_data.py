import sys
import os
import json
import glob
import csv
import joblib
import argparse
import pandas as pd

sys.path.append(os.getcwd())
from utils.preprocess import preprocess_data

def get_parser():
    parser = argparse.ArgumentParser("HanShin Medikind")
    parser.add_argument("--joblib_dir", type=str, required=True, help="가중치 파일 경로") 
    parser.add_argument("--data_dir", type=str, help="데이터셋 위치(임시)")
    parser.add_argument("--cfg", type=str, default="data/cfg.json", help="config 위치")
    
    return parser

def main(args):
    mode = "inference"

    if not os.path.exists(args.data_dir):
        print(f"[ERROR] {args.data_dir}이 존재하지 않습니다.")
        return
    if not os.path.exists(args.cfg):
        print(f"[ERROR] {args.cfg}이 존재하지 않습니다.")
        return

    with open(args.cfg, "rt", encoding="utf-8") as f:
        cfg = json.load(f)    

    if "csv" in args.data_dir:
        data = pd.read_csv(args.data_dir)
    else:
        data = pd.read_excel(args.data_dir)
    data = data[:10]


    output_dir = "./output/output.xlsx"
    if os.path.exists(output_dir):
        os.remove(output_dir)

    excel_writer = pd.ExcelWriter(output_dir, engine="xlsxwriter")
    
    for joblib_path in glob.glob(os.path.join(args.joblib_dir+"/*.joblib")):
        joblib_name = os.path.split(joblib_path)[-1]
        task = int(joblib_name[0])
        rf, scaler, normalizer = joblib.load(joblib_path)
        
        X, all_data = preprocess_data(data, task, cfg=cfg["preprocess"], mode=mode, scalers=(scaler, normalizer), get_all_data=True)

        output_df = pd.DataFrame(columns=cfg["output"]["cols"])
        for col in output_df.columns.tolist():
            output_df[col] = pd.DataFrame(all_data[col])
        output_df["predict"] = pd.DataFrame(data=rf.predict(X), index=output_df.index)
        output_df.to_excel(excel_writer ,encoding="euc-kr", sheet_name = joblib_name)

    excel_writer.save()
    
if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)