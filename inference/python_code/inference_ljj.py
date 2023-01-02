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
    parser.add_argument("--joblib_dir", type=str, default='/home/ljj/workspace/hanshin_inference/train', help="joblib 파일 경로") 
    parser.add_argument("--cfg", type=str, default="/home/ljj/workspace/hanshin_inference/cfg.json", help="config 위치")
    parser.add_argument("--data", type=str, default="/home/ljj/workspace/hanshin_inference/inference_data/service_data_1person.csv", help="config 위치")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    with open(args.cfg, "rt", encoding="utf-8") as f:
        cfg = json.load(f)

    data = pd.read_csv(args.data)

    models = []
    
    for joblib_path in glob.glob(os.path.join(args.joblib_dir, "*.joblib")):
        rf, scaler, normalizer = joblib.load(joblib_path) # rf : model, scaler : 
        joblib_name = os.path.split(joblib_path)[-1] # model name
        task = int(joblib_name.split("_")[0])
        models.append([task, rf, scaler, normalizer])
    # ======================= QT EXEC ================================== # 


    # ======================= Button ================================== # 
    for task, model, scaler, norm in models:
        X, all_data = preprocess_data(data, task, cfg=cfg["preprocess"], mode="inference", scalers=(scaler, norm), get_all_data=True)
        person_private = pd.DataFrame(columns=cfg["output"]["private"])
        for key, value in cfg["output"]["cols"].items():
            disease = pd.DataFrame(columns=value)
            output_df = pd.concat([person_private, disease], axis=1)
            for col in output_df.columns.tolist():
                output_df[col] = pd.DataFrame(all_data[col])
            print("dsa")
            predict = model.predict(X)
            output_df["predict"] = pd.DataFrame(data=predict, index=output_df.index) # Result 
        # output_df.to_excel(excel_writer ,encoding="euc-kr", sheet_name = joblib_name)

    # excel_writer.save()