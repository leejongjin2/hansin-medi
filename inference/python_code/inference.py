import sys
import os
import glob
import json
import joblib
import argparse
import pandas as pd

sys.path.insert(0, os.getcwd())
from preprocess import preprocess_data
import csv


def get_parser():
    parser = argparse.ArgumentParser("HanShin Medikind")
    parser.add_argument("--joblib_dir", type=str, help="joblib 파일 경로") 
    parser.add_argument("--many", type=int, default=10, help="db에서 데이터를 가져올 사람 수")
    parser.add_argument("--cfg", type=str, default="data/cfg.json", help="config 위치")
    parser.add_argument("--data", type=str, default="data/cfg.csv", help="config 위치")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    with open(args.cfg, "rt", encoding="utf-8") as f:
        cfg = json.load(f)

    # service_data_1person.xlsx
    data = 'service_data_1person.xlsx'
# get_data(args.many, cfg=cfg["db"])

    output_dir = "./output/liver_per.xlsx"
    # output_dir = "./output/output.xlsx"
    if os.path.exists(output_dir):
        os.remove(output_dir)

    # excel_writer = pd.ExcelWriter(output_dir, engine="xlsxwriter")
    a = []
    
    for joblib_path in glob.glob(os.path.join(args.joblib_dir, "*.joblib")):
        rf, scaler, normalizer = joblib.load(joblib_path) # rf : model, scaler : 
        joblib_name = os.path.split(joblib_path)[-1] # model name
        task = int(joblib_name.split("_")[0])
        a.append(task, scaler, normalizer)
    # ======================= QT EXEC ================================== # 


    # ======================= Button ================================== # 
    for t, s, n in a:
        X, all_data = preprocess_data(data, t, cfg=cfg["preprocess"], mode="inference", scalers=(s, n), get_all_data=True)
        person_private = pd.DataFrame(columns=cfg["output"]["private"])
        disease = pd.DataFrame(columns=cfg["output"]["cols"])
        output_df = pd.concat([person_private, disease], axis=1)
        for col in output_df.columns.tolist():
            output_df[col] = pd.DataFrame(all_data[col])
        output_df["predict"] = pd.DataFrame(data=rf.predict(X), index=output_df.index) # Result 
        # output_df.to_excel(excel_writer ,encoding="euc-kr", sheet_name = joblib_name)

    # excel_writer.save()