import pymssql
from hwiUtils.info import info_start, info_end


def update_outlierTB():
    info_start('update outlier TB')
    
    """_summary_
    db update 결측치 테이블
    """
    
    info_end('update outlier TB')

def update_hanshinTrainTB():
    info_start('update Hanshin Train TB')
    
    """_summary_
    db insert data 한신 학습TB
    """
    
    info_end('update Hanshin Train TB')
    
def update_infinityTrainTB():
    info_start('update Infinity Train TB')
    
    """_summary_
    db insert data 인피니티 학습TB
    """
    
    info_end('update Infinity Train TB')

def update_hanshinInferenceTB():
    info_start('update Hanshin Inference TB')
    
    """_summary_
    db insert data 일일검진자TB with 발병예측컬럼들은 null로 채워서
    """
    
    # conn = pymssql.connect(server='192.168.0.25' , user='sa', password='!command', database='ANAL_2022')
    # cursor = conn.cursor()
    # cursor.execute('INSERT INTO ANAL_2022.dbo.AutoCare_HCB SELECT * FROM (SELECT CONVERT(CHAR(10), A.per1_date, 23) per1_date, A.per1_bun_no, A.per1_name,\
    #         CONVERT(CHAR(10), A.per1_birth_date, 23) per1_birth_date, SUBSTRING(A.per1_jumin,7,1) per1_gender,A.per1_life_code1,\
    #         A.per1_life_code2, A.per1_life_code3, A.per1_life_code4, A.per1_life_code5, A.per1_ilban, A.per1_kwa1, A.per1_kwa2,\
    #         A.per1_kwa3, A.per1_kwa4, A.per1_kwa5, A.per1_kwa6, A.per1_spc_year, B.mj1_1_1, B.mj1_1_2, B.mj1_2_1, B.mj1_2_2, B.mj1_3_1,\
    #         B.mj1_3_2, B.mj1_4_1, B.mj1_4_2, B.mj1_5_1, B.mj1_5_2, B.mj1_6_1, B.mj1_6_2, B.mj1_7_1,B.mj1_7_2, B.mj2_1, B.mj2_2, B.mj2_3,\
    #         B.mj2_4, B.mj2_5, B.mj3, B.mj4, B.mj5, B.mj6, B.mj71, B.mj72, B.mj73, B.mj74, B.mj8_1, B.mj8_2_1, B.mj8_2_2, B.mj9_1, B.mj9_2_1,\
    #         B.mj9_2_2, B.mj10, C.gul_gum_code, C.gul_value_form FROM HCMS_2018.dbo.M01002TB1 A, HCMS_2018.dbo.M01010TB1_2019 B,\
    #         HCMS_2018.dbo.M01007TB1 C WHERE A.per1_date=B.mj_date and A.per1_bun_no=B.mj_no and A.per1_date=C.gul_date and A.per1_bun_no=C.gul_bun_no\
    #         and A.per1_date >= DATEADD(DAY, -1, CONVERT(NVARCHAR, GETDATE(), 112)) and A.per1_date <CONVERT(NVARCHAR, GETDATE(), 112))\
    #         AS result PIVOT (MIN(gul_value_form) FOR gul_gum_code IN ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904],\
    #         [C038], [C026], [C027], [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], [I348],\
    #         [I502], [I503], [I349]))AS pivot_result;')
    # conn.commit()
    
    info_end('update Hanshin Inference TB')