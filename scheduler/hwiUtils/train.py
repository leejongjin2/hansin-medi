import sys
import random
import json
import joblib
import os
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix

from scheduler.hwiUtils.info import info_start, info_end
from hwiUtils.preprocess import preprocess_data

def train_HanshinModel():
    info_start('train train_HanshinModel')
    
    """_summary_
    한신 저장경로 : ???
    모델 이름 그대로 Train 및 저장
    """
    
    info_end('train train_HanshinModel')

def train_InfinityModel():
    info_start('train train_InfinityModel')
    
    """_summary_
    인피니티케어 저장경로 : ???
    모델 이름 그대로 Train 및 저장
    """
    
    info_end('train train_InfinityModel')
    
###########################################################################################



def get_parser():
    parser = argparse.ArgumentParser("HanShin Medikind")
    parser.add_argument("--data_dir", type=str, help="데이터셋 위치(임시)", default='/home/autocare/바탕화면/new_train_percent_hanshin/data/new_train_dataset_2022.xlsx') 
    parser.add_argument("--task", nargs='+', type=int, default=[i for i in range(1, 15)], help="훈련할 질환부위")
    parser.add_argument("--n_estimators", type=int, default=-1, help="n_estimator 값")
    parser.add_argument("--random_state", type=int, default=-1, help="random_state 값")
    parser.add_argument("--output_dir", type=str, default="./output/", help="저장 위치")
    parser.add_argument("--cfg", type=str, default="data/cfg.json", help="config 위치")
    return parser

def main(args):
    int2task = {1:"간암", 2:"위암", 3:"폐암", 4:"대장암", 5:"갑상선암", 6:"유방암",
            7:"뇌졸중", 8:"심근경색", 9:"당뇨병", 10:"폐결핵", 11:"고혈압", 12:"고지혈증",
            13:"지방간", 14:"단백뇨"}

    if not os.path.exists(args.data_dir):
        print(f"[ERROR] {args.data_dir}이 존재하지 않습니다.")
        return
    if not os.path.exists(args.cfg):
        print(f"[ERROR] {args.cfg}이 존재하지 않습니다.")
        return

    if "csv" in args.data_dir:
        data = pd.read_csv(args.data_dir)
    else:
        data = pd.read_excel(args.data_dir)

    if args.random_state == -1:
        # args.random_state = random.randint(1,8888) # 랜덤 지정
        args.random_state = 1234
        print(f"random_state: {args.random_state}")
    if args.n_estimators == -1:
        # args.n_estimators = random.randint(1,8888) # 랜덤 지정
        args.n_estimators = 5
        print(f"n_estimators: {args.n_estimators}")

    with open(args.cfg, "rt", encoding="utf-8") as f:
        cfg = json.load(f)
        cfg = cfg["preprocess"]

    for task in args.task:
        print("\n---------------------------------------------")
        print(f"{int2task[task]} 학습을 위한 데이터 전처리를 시작합니다.")
        (X_train, X_test, y_train, y_test), scaler, noramlizer = preprocess_data(data, task, cfg=cfg)
        print(f"\n{int2task[task]}에 대해 학습을 시작합니다.")
        rf_run = RandomForestRegressor(n_estimators=args.n_estimators, random_state=args.random_state)
        rf_run.fit(X_train, y_train)

        print(y_test.value_counts())
        pred = rf_run.predict(X_test)
        print('모델 훈련 세트 정확도 : {:.3f}'.format(rf_run.score(X_train, y_train)))
        print('모델 테스트 세트 정확도 : {:.3f}'.format(rf_run.score(X_test, y_test)))
        
        os.makedirs(os.path.join(args.output_dir, "train"), exist_ok=True)
        file_name = f"{task}_{int2task[task]}_발병확률_예측모델_{rf_run.score(X_test, y_test):.3f}.joblib"
        
        weights = (rf_run, scaler, noramlizer)
        #joblib.dump(weights, os.path.join(args.output_dir, "train", file_name))
        print(f"{int2task[task]}에 대해 학습이 완료되었습니다.")
        print("---------------------------------------------")

if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)