import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, Normalizer
from sklearn.model_selection import train_test_split
import tqdm


def overwrite_data(src, dst):
    indexes = list(src.index)
    dst = dst.loc[indexes, :]
    for col in src.columns.tolist():
        dst[col] = src[col]

    return dst


def preprocess_data(all_data, task, cfg, mode="train", scalers=None, get_all_data=False):
    if mode != "train":
        (scaler, noramlizer) = scalers
    if "per1_age" not in all_data.columns.tolist() or "mj70" not in all_data.columns.tolist():
       all_data = add_col_data(all_data)
       
    data = clean_up_data(all_data, task, cfg=cfg["use_cols"])
    X, y = get_dataset(data, task, cfg=cfg["target"])

    if get_all_data:
        all_data = overwrite_data(data, all_data)
    
    if mode == "train":
        data = train_test_split(X, y, train_size=0.7, test_size=0.3)
        data, scaler = scale_robust(data, mode)
        data, noramlizer = noramlize_data(data, mode)

        if get_all_data:
            return (data, scaler, noramlizer), all_data
        return data, scaler, noramlizer

    else: 
        data = X
        data, _ = scale_robust(data, mode, scaler)
        data, _ = noramlize_data(data, mode, noramlizer)

        if get_all_data:
            return data, all_data
        return data

def convert_txt2int(data):
    print("obesity(비만도) 값 치환")
    for i in tqdm.tqdm(range(0, len(data))):
        if data['obesity'].iloc[i]=='저체중':
            data['obesity'].iloc[i]=1
        elif data['obesity'].iloc[i]=='정상체중':
            data['obesity'].iloc[i]=2
        elif data['obesity'].iloc[i]=='비만1단계':
            data['obesity'].iloc[i]=3
        elif data['obesity'].iloc[i]=='비만2단계':
            data['obesity'].iloc[i]=4
        elif data['obesity'].iloc[i]=='비만3단계':
            data['obesity'].iloc[i]=5
            
    print("urine_protein(요단백) 값 치환")
    for i in tqdm.tqdm(range(0, len(data))):
        if data['urine_protein'].iloc[i]=='음성':
            data['urine_protein'].iloc[i]=0
        elif data['urine_protein'].iloc[i]=='약양성':
            data['urine_protein'].iloc[i]=1
        elif data['urine_protein'].iloc[i]=='1':
            data['urine_protein'].iloc[i]=2
        elif data['urine_protein'].iloc[i]=='2':
            data['urine_protein'].iloc[i]=3
        elif data['urine_protein'].iloc[i]=='3':
            data['urine_protein'].iloc[i]=4
        elif data['urine_protein'].iloc[i]=='4':
            data['urine_protein'].iloc[i]=5
            
    if "liver_b_antigen" in data.columns.tolist():
        print("B형간염표면항원 값 치환")
        for i in tqdm.tqdm(range(0, len(data))):
            if data['liver_b_antigen'].iloc[i]=='음성':
                data['liver_b_antigen'].iloc[i]=0
            elif data['liver_b_antigen'].iloc[i]=='약양성':
                data['liver_b_antigen'].iloc[i]=1
            elif data['liver_b_antigen'].iloc[i]=='양성':
                data['liver_b_antigen'].iloc[i]=1
            else: # 수치+문자 혼합 데이터
                data['liver_b_antigen'].iloc[i]=0

    return data

def noramlize_data(data, mode, normal_scaler=None):
    if mode == "train":
        normal_scaler = Normalizer()
        X_train, X_test, y_train, y_test = data
        normal_scaler.fit(X_train)
        X_train = normal_scaler.transform(X_train)
        X_test = normal_scaler.transform(X_test)
        return (X_train, X_test, y_train, y_test), normal_scaler
    else:
        X = normal_scaler.transform(data)
        return X, None

def scale_robust(data, mode, scaler=None):
    if mode == "train":
        scaler = RobustScaler()
        X_train, X_test, y_train, y_test = data
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        return (X_train, X_test, y_train, y_test), scaler
    else:
        X = scaler.transform(data)
        return X, None

