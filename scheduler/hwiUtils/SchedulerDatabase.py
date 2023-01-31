import pymssql
from hwiUtils.info import info_start, info_end
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HanshinDatabase(object):
    def __init__(self):
        print('start database')
        self.conn = pymssql.connect(server='192.168.0.25', user='sa', password='!command', database='ANAL_2022')
        self.today = datetime(2023, 1, 1)
        
    def get_hanshinTrainData(self):
        info_start("get Hanshin Train Data")

        columns = ['per1_date', 'per1_chat_no', 'per1_bun_no', 'per1_name', 'per1_birth_date',\
       'per1_gender', 'per1_life_code1', 'per1_life_code2', 'per1_life_code3',\
       'per1_life_code4', 'per1_life_code5', 'per1_ilban', 'per1_kwa1',\
       'per1_kwa2', 'per1_kwa3', 'per1_kwa4', 'per1_kwa5', 'per1_kwa6',\
       'per1_spc_year', 'mj1_1_1', 'mj1_1_2', 'mj1_2_1', 'mj1_2_2', 'mj1_3_1',\
       'mj1_3_2', 'mj1_4_1', 'mj1_4_2', 'mj1_5_1', 'mj1_5_2', 'mj1_6_1',\
       'mj1_6_2', 'mj1_7_1', 'mj1_7_2', 'mj2_1', 'mj2_2', 'mj2_3', 'mj2_4',\
       'mj2_5', 'mj3', 'mj4', 'mj5', 'mj6', 'mj71', 'mj72', 'mj73', 'mj74',\
       'mj8_1', 'mj8_2_1', 'mj8_2_2', 'mj9_1', 'mj9_2_1', 'mj9_2_2', 'mj10',\
       'height', 'weight', 'wai_cir', 'bmi', 'obesity', 'blood_press_high',\
       'blood_press_low', 'total_col', 'hdl_col', 'ldl_col_cal', 'tri_gly',\
       'r_gtp', 'liver_bilirubin', 'liver_protein', 'liver_albumin',\
       'liver_globulin', 'liver_ast', 'liver_alt', 'liver_alp', 'glucose',\
       'urine_protein', 'creatinine', 'liver_b_antigen',\
       'stomach_helico_bacter', 'lung_cyfra21_1', 'lar_int_cea',\
       'lar_int_ca19', 'thy_tsh', 'thy_ft4', 'breast_ca15_3']
        
        info_end("get Hanshin Train Data")
    
    def get_infinityTrainData(self):
        pass
    
    def update_outlierTB(self):
        info_start('update outlier TB')
        
        """_summary_
        db update 결측치 테이블
        """
        
        # self.conn.commit()
        info_end('update outlier TB')

    def update_hanshinTrainTB(self):
        info_start('update Hanshin Train TB')
        
        # today = datetime.today().strftime('%Y-%m-%d')
        prior_updatedDate = self.today - relativedelta(months=3, days=1)

        # test용 코드        
        # def test(today, prior_updatedDate):
        #     today = today + relativedelta(months=3)
        #     prior_updatedDate = today - relativedelta(months=3, days=1)
        #     print('after ', today, prior_updatedDate)
        #     return today, prior_updatedDate
        
        # Where 문 : 마지막 업데이트 날짜, 분기별 업데이트 날짜 기록
        sql = f"INSERT INTO ANAL_2022.dbo.HCB_Train_Data \
                SELECT * FROM ANAL_2022.dbo.AutoCare_HCB \
                WHERE per1_date > '{prior_updatedDate}' and per1_date <= '{self.today}' and (per1_chat_no) IN ( \
                SELECT per1_chat_no \
                FROM ANAL_2022.dbo.AutoCare_HCB \
                GROUP BY per1_chat_no, per1_birth_date, per1_name \
                HAVING  COUNT(per1_chat_no) >= 3) \
                ORDER BY per1_birth_date, per1_name, per1_date ASC;"

        cursor = self.conn.cursor()
        cursor.execute(sql)

        # self.conn.commit()
        info_end('update Hanshin Train TB')
        
    def update_infinityTrainTB(self):
        info_start('update Infinity Train TB')
        
        """_summary_
        db insert data 인피니티 학습TB
        """
        
        # self.conn.commit()
        info_end('update Infinity Train TB')

    def update_hanshinInferenceTB(self):
        info_start('update Hanshin Inference TB')
        
        """_summary_
        db insert data 일일검진자TB with 발병예측컬럼들은 null로 채워서
        """
        before_3days = self.today - relativedelta(days=3)
        before_2days = self.today - relativedelta(days=2)
        
        sql = f"INSERT INTO ANAL_2022.dbo.AutoCare_HCB (per1_date, per1_chat_no, per1_bun_no, per1_name, per1_birth_date, per1_gender, \
                    per1_life_code1, per1_life_code2, per1_life_code3, per1_life_code4, per1_life_code5, per1_ilban, per1_kwa1, per1_kwa2, \
                    per1_kwa3, per1_kwa4, per1_kwa5, per1_kwa6, per1_spc_year, mj1_1_1, mj1_1_2, mj1_2_1, mj1_2_2, mj1_3_1, \
                    mj1_3_2, mj1_4_1, mj1_4_2, mj1_5_1, mj1_5_2, mj1_6_1, mj1_6_2, mj1_7_1,mj1_7_2, mj2_1, mj2_2, mj2_3, \
                    mj2_4, mj2_5, mj3, mj4, mj5, mj6, mj71, mj72, mj73, mj74, mj8_1, mj8_2_1, mj8_2_2, mj9_1, mj9_2_1, mj9_2_2, mj10, \
                    TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, \
                    C038, C026, C027, C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022, I348, \
                    I502, I503, I349) \
                    SELECT * FROM (SELECT CONVERT(CHAR(10), A.per1_date, 23) per1_date, A.per1_chat_no, A.per1_bun_no, A.per1_name, \
                        CONVERT(CHAR(10), A.per1_birth_date, 23) per1_birth_date, SUBSTRING(A.per1_jumin,7,1) per1_gender,A.per1_life_code1, \
                        A.per1_life_code2, A.per1_life_code3, A.per1_life_code4, A.per1_life_code5, A.per1_ilban, A.per1_kwa1, A.per1_kwa2, \
                        A.per1_kwa3, A.per1_kwa4, A.per1_kwa5, A.per1_kwa6, A.per1_spc_year, B.mj1_1_1, B.mj1_1_2, B.mj1_2_1, B.mj1_2_2, B.mj1_3_1, \
                        B.mj1_3_2, B.mj1_4_1, B.mj1_4_2, B.mj1_5_1, B.mj1_5_2, B.mj1_6_1, B.mj1_6_2, B.mj1_7_1,B.mj1_7_2, B.mj2_1, B.mj2_2, B.mj2_3, \
                        B.mj2_4, B.mj2_5, B.mj3, B.mj4, B.mj5, B.mj6, B.mj71, B.mj72, B.mj73, B.mj74, B.mj8_1, B.mj8_2_1, B.mj8_2_2, B.mj9_1, B.mj9_2_1, \
                        B.mj9_2_2, B.mj10, C.gul_gum_code, C.gul_value_form FROM HCMS_2018.dbo.M01002TB1 A, HCMS_2018.dbo.M01010TB1_2019 B, \
                        HCMS_2018.dbo.M01007TB1 C WHERE A.per1_date=B.mj_date and A.per1_bun_no=B.mj_no and A.per1_date=C.gul_date and A.per1_bun_no=C.gul_bun_no \
                        and A.per1_date >= {before_3days} and A.per1_date < {before_2days} \
                        AS result PIVOT (MIN(gul_value_form) FOR gul_gum_code IN ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904], \
                        [C038], [C026], [C027], [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], [I348], \
                        [I502], [I503], [I349]))AS pivot_result;" \
        
        cursor = self.conn.cursor()
        cursor.execute(sql)
        # self.conn.commit()
        info_end('update Hanshin Inference TB')
        
    def close_db(self):
        self.conn.close()