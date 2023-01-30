import numpy as np
import pandas as pd
import sys
import os
import json
import glob
import joblib
import argparse
import tqdm
# import seaborn as sns

## 데이터 불러오기
data = pd.read_excel('data/new_train_dataset.xlsx')
data.info()

## 만 나이 계산 
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

print(data['per1_age'].unique()) # 최고령/최연소 및 연령대 파악
print(data['per1_spc_year'].value_counts()) # 연도별 검진자 수 조회

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
print(data['age_group'].value_counts()) # 연령대별 검진자 수 조회
print(data. columns)

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
print(data['per1_gender'].value_counts())

## 혈액검사 전처리
# 비만도 전처리
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
# data['obesity'] = data['obesity'].astype('int')
        
# 요단백 전처리  
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
# data['urine_protein'] = data['urine_protein'].astype('int')

# B형간염표면항원 전처리
print("B형간염표면항원 값 치환")
for i in tqdm.tqdm(range(0, len(data))):
    if data['liver_b_antigen'].iloc[i]=='음성':
        data['liver_b_antigen'].iloc[i]=0
    elif data['liver_b_antigen'].iloc[i]=='약양성':
            data['liver_b_antigen'].iloc[i]=1
    elif data['liver_b_antigen'].iloc[i]=='양성':
            data['liver_b_antigen'].iloc[i]=2
# data['liver_b_antigen'] = data['liver_b_antigen'].astype('int')

## 혈액검사 30개 컬럼 피벗 테이블 생성
print('혈액검사 30개 컬럼 피벗 테이블 생성')
# 1) 신장
print("1) 신장 (height)")
pt_height_1 = pd.pivot_table(data,                # 피벗할 데이터프레임
                     index = 'age_group',    # 행 위치에 들어갈 열
                     columns = 'per1_gender',    # 열 위치에 들어갈 열
                     values = 'height',     # 데이터로 사용할 열
                     aggfunc = 'mean')   # 데이터 집계함수
print(pt_height_1)

# 2) 체중
print("2) 체중 (weight)")
pt_weight_2 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'weight',
                     aggfunc = 'mean') 
print(pt_weight_2)

# 3) 허리둘레
print("3) 허리둘레 (wai_cir)")
pt_wai_cir_3 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'wai_cir',
                     aggfunc = 'mean') 
print(pt_wai_cir_3)

# 4) BMI
print("4) BMI")
pt_bmi_4 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'bmi',
                     aggfunc = 'mean') 
print(pt_bmi_4)

# 5) 비만도
print("5) 비만도 (obesity)")
pt_obesity_5 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'obesity',
                     aggfunc = 'mean') 
print(pt_obesity_5)

# 6) 수축기 혈압
print("6) 수축기 혈압 (blood_press_high)")
pt_bp_high_6 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'blood_press_high',
                     aggfunc = 'mean') 
print(pt_bp_high_6)

# 7) 이완기 혈압
print("7) 이완기 혈압 (blood_press_low)")
pt_bp_low_7 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'blood_press_low',
                     aggfunc = 'mean') 
print(pt_bp_low_7)

# 8) 총 콜레스테롤
print("8) 총 콜레스테롤 (total_col)")
pt_total_col_8 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'total_col',
                     aggfunc = 'mean') 
print(pt_total_col_8)

# 9) HDL 콜레스테롤
print("9) HDL 콜레스테롤 (hdl_col)")
pt_hdl_col_9 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'hdl_col',
                     aggfunc = 'mean') 
print(pt_hdl_col_9)

# 10) LDL 콜레스테롤
print("10) LDL 콜레스테롤 (ldl_col)")
pt_ldl_col_10 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'ldl_col_cal',
                     aggfunc = 'mean') 
print(pt_ldl_col_10)

# 11) 중성지방
print("11) 중성지방 (tri_gly)")
pt_tri_gly_11= pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'tri_gly',
                     aggfunc = 'mean') 
print(pt_tri_gly_11)

# 12) r-GTP
print("12) r-GTP")
pt_r_gtp_12 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'r_gtp',
                     aggfunc = 'mean') 
print(pt_r_gtp_12)

# 13) 총 빌리루빈
print("13) 총 빌리루빈 (liver_bilirubin)")
pt_liver_bilirubin_13 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_bilirubin',
                     aggfunc = 'mean') 
print(pt_liver_bilirubin_13)

# 14) 총 단백
print("14) 총 단백 (liver_protein)")
pt_liver_protein_14 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_protein',
                     aggfunc = 'mean') 
print(pt_liver_protein_14)

# 15) 알부민
print("15) 알부민 (liver_albumin)")
pt_liver_albumin_15 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_albumin',
                     aggfunc = 'mean') 
print(pt_liver_albumin_15)

# 16) 글로불린
print("16) 글로불린 (liver_globulin)")
pt_liver_globulin_16 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_globulin',
                     aggfunc = 'mean') 
print(pt_liver_globulin_16)

# 17) AST
print("17) AST")
pt_liver_ast_17 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_ast',
                     aggfunc = 'mean') 
print(pt_liver_ast_17)

# 18) ALT
print("18) ALT")
pt_liver_alt_18 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_alt',
                     aggfunc = 'mean') 
print(pt_liver_alt_18)

# 19) ALP
print("19) ALP")
pt_liver_alp_19 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_alp',
                     aggfunc = 'mean') 
print(pt_liver_alp_19)

# 20) 공복혈당
print("20) 공복혈당")
pt_glucose_20 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'glucose',
                     aggfunc = 'mean') 
print(pt_glucose_20)

# 21) 요단백
print("21) 요단백")
pt_urine_protein_21= pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'urine_protein',
                     aggfunc = 'mean') 
print(pt_urine_protein_21)

# 22) 혈청 크레아티닌
print("22) 혈청 크레아티닌")
pt_creatinine_22 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'creatinine',
                     aggfunc = 'mean') 
print(pt_creatinine_22)

# 23) B형 간염표면 항원
print("23) B형 간염표면 항원")
pt_liver_b_antigen_23 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'liver_b_antigen',
                     aggfunc = 'mean') 
print(pt_liver_b_antigen_23)

# 24) 헬리코박터
print("24) 헬리코박터(helico_bacter)")
pt_helico_bacter_24 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'stomach_helico_bacter',
                     aggfunc = 'mean') 
print(pt_helico_bacter_24)

# 25) Cyfra21-1
print("25) Cyfra21-1 (lung_cyfra21_1)")
pt_cyfra21_1_25 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'lung_cyfra21_1',
                     aggfunc = 'mean') 
print(pt_cyfra21_1_25)

# 26) CEA
print("26) CEA")
pt_cea_26 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'lar_int_cea',
                     aggfunc = 'mean') 
print(pt_cea_26)

# 27) CA19
print("27) CA19")
pt_ca19_27 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'lar_int_ca19',
                     aggfunc = 'mean') 
print(pt_ca19_27)

# 28) TSH
print("28) TSH")
pt_tsh_28 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'thy_tsh',
                     aggfunc = 'mean') 
print(pt_tsh_28)

# 29) FT4
print("29) FT4")
pt_ft4_29 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'thy_ft4',
                     aggfunc = 'mean') 
print(pt_ft4_29)

# 30) CA15-3
print("30) CA15-3")
pt_ca15_3_30 = pd.pivot_table(data,
                     index = 'age_group',
                     columns = 'per1_gender',
                     values = 'breast_ca15_3',
                     aggfunc = 'mean') 
print(pt_ca15_3_30)

print(pt_cyfra21_1_25.info())
print(pt_cyfra21_1_25.columns)