def add_col_data(data):
    print("만 나이 컬럼 데이터 추가")
    data['per1_age'] = 0
    data['per1_date'] = data['per1_date'].astype('datetime64')
    data['per1_birth_date'] = data['per1_birth_date'].astype('datetime64')

    for i in tqdm.tqdm(range(0,len(data))):
        today = data['per1_date'].iloc[i].date()
        year = data['per1_date'].iloc[i].year- data['per1_birth_date'].iloc[i].year
        if data['per1_date'].iloc[i].month < (data['per1_birth_date'].iloc[i]).month or (data['per1_date'].iloc[i].month==(data['per1_birth_date'].iloc[i]).month and data['per1_date'].iloc[i].day<(data['per1_birth_date'].iloc[i]).day):
            year -=1
        data['per1_age'].iloc[i]=year

    ## 연령대 컬럼 생성 :14개 연령대
    print("14개 연령대 컬럼 생성 : 10대, 20대, 30대 ~ 80대(중반/후반)")
    data['age_group'] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_age'].iloc[i] < 20:
            data['age_group'].iloc[i]=1
        elif data['per1_age'].iloc[i] >= 20 and data['per1_age'].iloc[i] < 30:
            data['age_group'].iloc[i]=2
        elif data['per1_age'].iloc[i] >= 30 and data['per1_age'].iloc[i] < 35:
            data['age_group'].iloc[i]=3
        elif data['per1_age'].iloc[i] >= 35 and data['per1_age'].iloc[i] < 40:
            data['age_group'].iloc[i]=4
        elif data['per1_age'].iloc[i] >= 40 and data['per1_age'].iloc[i] < 45:
            data['age_group'].iloc[i]=5
        elif data['per1_age'].iloc[i] >= 45 and data['per1_age'].iloc[i] < 50:
            data['age_group'].iloc[i]=6
        elif data['per1_age'].iloc[i] >= 50 and data['per1_age'].iloc[i] < 55:
            data['age_group'].iloc[i]=7
        elif data['per1_age'].iloc[i] >= 55 and data['per1_age'].iloc[i] < 60:
            data['age_group'].iloc[i]=8
        elif data['per1_age'].iloc[i] >= 60 and data['per1_age'].iloc[i] < 65:
            data['age_group'].iloc[i]=9
        elif data['per1_age'].iloc[i] >= 65 and data['per1_age'].iloc[i] < 70:
            data['age_group'].iloc[i]=10
        elif data['per1_age'].iloc[i] >= 70 and data['per1_age'].iloc[i] < 75:
            data['age_group'].iloc[i]=11
        elif data['per1_age'].iloc[i] >= 75 and data['per1_age'].iloc[i] < 80:
            data['age_group'].iloc[i]=12
        elif data['per1_age'].iloc[i] >= 80 and data['per1_age'].iloc[i] < 85:
            data['age_group'].iloc[i]=13
        else:
            data['age_group'].iloc[i]=14

    ## 성별 전처리 (1명 0 -> 2 전환, 남성 :1/3/5 -> 1, 여성:2/4/6 ->2)
    print('성별 전처리 :1) 1명 0 -> 2 전환, 2) 남성 :1/3/5 -> 1, 여성:2/4/6 ->2 변환')
    # 1) 성별 : 0 (20년 1명) -> 2로 전환
    for i in tqdm.tqdm(range(0, len(data))):
        if data['per1_gender'].iloc[i]==0:
            data['per1_gender'].iloc[i]=2
    # 2) 성별 통일 (남성 :1/3/5 -> 1, 여성:2/4/6 ->2)
    for i in tqdm.tqdm(range(0, len(data))):
        if data['per1_gender'].iloc[i]==3 or data['per1_gender'].iloc[i]==5:
            data['per1_gender'].iloc[i]=1
        elif data['per1_gender'].iloc[i]==4 or data['per1_gender'].iloc[i]==6:
            data['per1_gender'].iloc[i]=2
            
    ## 1년 기준 음주량 컬럼 생성
    print("1년기준 음주량 컬럼 추가 : mj70(1년 중 음주 일수)")
    # mj74 : 음주여부 null -> 0으로 대체 (0: 음주 안함)
    data['mj74'] = data['mj74'].replace(np.nan, 0)
    data['mj74'] = data['mj74'].astype('int')

    ## mj71(일주일_음주량) 전처리------ 
    # mj71(일주일_음주량) = ' ' -> 잠시 -2로 바꾸기 (컬럼 정수형 변환 목적)
    for i in range(0,len(data)):
        if data['mj71'].iloc[i]==' ':
            data['mj71'].iloc[i] = -2
        else:
            data['mj71'].iloc[i] = data['mj71'].iloc[i]

    data = data.dropna(subset=['mj71'])
    data['mj71'] = data['mj71'].astype('int')

    # mj71(일주일) * 52 → 1년 단위로 환산
    for i in range(0,len(data)):
        if data['mj71'].iloc[i]==-2:
            data['mj71'].iloc[i] = -2
        else:
            data['mj71'].iloc[i] = data['mj71'].iloc[i]*52

    ## mj72(한달_음주량) 전처리------ 
    # mj72(한달_음주량) = ' ' -> 잠시 -2로 바꾸기 (컬럼 정수형 변환 목적)
    for i in range(0,len(data)):
        if data['mj72'].iloc[i]=='  ':
            data['mj72'].iloc[i] = -2
        else:
            data['mj72'].iloc[i] = data['mj72'].iloc[i]

    data = data.dropna(subset=['mj72'])
    data['mj72'] = data['mj72'].replace(np.nan, 0)
    data['mj72'] = data['mj72'].astype('int')

    # mj72(한달) * 12 → 1년 단위로 환산
    for i in range(0,len(data)):
        if data['mj72'].iloc[i]==-2:
            data['mj72'].iloc[i] = -2
        else:
            data['mj72'].iloc[i] = data['mj72'].iloc[i]*12
            
    ## mj73(1년_음주량) 전처리------ 
    # mj73(1년_음주량) = '   ' -> 잠시 -2로 바꾸기 (컬럼 정수형 변환 목적)
    # 나머지는 그대로 사용
    # 정수형 변환
    data['mj73'] = data['mj73'].str.strip()
    data['mj73'] = data['mj73'].replace('', 0)
    data['mj73'] = data['mj73'].astype('int')

    ## 음주_ 1년 음주 횟수 컬럼 생성 : mj70------
    # mj70(1년 음주 횟수) 0으로 생성 후 변환
    data['mj70'] = 0
    for i in range(0,len(data)):
        if data['mj71'].iloc[i]==-2:
            if data['mj72'].iloc[i]==-2:
                data['mj70'].iloc[i] = data['mj73'].iloc[i]
            else :
                data['mj70'].iloc[i] = data['mj72'].iloc[i]
        else:
            data['mj70'].iloc[i] = data['mj71'].iloc[i]

    ## 1) ~ 30) 전체 피벗 테이블 생성
    # 피벗 미존재 : [1] obesity(비만도), [2] urine_protein(요단백), [3] liver_b_antigen(B형간염항원), [4] stomach_helico_bacter(헬리코박터)
    grouped = data.groupby(['age_group','per1_gender'])
    gdf = grouped.mean()
    gdf = pd.DataFrame(gdf)
    print(gdf.columns)

    ## 혈액검사 26개 컬럼 피벗 테이블(그룹함수) 기반 결측치 채우기
    # 4개 컬럼 예외 -> 후처리 진행 ([1] obesity(비만도), [2] urine_protein(요단백), [3] liver_b_antigen(B형간염항원), [4] stomach_helico_bacter(헬리코박터))
    print('혈액검사 26개 컬럼 피벗 테이블(그룹함수) 기반 결측치 채우기')
    columns_26 = ['height', 'weight', 'wai_cir', 'bmi', 'blood_press_high',
        'blood_press_low', 'total_col', 'hdl_col', 'ldl_col_cal', 'tri_gly',
        'r_gtp', 'liver_bilirubin', 'liver_protein', 'liver_albumin',
        'liver_globulin', 'liver_ast', 'liver_alt', 'liver_alp', 'glucose',
        'creatinine', 'lung_cyfra21_1', 'lar_int_cea',
        'lar_int_ca19', 'thy_tsh', 'thy_ft4', 'breast_ca15_3']

    ## 26개 중 3개 컬럼[21.Cyfra21-1, 22.CEA, 24.TSH : 13,14 여 / 14 남 데이터 미존재 -> 12/13 남녀 데이터로 결측치 채우기]
    ## 26개 중 1개 컬럼[26.CA15-3] : 대부분 남자 미존재 및 불필요 컬럼
    print('26개 중 4개 컬럼 연령대 미존재 결측치 추가 처리')
    print('[1] Cyfra21-1 13 여, 14 남녀 미존재 -> 13,14 여 : 12여(2.90), 14 남 : 13남(3.63)로 결측치 채우기')
    for i in tqdm.tqdm(range(0,len(data))):
        if data["per1_gender"].iloc[i]==1:
            data["lung_cyfra21_1"].fillna(3.63, inplace=True)
        elif data["per1_gender"].iloc[i]==2:
            data["lung_cyfra21_1"].fillna(2.90, inplace=True)
            
    print('[2] CEA(lar_int_cea) 14 여 미존재 -> 14 여 : 13여(3.00)로 결측치 채우기')
    data["lar_int_cea"].fillna(3.00, inplace=True)

    print('[3] TSH(thy_tsh) 14 여 미존재 -> 14 여 : 13여(1.16)로 결측치 채우기')
    data["thy_tsh"].fillna(1.16, inplace=True)

    print('[4] CA15-3(breast_ca15_3) 1~4 남, 9~14 남 미존재 -> 1~4 남 : 5남(8.22), 9~14 남 : 8남(9.90)로 결측치 채우기')
    for i in tqdm.tqdm(range(0,len(data))):
        # 1~4 남
        if data["age_group"].iloc[i]>=1 and data["age_group"].iloc[i]<=4:
            data["breast_ca15_3"].fillna(8.22, inplace=True)
        # 9~14 남   
        elif data["age_group"].iloc[i]>=9 and data["age_group"].iloc[i]<=14:
            data["breast_ca15_3"].fillna(9.90, inplace=True)
            
    print('---------------------26개 중 4개 컬럼 연령대 미존재 결측치 추가 처리 완료---------------------')

    ## 4개 혈액검사 컬럼 예외 -> 후처리 진행 
    ## [1] obesity(비만도), [2] urine_protein(요단백), [3] liver_b_antigen(B형간염항원), [4] stomach_helico_bacter(헬리코박터)
    print("4개 예외 컬럼 결측치 채우기 : obesity, urine_protein, liver_b_antigen, stomach_helico_bacter")
    # [1] obesity(비만도)
    print("[1] obesity(비만도) 결측치 채우기 : BMI 기준")
    data["bmi"] = data["bmi"].astype('float64')
    for i in tqdm.tqdm(range(0,len(data))):
        if data["bmi"].iloc[i] < 18.5:
            data["obesity"].iloc[i] = 1
        elif data["bmi"].iloc[i] >= 18.5 and data["bmi"].iloc[i] < 25.0:
            data["obesity"].iloc[i] = 2
        elif data["bmi"].iloc[i] >= 25.0 and data["bmi"].iloc[i] < 30.0:
            data["obesity"].iloc[i] = 3
        elif data["bmi"].iloc[i] >= 30.0 and data["bmi"].iloc[i] < 35.0:
            data["obesity"].iloc[i] = 4
        elif data["bmi"].iloc[i] >= 35.0:
            data["obesity"].iloc[i] = 5
    print(data["obesity"].value_counts())

    # [2] urine_protein(요단백)
    print("[2] urine_protein(요단백) 결측치 채우기 : 0 (음성)")
    data["urine_protein"].fillna(0, inplace=True)

    # [3] liver_b_antigen(B형간염항원)
    print("[3] liver_b_antigen(B형간염항원) 결측치 채우기 : 0 (음성)")
    data["liver_b_antigen"].fillna(0, inplace=True)

    # [4] stomach_helico_bacter(헬리코박터)
    print("[4] stomach_helico_bacter(헬리코박터) 결측치 채우기 : 0 (음성)")
    data["stomach_helico_bacter"].fillna(0, inplace=True)
    print("----------4개 예외 컬럼 결측치 채우기 : obesity, urine_protein, liver_b_antigen, stomach_helico_bacter 완료----------")

    ## 혈액검사 26개 컬럼 피벗 테이블(그룹함수) 기반 결측치 채우기
    # 1) 신장
    data["height"].fillna(data.groupby(['age_group','per1_gender'])["height"].transform("mean"), inplace=True)
    print("1) 신장(height) 채우기 완료")

    # 2) 체중
    data["weight"].fillna(data.groupby(['age_group','per1_gender'])["weight"].transform("mean"), inplace=True)
    print("2) 체중(weight) 채우기 완료")

    # 3) 허리둘레
    data["wai_cir"].fillna(data.groupby(['age_group','per1_gender'])["wai_cir"].transform("mean"), inplace=True)
    print("3) 허리둘레(wai_cir) 채우기 완료")

    # 4) BMI
    data["bmi"].fillna(data.groupby(['age_group','per1_gender'])["bmi"].transform("mean"), inplace=True)
    print("4) BMI(bmi) 채우기 완료")
    #print("4) BMI - 소수점 첫째자리까지로 반올림")
    #for i in tqdm.tqdm(range(0,len(data))):
    #    data["bmi"].iloc[i] = round(data["bmi"].iloc[i], 1)

    # 5) 수축기 혈압
    data["blood_press_high"].fillna(data.groupby(['age_group','per1_gender'])["blood_press_high"].transform("mean"), inplace=True)
    print("5) 수축기 혈압(blood_press_high) 채우기 완료")

    # 6) 이완기 혈압
    data["blood_press_low"].fillna(data.groupby(['age_group','per1_gender'])["blood_press_low"].transform("mean"), inplace=True)
    print("6) 이완기 혈압(blood_press_low) 채우기 완료")

    # 7) 총 콜레스테롤
    data["total_col"].fillna(data.groupby(['age_group','per1_gender'])["total_col"].transform("mean"), inplace=True)
    print("7) 총 콜레스테롤(total_col) 채우기 완료")

    # 8) HDL 콜레스테롤
    data["hdl_col"].fillna(data.groupby(['age_group','per1_gender'])["hdl_col"].transform("mean"), inplace=True)
    print("8) HDL 콜레스테롤(hdl_col) 채우기 완료")

    # 9) LDL 콜레스테롤
    data["ldl_col_cal"].fillna(data.groupby(['age_group','per1_gender'])["ldl_col_cal"].transform("mean"), inplace=True)
    print("9) LDL 콜레스테롤(ldl_col) 채우기 완료")

    # 10) 중성지방
    data["tri_gly"].fillna(data.groupby(['age_group','per1_gender'])["tri_gly"].transform("mean"), inplace=True)
    print("10) 중성지방(tri_gly) 채우기 완료")

    # 11) r-GTP
    data["r_gtp"].fillna(data.groupby(['age_group','per1_gender'])["r_gtp"].transform("mean"), inplace=True)
    print("11) r-GTP 채우기 완료")

    # 12) 총 빌리루빈
    data["liver_bilirubin"].fillna(data.groupby(['age_group','per1_gender'])["liver_bilirubin"].transform("mean"), inplace=True)
    print("12) 총 빌리루빈(liver_bilirubin) 채우기 완료")

    # 13) 총 단백
    data["liver_protein"].fillna(data.groupby(['age_group','per1_gender'])["liver_protein"].transform("mean"), inplace=True)
    print("13) 총 단백(liver_protein) 채우기 완료")

    # 14) 알부민
    data["liver_albumin"].fillna(data.groupby(['age_group','per1_gender'])["liver_albumin"].transform("mean"), inplace=True)
    print("14) 알부민(liver_albumin) 채우기 완료")

    # 15) 글로불린
    data["liver_globulin"].fillna(data.groupby(['age_group','per1_gender'])["liver_globulin"].transform("mean"), inplace=True)
    print("15) 글로불린(liver_globulin) 채우기 완료")

    # 16) AST
    data["liver_ast"].fillna(data.groupby(['age_group','per1_gender'])["liver_ast"].transform("mean"), inplace=True)
    print("16) AST(liver_ast) 채우기 완료")

    # 17) ALT
    data["liver_alt"].fillna(data.groupby(['age_group','per1_gender'])["liver_alt"].transform("mean"), inplace=True)
    print("17) ALT(liver_alt) 채우기 완료")

    # 18) ALP
    data["liver_alp"].fillna(data.groupby(['age_group','per1_gender'])["liver_alp"].transform("mean"), inplace=True)
    print("18) ALP(liver_alp) 채우기 완료")

    # 19) 공복혈당
    data["glucose"].fillna(data.groupby(['age_group','per1_gender'])["glucose"].transform("mean"), inplace=True)
    print("19) 공복혈당(glucose) 채우기 완료")

    # 20) 혈청 크레아티닌
    data["creatinine"].fillna(data.groupby(['age_group','per1_gender'])["creatinine"].transform("mean"), inplace=True)
    print("20) 혈청 크레아티닌(creatinine) 채우기 완료")

    # 21) Cyfra21-1
    data["lung_cyfra21_1"].fillna(data.groupby(['age_group','per1_gender'])["lung_cyfra21_1"].transform("mean"), inplace=True)
    print("21) Cyfra21-1(lung_cyfra21_1) 채우기 완료")

    # 22) CEA
    data["lar_int_cea"].fillna(data.groupby(['age_group','per1_gender'])["lar_int_cea"].transform("mean"), inplace=True)
    print("22) CEA(lar_int_cea) 채우기 완료")

    # 23) CA19
    data["lar_int_ca19"].fillna(data.groupby(['age_group','per1_gender'])["lar_int_ca19"].transform("mean"), inplace=True)
    print("23) CA19(lar_int_ca19) 채우기 완료")

    # 24) TSH
    data["thy_tsh"].fillna(data.groupby(['age_group','per1_gender'])["thy_tsh"].transform("mean"), inplace=True)
    print("24) TSH(thy_tsh) 채우기 완료")

    # 25) FT4
    data["thy_ft4"].fillna(data.groupby(['age_group','per1_gender'])["thy_ft4"].transform("mean"), inplace=True)
    print("25) FT4(thy_ft4) 채우기 완료")

    # 26) CA15-3
    data["breast_ca15_3"].fillna(data.groupby(['age_group','per1_gender'])["breast_ca15_3"].transform("mean"), inplace=True)
    print("26) CA15-3(breast_ca15_3) 채우기 완료")
    print('---------------------혈액검사 26개 컬럼 피벗 테이블(그룹함수) 기반 결측치 채우기 완료---------------------')
    
   ## 확률 계산용 컬럼(20% 기준)
    # 1) AST
    print('1) AST 확률 계산(20% 기준)')
    data["liver_ast_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['liver_ast'].iloc[i] >=24 and data['liver_ast'].iloc[i]<32:
            data['liver_ast_per'].iloc[i]+=4
        elif data['liver_ast'].iloc[i]>=32 and data['liver_ast'].iloc[i]<40:
            data['liver_ast_per'].iloc[i]+=8
        elif data['liver_ast'].iloc[i]>=40 and data['liver_ast'].iloc[i]<48:
            data['liver_ast_per'].iloc[i]+=12 
        elif data['liver_ast'].iloc[i]>=48 and data['liver_ast'].iloc[i]<56:
            data['liver_ast_per'].iloc[i]+=16
        elif data['liver_ast'].iloc[i]<=4:
            data['liver_ast_per'].iloc[i]+=16 
        elif data['liver_ast'].iloc[i]>=56:
            data['liver_ast_per'].iloc[i]+=20
    
    # 2) ALT
    print('2) ALT 확률 계산(20% 기준)')
    data["liver_alt_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['liver_alt'].iloc[i] >=24 and data['liver_alt'].iloc[i]<32:
            data['liver_alt_per'].iloc[i]+=4
        elif data['liver_alt'].iloc[i]>=32 and data['liver_alt'].iloc[i]<40:
            data['liver_alt_per'].iloc[i]+=8
        elif data['liver_alt'].iloc[i]>=40 and data['liver_alt'].iloc[i]<48:
                data['liver_alt_per'].iloc[i]+=12 
        elif data['liver_alt'].iloc[i]>=48 and data['liver_alt'].iloc[i]<56:
                data['liver_alt_per'].iloc[i]+=16
        elif data['liver_alt'].iloc[i]<=4:
            data['liver_alt_per'].iloc[i]+=16 
        elif data['liver_alt'].iloc[i]>=56:
                data['liver_alt_per'].iloc[i]+=20
    
    # 3) ALP
    print('3) ALP 확률 계산(20% 기준)')
    data["liver_alp_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['liver_alp'].iloc[i] <=29:
            data['liver_alp_per'].iloc[i]+=20
        elif data['liver_alp'].iloc[i]>29 and data['liver_alp'].iloc[i]<=32:
            data['liver_alp_per'].iloc[i]+=16
        elif data['liver_alp'].iloc[i]>32 and data['liver_alp'].iloc[i]<=35:
            data['liver_alp_per'].iloc[i]+=12
        elif data['liver_alp'].iloc[i]>35 and data['liver_alp'].iloc[i]<=38:
            data['liver_alp_per'].iloc[i]+=8
        elif data['liver_alp'].iloc[i]>38 and data['liver_alp'].iloc[i]<=41:
            data['liver_alp_per'].iloc[i]+=4
        elif data['liver_alp'].iloc[i]>41 and data['liver_alp'].iloc[i]<96:
            data['liver_alp_per'].iloc[i]+=0
        elif data['liver_alp'].iloc[i]>=96 and data['liver_alp'].iloc[i]<108:
            data['liver_alp_per'].iloc[i]+=4
        elif data['liver_alp'].iloc[i]>=108 and data['liver_alp'].iloc[i]<120:
            data['liver_alp_per'].iloc[i]+=8
        elif data['liver_alp'].iloc[i]>=120 and data['liver_alp'].iloc[i]<132:
            data['liver_alp_per'].iloc[i]+=12
        elif data['liver_alp'].iloc[i]>=132 and data['liver_alp'].iloc[i]<144:
            data['liver_alp_per'].iloc[i]+=16
        elif data['liver_alp'].iloc[i]>=144:
            data['liver_alp_per'].iloc[i]+=20
    
    # 4) r-GTP
    print('4) r-GTP 확률 계산(20% 기준)')
    data["r_gtp_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if data['r_gtp'].iloc[i]<=6:
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>6 and data['r_gtp'].iloc[i]<=11:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>11 and data['r_gtp'].iloc[i]<51:
                data['r_gtp_per'].iloc[i]+=0
            elif data['r_gtp'].iloc[i]>=51 and data['r_gtp'].iloc[i]<57:
                data['r_gtp_per'].iloc[i]+=4
            elif data['r_gtp'].iloc[i]>=57 and data['r_gtp'].iloc[i]<63:
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>=63 and data['r_gtp'].iloc[i]<69:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>=69 and data['r_gtp'].iloc[i]<75:
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>=75:
                data['r_gtp_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if data['r_gtp'].iloc[i]<=4:
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>4 and data['r_gtp'].iloc[i]<=8:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>8 and data['r_gtp'].iloc[i]<29:
                data['r_gtp_per'].iloc[i]+=0
            elif data['r_gtp'].iloc[i]>=29 and data['r_gtp'].iloc[i]<32:
                data['r_gtp_per'].iloc[i]+=4
            elif data['r_gtp'].iloc[i]>=32 and data['r_gtp'].iloc[i]<35:
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>=35 and data['r_gtp'].iloc[i]<38:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>=38 and data['r_gtp'].iloc[i]<41:
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>=41:
                data['r_gtp_per'].iloc[i]+=20

    # 5) HDL
    print('5) HDL 확률 계산(20% 기준)')
    data["hdl_col_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['hdl_col'].iloc[i]<=48:
            data['hdl_col_per'].iloc[i]+=20
        elif data['hdl_col'].iloc[i]<=54 and data['hdl_col'].iloc[i]>48:
            data['hdl_col_per'].iloc[i]+=16
        elif data['hdl_col'].iloc[i]<=60 and data['hdl_col'].iloc[i]>54:
            data['hdl_col_per'].iloc[i]+=12 
        elif data['hdl_col'].iloc[i]<=66 and data['hdl_col'].iloc[i]>60:
            data['hdl_col_per'].iloc[i]+=8
        elif data['hdl_col'].iloc[i]<=72 and data['hdl_col'].iloc[i]>66:
            data['hdl_col_per'].iloc[i]+=4
    
    # 6) CEA
    print('6) CEA 확률 계산(20% 기준)')
    data["cea_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['lar_int_cea'].iloc[i]>=2.6 and data['lar_int_cea'].iloc[i]<3.3:
            data['cea_per'].iloc[i]+=4
        elif data['lar_int_cea'].iloc[i]>=3.3 and data['lar_int_cea'].iloc[i]<4.0:
            data['cea_per'].iloc[i]+=8
        elif data['lar_int_cea'].iloc[i]>=4.0 and data['lar_int_cea'].iloc[i]<4.7:
            data['cea_per'].iloc[i]+=12 
        elif data['lar_int_cea'].iloc[i]>=4.7 and data['lar_int_cea'].iloc[i]<5.4:
            data['cea_per'].iloc[i]+=16
        elif data['lar_int_cea'].iloc[i]>=5.4:
            data['cea_per'].iloc[i]+=20
    
    # 7) CA19 
    print('7) CA19 확률 계산(20% 기준)')
    data["ca19_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['lar_int_ca19'].iloc[i]>=13 and data['lar_int_ca19'].iloc[i]<20:
            data['ca19_per'].iloc[i]+=4
        elif data['lar_int_ca19'].iloc[i]>=20 and data['lar_int_ca19'].iloc[i]<27:
            data['ca19_per'].iloc[i]+=8
        elif data['lar_int_ca19'].iloc[i]>=27 and data['lar_int_ca19'].iloc[i]<34:
            data['ca19_per'].iloc[i]+=12 
        elif data['lar_int_ca19'].iloc[i]>=34 and data['lar_int_ca19'].iloc[i]<41:
            data['ca19_per'].iloc[i]+=16
        elif data['lar_int_ca19'].iloc[i]>=41:
            data['ca19_per'].iloc[i]+=20
    
    # 8) Cyfra21-1 
    print('8) Cyfra21-1 확률 계산(20% 기준)')
    data["cyfra21_1_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['lung_cyfra21_1'].iloc[i]>=1.2 and data['lung_cyfra21_1'].iloc[i]<1.9:
            data['cyfra21_1_per'].iloc[i]+=4
        elif data['lung_cyfra21_1'].iloc[i]>=1.9 and data['lung_cyfra21_1'].iloc[i]<2.6:
            data['cyfra21_1_per'].iloc[i]+=8
        elif data['lung_cyfra21_1'].iloc[i]>=2.6 and data['lung_cyfra21_1'].iloc[i]<3.3:
            data['cyfra21_1_per'].iloc[i]+=12 
        elif data['lung_cyfra21_1'].iloc[i]>=3.3 and data['lung_cyfra21_1'].iloc[i]<4.0:
            data['cyfra21_1_per'].iloc[i]+=16
        elif data['lung_cyfra21_1'].iloc[i]>=4.0:
            data['cyfra21_1_per'].iloc[i]+=20
    
    # 9) FreeT4
    print('9) FreeT4 확률 계산(20% 기준)')
    data["ft4_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['thy_ft4'].iloc[i]<0.59:
            data['ft4_per'].iloc[i]+=20
        elif data['thy_ft4'].iloc[i]>=0.59 and data['thy_ft4'].iloc[i]<0.76:
            data['ft4_per'].iloc[i]+=16
        elif data['thy_ft4'].iloc[i]>=0.76 and data['thy_ft4'].iloc[i]<0.93:
            data['ft4_per'].iloc[i]+=12 
        elif data['thy_ft4'].iloc[i]>=0.93 and data['thy_ft4'].iloc[i]<1.10:
            data['ft4_per'].iloc[i]+=8
        elif data['thy_ft4'].iloc[i]>=1.10 and data['thy_ft4'].iloc[i]<1.27:
            data['ft4_per'].iloc[i]+=4
        elif data['thy_ft4'].iloc[i]>=1.27 and data['thy_ft4'].iloc[i]<1.36:
            data['ft4_per'].iloc[i]+=0
        elif data['thy_ft4'].iloc[i]>=1.36 and data['thy_ft4'].iloc[i]<1.53:
            data['ft4_per'].iloc[i]+=4
        elif data['thy_ft4'].iloc[i]>=1.53 and data['thy_ft4'].iloc[i]<1.70:
            data['ft4_per'].iloc[i]+=8
        elif data['thy_ft4'].iloc[i]>=1.70 and data['thy_ft4'].iloc[i]<1.87:
            data['ft4_per'].iloc[i]+=12
        elif data['thy_ft4'].iloc[i]>=1.87 and data['thy_ft4'].iloc[i]<2.04:
            data['ft4_per'].iloc[i]+=16
        elif data['thy_ft4'].iloc[i]>=2.04:
            data['ft4_per'].iloc[i]+=20
    
    # 10) TSH 
    print('10) TSH 확률 계산(20% 기준)')
    data["tsh_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['thy_tsh'].iloc[i]>=1.30 and data['thy_tsh'].iloc[i]<2.20:
            data['tsh_per'].iloc[i]+=4
        elif data['thy_tsh'].iloc[i]>=2.20 and data['thy_tsh'].iloc[i]<3.10:
            data['tsh_per'].iloc[i]+=8
        elif data['thy_tsh'].iloc[i]>=3.10 and data['thy_tsh'].iloc[i]<4.00:
            data['tsh_per'].iloc[i]+=12 
        elif data['thy_tsh'].iloc[i]>=4.00 and data['thy_tsh'].iloc[i]<4.90:
            data['tsh_per'].iloc[i]+=16
        elif data['thy_tsh'].iloc[i]>=4.90:
            data['tsh_per'].iloc[i]+=20
     
     # 11) CA15-3
    print('11) CA15-3 확률 계산(20% 기준)')
    data["ca15_3_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['breast_ca15_3'].iloc[i]>=3 and data['breast_ca15_3'].iloc[i]<12:
            data['ca15_3_per'].iloc[i]+=4
        elif data['breast_ca15_3'].iloc[i]>=12 and data['breast_ca15_3'].iloc[i]<21:
            data['ca15_3_per'].iloc[i]+=8
        elif data['breast_ca15_3'].iloc[i]>=21 and data['breast_ca15_3'].iloc[i]<30:
            data['ca15_3_per'].iloc[i]+=12 
        elif data['breast_ca15_3'].iloc[i]>=30 and data['breast_ca15_3'].iloc[i]<39:
            data['ca15_3_per'].iloc[i]+=16
        elif data['breast_ca15_3'].iloc[i]>=39:
            data['ca15_3_per'].iloc[i]+=20
    
    # 12) BMI 
    print('12) BMI 확률 계산(20% 기준)')
    data["bmi_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['bmi'].iloc[i]>=18.5 and data['bmi'].iloc[i]<=18.9:
            data['bmi_per'].iloc[i]+=5
        elif data['bmi'].iloc[i]>=22.5 and data['bmi'].iloc[i]<=22.9:
            data['bmi_per'].iloc[i]+=5
        elif data['bmi'].iloc[i]>=23.0 and data['bmi'].iloc[i]<=23.9:
            data['bmi_per'].iloc[i]+=10
        elif data['bmi'].iloc[i]>=24.0 and data['bmi'].iloc[i]<=24.9:
            data['bmi_per'].iloc[i]+=15
        elif data['bmi'].iloc[i]>=25.0:
            data['bmi_per'].iloc[i]+=20
    
    # 13) 총 콜레스테롤
    print('13) 총 콜레스테롤 확률 계산(20% 기준)')
    data["total_col_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['total_col'].iloc[i]<90:
            data['total_col_per'].iloc[i]+=20
        elif data['total_col'].iloc[i]>=90 and data['total_col'].iloc[i]<110:
            data['total_col_per'].iloc[i]+=16
        elif data['total_col'].iloc[i]>=110 and data['total_col'].iloc[i]<130:
            data['total_col_per'].iloc[i]+=12 
        elif data['total_col'].iloc[i]>=130 and data['total_col'].iloc[i]<150:
            data['total_col_per'].iloc[i]+=8
        elif data['total_col'].iloc[i]>=150 and data['total_col'].iloc[i]<160:
            data['total_col_per'].iloc[i]+=4
        elif data['total_col'].iloc[i]>=160 and data['total_col'].iloc[i]<170:
            data['total_col_per'].iloc[i]+=0
        elif data['total_col'].iloc[i]>=170 and data['total_col'].iloc[i]<180:
            data['total_col_per'].iloc[i]+=4
        elif data['total_col'].iloc[i]>=180 and data['total_col'].iloc[i]<200:
            data['total_col_per'].iloc[i]+=8
        elif data['total_col'].iloc[i]>=200 and data['total_col'].iloc[i]<220:
            data['total_col_per'].iloc[i]+=12
        elif data['total_col'].iloc[i]>=220 and data['total_col'].iloc[i]<240:
            data['total_col_per'].iloc[i]+=16
        elif data['total_col'].iloc[i]>=240:
            data['total_col_per'].iloc[i]+=20
            
    # 14) LDL 
    print('14) LDL 확률 계산(20% 기준)')
    data["ldl_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['ldl_col_cal'].iloc[i]>=104 and data['ldl_col_cal'].iloc[i]<117:
            data['ldl_per'].iloc[i]+=4
        elif data['ldl_col_cal'].iloc[i]>=117 and data['ldl_col_cal'].iloc[i]<130:
            data['ldl_per'].iloc[i]+=8
        elif data['ldl_col_cal'].iloc[i]>=130 and data['ldl_col_cal'].iloc[i]<143:
            data['ldl_per'].iloc[i]+=12 
        elif data['ldl_col_cal'].iloc[i]>=143 and data['ldl_col_cal'].iloc[i]<156:
            data['ldl_per'].iloc[i]+=16
        elif data['ldl_col_cal'].iloc[i]>=156:
            data['ldl_per'].iloc[i]+=20
            
    # 15) 공복혈당
    print('15) 공복혈당 확률 계산(20% 기준)')
    data["glucose_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['glucose'].iloc[i]<60:
            data['glucose_per'].iloc[i]+=20
        elif data['glucose'].iloc[i]>=60 and data['glucose'].iloc[i]<65:
            data['glucose_per'].iloc[i]+=16    
        elif data['glucose'].iloc[i]>=65 and data['glucose'].iloc[i]<70:
            data['glucose_per'].iloc[i]+=12
        elif data['glucose'].iloc[i]>=70 and data['glucose'].iloc[i]<75:
            data['glucose_per'].iloc[i]+=8 
        elif data['glucose'].iloc[i]>=75 and data['glucose'].iloc[i]<80:
            data['glucose_per'].iloc[i]+=4
        elif data['glucose'].iloc[i]>=80 and data['glucose'].iloc[i]<90:
            data['glucose_per'].iloc[i]+=0
        elif data['glucose'].iloc[i]>=90 and data['glucose'].iloc[i]<95:
            data['glucose_per'].iloc[i]+=4
        elif data['glucose'].iloc[i]>=95 and data['glucose'].iloc[i]<100:
            data['glucose_per'].iloc[i]+=8
        elif data['glucose'].iloc[i]>=100 and data['glucose'].iloc[i]<105:
            data['glucose_per'].iloc[i]+=12
        elif data['glucose'].iloc[i]>=105 and data['glucose'].iloc[i]<110:
            data['glucose_per'].iloc[i]+=16
        elif data['glucose'].iloc[i]>=110:
            data['glucose_per'].iloc[i]+=20
            
    # 16) 중성지방 
    print('16) 중성지방 확률 계산(20% 기준)')
    data["tri_gly_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['tri_gly'].iloc[i]>=130 and data['tri_gly'].iloc[i]<140:
            data['tri_gly_per'].iloc[i]+=4
        elif data['tri_gly'].iloc[i]>=140 and data['tri_gly'].iloc[i]<150:
            data['tri_gly_per'].iloc[i]+=8
        elif data['tri_gly'].iloc[i]>=150 and data['tri_gly'].iloc[i]<160:
            data['tri_gly_per'].iloc[i]+=12 
        elif data['tri_gly'].iloc[i]>=160 and data['tri_gly'].iloc[i]<170:
            data['tri_gly_per'].iloc[i]+=16
        elif data['tri_gly'].iloc[i]>=170:
            data['tri_gly_per'].iloc[i]+=20
    
    # 17) 수축기 혈압
    print('17) 수축기 혈압 확률 계산(20% 기준)')
    data["blood_press_high_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['blood_press_high'].iloc[i]>=110 and data['blood_press_high'].iloc[i]<115:
            data['blood_press_high_per'].iloc[i]+=4
        elif data['blood_press_high'].iloc[i]>=115 and data['blood_press_high'].iloc[i]<120:
            data['blood_press_high_per'].iloc[i]+=8
        elif data['blood_press_high'].iloc[i]>=120 and data['blood_press_high'].iloc[i]<130:
            data['blood_press_high_per'].iloc[i]+=12 
        elif data['blood_press_high'].iloc[i]>=130 and data['blood_press_high'].iloc[i]<140:
            data['blood_press_high_per'].iloc[i]+=16
        elif data['blood_press_high'].iloc[i]>=140:
            data['blood_press_high_per'].iloc[i]+=20
    
    # 18) 이완기 혈압
    print('18) 이완기 혈압 확률 계산(20% 기준)')
    data["blood_press_low_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['blood_press_low'].iloc[i]>=70 and data['blood_press_low'].iloc[i]<75:
            data['blood_press_low_per'].iloc[i]+=4
        elif data['blood_press_low'].iloc[i]>=75 and data['blood_press_low'].iloc[i]<80:
            data['blood_press_low_per'].iloc[i]+=8
        elif data['blood_press_low'].iloc[i]>=80 and data['blood_press_low'].iloc[i]<90:
            data['blood_press_low_per'].iloc[i]+=12 
        elif data['blood_press_low'].iloc[i]>=90 and data['blood_press_low'].iloc[i]<100:
            data['blood_press_low_per'].iloc[i]+=16
        elif data['blood_press_low'].iloc[i]>=100:
            data['blood_press_low_per'].iloc[i]+=20
    
    # 19) 총 단백질
    print('19) 총 단백질 확률 계산(20% 기준)')
    data["liver_protein_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['liver_protein'].iloc[i]<5.5:
            data['liver_protein_per'].iloc[i]+=20
        elif data['liver_protein'].iloc[i]>=5.5 and data['liver_protein'].iloc[i]<6.0:
            data['liver_protein_per'].iloc[i]+=16
        elif data['liver_protein'].iloc[i]>=6.0 and data['liver_protein'].iloc[i]<6.5:
            data['liver_protein_per'].iloc[i]+=12 
        elif data['liver_protein'].iloc[i]>=6.5 and data['liver_protein'].iloc[i]<7.0:
            data['liver_protein_per'].iloc[i]+=8
        elif data['liver_protein'].iloc[i]>=7.0 and data['liver_protein'].iloc[i]<7.3:
            data['liver_protein_per'].iloc[i]+=4
        elif data['liver_protein'].iloc[i]>=7.3 and data['liver_protein'].iloc[i]<7.5:
            data['liver_protein_per'].iloc[i]+=0
        elif data['liver_protein'].iloc[i]>=7.5 and data['liver_protein'].iloc[i]<7.8:
            data['liver_protein_per'].iloc[i]+=4
        elif data['liver_protein'].iloc[i]>=7.8 and data['liver_protein'].iloc[i]<8.3:
            data['liver_protein_per'].iloc[i]+=8
        elif data['liver_protein'].iloc[i]>=8.3 and data['liver_protein'].iloc[i]<8.8:
            data['liver_protein_per'].iloc[i]+=12
        elif data['liver_protein'].iloc[i]>=8.8 and data['liver_protein'].iloc[i]<9.3:
            data['liver_protein_per'].iloc[i]+=16
        elif data['liver_protein'].iloc[i]>=9.3:
            data['liver_protein_per'].iloc[i]+=20
            
    # 20) 알부민
    print('20) 알부민 확률 계산(20% 기준)')
    data["albumin_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['liver_albumin'].iloc[i]<2.5:
            data['albumin_per'].iloc[i]+=20
        elif data['liver_albumin'].iloc[i]>=2.5 and data['liver_albumin'].iloc[i]<3.0:
            data['albumin_per'].iloc[i]+=16
        elif data['liver_albumin'].iloc[i]>=3.0 and data['liver_albumin'].iloc[i]<3.5:
            data['albumin_per'].iloc[i]+=12 
        elif data['liver_albumin'].iloc[i]>=3.5 and data['liver_albumin'].iloc[i]<4.0:
            data['albumin_per'].iloc[i]+=8
        elif data['liver_albumin'].iloc[i]>=4.0 and data['liver_albumin'].iloc[i]<4.3:
            data['albumin_per'].iloc[i]+=4
        elif data['liver_albumin'].iloc[i]>=4.3 and data['liver_albumin'].iloc[i]<4.5:
            data['albumin_per'].iloc[i]+=0
        elif data['liver_albumin'].iloc[i]>=4.5 and data['liver_albumin'].iloc[i]<4.8:
            data['albumin_per'].iloc[i]+=4
        elif data['liver_albumin'].iloc[i]>=4.8 and data['liver_albumin'].iloc[i]<5.3:
            data['albumin_per'].iloc[i]+=8
        elif data['liver_albumin'].iloc[i]>=5.3 and data['liver_albumin'].iloc[i]<5.8:
            data['albumin_per'].iloc[i]+=12
        elif data['liver_albumin'].iloc[i]>=5.8 and data['liver_albumin'].iloc[i]<6.3:
            data['albumin_per'].iloc[i]+=16
        elif data['liver_albumin'].iloc[i]>=6.3:
            data['albumin_per'].iloc[i]+=20
            
    # 21) 요단백
    print('21) 요단백 확률 계산(20% 기준)')
    data["urine_protein_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['urine_protein'].iloc[i]==1:
            data['urine_protein_per'].iloc[i]+=4
        elif data['urine_protein'].iloc[i]==2:
            data['urine_protein_per'].iloc[i]+=8
        elif data['urine_protein'].iloc[i]==3:
            data['urine_protein_per'].iloc[i]+=12 
        elif data['urine_protein'].iloc[i]==4:
            data['urine_protein_per'].iloc[i]+=16
        elif data['urine_protein'].iloc[i]==5:        
            data['urine_protein_per'].iloc[i]+=20
    
    # 22) 혈청 크레아티닌 
    print('22) 혈청 크레아티닌 확률 계산(20% 기준)')
    data["creatinine_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['creatinine'].iloc[i]<0.4:
            data['creatinine_per'].iloc[i]+=20
        elif data['creatinine'].iloc[i]>=0.4 and data['creatinine'].iloc[i]<0.5:
            data['creatinine_per'].iloc[i]+=16
        elif data['creatinine'].iloc[i]>=0.5 and data['creatinine'].iloc[i]<0.6:
            data['creatinine_per'].iloc[i]+=12 
        elif data['creatinine'].iloc[i]>=0.6 and data['creatinine'].iloc[i]<0.7:
            data['creatinine_per'].iloc[i]+=8
        elif data['creatinine'].iloc[i]>=0.7 and data['creatinine'].iloc[i]<0.8:
            data['creatinine_per'].iloc[i]+=4
        elif data['creatinine'].iloc[i]>=0.8 and data['creatinine'].iloc[i]<1.3:
            data['creatinine_per'].iloc[i]+=0
        elif data['creatinine'].iloc[i]>=1.3 and data['creatinine'].iloc[i]<1.4:
            data['creatinine_per'].iloc[i]+=4
        elif data['creatinine'].iloc[i]>=1.4 and data['creatinine'].iloc[i]<1.5:
            data['creatinine_per'].iloc[i]+=8
        elif data['creatinine'].iloc[i]>=1.5 and data['creatinine'].iloc[i]<1.6:
            data['creatinine_per'].iloc[i]+=12
        elif data['creatinine'].iloc[i]>=1.6 and data['creatinine'].iloc[i]<1.7:
            data['creatinine_per'].iloc[i]+=16
        elif data['creatinine'].iloc[i]>=1.7:
            data['creatinine_per'].iloc[i]+=20
    
    # data.to_excel('data/service_data.xlsx',index=False)
    
    print(data.info())
    return data

def get_dataset(data, task, cfg):
    col = cfg[str(task)]

    # 새로운 기준이 있는경우 컬럼 생성
    if task == 1: #간암                
        data['percent_01'] = 0
        print('간암 발병 확률 컬럼 생성')
        for i in tqdm.tqdm(range(0, len(data))):
            if data['liver_b_antigen'].iloc[i]==1:
                data['percent_01'].iloc[i] = 50 + (0.5*(data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + data['r_gtp_per'].iloc[i] +data['hdl_col_per'].iloc[i]))
            else:
                data['percent_01'].iloc[i] = data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + data['r_gtp_per'].iloc[i] +data['hdl_col_per'].iloc[i]
        print(data['percent_01'].value_counts())
        
        # data = data.drop(['alp_yn'], axis=1)  #안 쓸 컬럼 drop 
        # data[col] = data[col].replace(0,2)

    elif task == 2: #위암
        data['percent_02'] = 0
        print('위암 발병 확률 컬럼 생성')
        for i in tqdm.tqdm(range(0, len(data))):
            if data['stomach_helico_bacter'].iloc[i]==1:
                data['percent_02'].iloc[i] = 50 + (0.5*((1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i] + (0.5*data['glucose_per'].iloc[i])))
            else:
                data['percent_02'].iloc[i] = (1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i] + (0.5*data['glucose_per'].iloc[i])
        print(data['percent_02'].value_counts())
        data[col] = data[col].replace(0,2)
        
    elif task == 3: #폐암
        data['percent_03'] = 0
        print("폐암 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_03'].iloc[i]=(1.5*data['cyfra21_1_per'].iloc[i]) + data['cea_per'].iloc[i] + (0.5*data['liver_ast_per'].iloc[i]) + (0.5*data['liver_alp_per'].iloc[i]) + data['glucose_per'].iloc[i] + (0.5*data['ca19_per'].iloc[i])

    elif task == 4: #대장암
        data['percent_04'] = 0
        print("대장암 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_04'].iloc[i]=(1.5*data['cea_per'].iloc[i]) + (1.5*data['ca19_per'].iloc[i]) + (0.5*data['glucose_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i]) + (0.5*data['r_gtp_per'].iloc[i])
        print(data['percent_04'].value_counts())
    
    elif task == 5: #갑상선암
        data['percent_05'] = 0
        print("갑상선암 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_05'].iloc[i]=(1.5*data['ft4_per'].iloc[i]) + (1.5*data['tsh_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['liver_alp_per'].iloc[i])
        print(data['percent_05'].value_counts())
        
    elif task == 6: #유방암
        data['percent_06'] = 0
        print("유방암 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_06'].iloc[i]=(1.5*data['ca15_3_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + data['total_col_per'].iloc[i] + (1.5*data['bmi_per'].iloc[i]) + (0.5*data['hdl_col_per'].iloc[i])
        print(data['percent_06'].value_counts())
        
    elif task == 7: #뇌졸중
        data['percent_07'] = 0
        print("뇌졸중 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_07'].iloc[i]=(2.5*data['blood_press_high_per'].iloc[i]) + (1.5*data['blood_press_low_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i])
        print(data['percent_07'].value_counts())
        
    elif task == 8: #심근경색
        data['percent_08'] = 0
        print("심근경색 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_08'].iloc[i]=(1.5*data['total_col_per'].iloc[i]) + data['ldl_per'].iloc[i] + data['bmi_per'].iloc[i] + (0.5*data['blood_press_high_per'].iloc[i]) + (0.5*data['blood_press_low_per'].iloc[i]) + (0.5*data['glucose_per'].iloc[i])
        print(data['percent_08'].value_counts())

    elif task == 9: #당뇨병
        data['percent_09'] = 0
        print("당뇨병 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_09'].iloc[i]=(2*data['glucose_per'].iloc[i]) + data['tri_gly_per'].iloc[i] + (0.5*data['r_gtp_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i]) + data['ldl_per'].iloc[i]
        print(data['percent_09'].value_counts())
        
    elif task == 10: #폐결핵
        data['percent_10'] = 0
        print("폐결핵 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_10'].iloc[i] = data['total_col_per'].iloc[i] + data['albumin_per'].iloc[i] + data['ldl_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i]
        print(data['percent_10'].value_counts())
                
    elif task == 11: #고혈압
        data['percent_11'] = 0
        print("고혈압 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_11'].iloc[i] = (1.5*data['blood_press_low_per'].iloc[i]) + (1.5*data['blood_press_high_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])  + data['glucose_per'].iloc[i] + (0.5*data['tri_gly_per'].iloc[i])
        print(data['percent_11'].value_counts())
        
    elif task == 12: #고지혈증
        data['percent_12'] = 0
        print("고지혈증 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_12'].iloc[i] = (1.5*data['total_col_per'].iloc[i]) + (1.5*data['tri_gly_per'].iloc[i]) + data['ldl_per'].iloc[i] + data['hdl_col_per'].iloc[i]
        print(data['percent_12'].value_counts())

    elif task == 13: #지방간
        data['percent_13'] = 2
        print("지방간 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_13'].iloc[i] = data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['r_gtp_per'].iloc[i] + data['liver_alp_per'].iloc[i] + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])
        print(data['percent_13'].value_counts())
                    
    elif task == 14: #단백뇨
        data['percent_14'] = 2
        print("단백뇨 발병 확률 컬럼 생성")
        for i in tqdm.tqdm(range(0, len(data))):
            data['percent_14'].iloc[i]=(2*data['urine_protein_per'].iloc[i]) + data['albumin_per'].iloc[i] + data['creatinine_per'].iloc[i] + data['liver_protein_per'].iloc[i]
        print(data['percent_14'].value_counts())

    X = data.drop([col], axis=1)
    y = data[[col]].astype('int')
    # # row 생략 없이 출력
    # pd.set_option('display.max_rows', None)
    # # col 생략 없이 출력
    # pd.set_option('display.max_columns', None)
    # print(X.isna().sum())
    # print(y.isna().sum())
    return X, y

def clean_up_data(data, task, cfg):
    for origin, new in zip(cfg["rename_cols"]["origin"], cfg["rename_cols"]["new"]):
        if origin in data.columns.tolist():
            data = data.rename(columns={origin:new})

    cols = cfg["base"] + cfg[str(task)]

    if set(cols)-set(data.columns.tolist()):
        print("[ERROR] config에 존재하는 컬럼 없음")
        print(set(cols)-set(data.columns.tolist()))

    data = data[cols]
    data = convert_txt2int(data)

    # 숫자, ".", "-" 제외 제거
    data = data.astype("str")
    data = data.replace(regex=r'[^0-9\.-]', value="")
    data = data.replace('', "-1") #np.nan -> 제거
    data = data.fillna("2")

    #이상치 제거
    # for col in data.columns.tolist():
    #    if "per1" not in col and "mj" not in col:
    #        data[col] = data[col].dropna()
    
    #    if "mj1_" in col or "mj2" in col:
    #        idx = data[~((data[col]=="1") | (data[col]=="2"))].index
    #        if not idx.empty:
    #            print(f"[WARNING] {col}에서 이상치 {len(idx)}개 제거")
    #            print(f"확인 해야하는 index: {idx}")
    #            data = data.drop(idx)
    
    data = convert_type(data)

    return data

def convert_type(data):
    col_list = data.columns.tolist()
    for col in col_list:
        data[col] = data[col].astype('float')
        if "per1" in col or "mj" in col:
            data[col] = data[col].astype('int')

    return data