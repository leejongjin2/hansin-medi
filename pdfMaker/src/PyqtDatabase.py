import pymssql
class HanshinDatabase(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HanshinDatabase, cls).__new__(cls)
            conn = pymssql.connect(server='192.168.0.25', user='sa', password='!command', database='ANAL_2022')
            cls.cursor = conn.cursor()  
            
            cls.patient_indexName = ['검진일자', '차트번호', '검체번호', '이름', '생년월일', '성별']
            cls.patient_column = 'per1_date, per1_chat_no, per1_bun_no, per1_name, per1_birth_date, per1_gender'
            
            cls.analysis_indexName = ['분석지표', '분석지표 한글명', '남성 최저치', '남성 최고치', '여성 최저치' '여성 최고치', '단위', '검사코드']
            cls.analysis_column = 'analysis_index_kor, male_min_value, male_max_value, female_min_value, female_max_value, unit, gum_code'
            
            return cls.instance
        else:
            print('Logined Database')
            return cls.instance
    
    def get_patientData(cls, cht_no, bun_no, inspc_date, name):
        if not (cht_no or bun_no or inspc_date or name):
            raise ValueError
        
        # TODO add try except
        sql = cls.get_patientSearching_sql(cht_no, bun_no, inspc_date, name)
        cls.cursor.execute(sql)
        patients = cls.cursor.fetchall()
        return cls.patient_indexName, patients

    def get_patientSearching_sql(cls, cht_no, bun_no, inspc_date, name):
        # TODO delete TOP
        sql = 'SELECT '+ cls.patient_column + ' FROM ANAL_2022.dbo.HCB_Train_Data WHERE '
        # sql = 'SELECT TOP(100) '+ cls.patient_column + ' FROM ANAL_2022.dbo.HCB_Train_Data WHERE '
        
        temp = []
        if cht_no:
            temp.append(f"per1_chat_no = '{cht_no}'")
        if bun_no:
            temp.append(f"per1_bun_no = '{bun_no}'")
        if inspc_date:
            temp.append(f"per1_date = '{inspc_date}'")
        if name:
            temp.append(f"per1_name = '{name}'")
            
        sql += ' and '.join(temp)
        return sql

    def get_analysisIndexes(cls):
        sql = 'SELECT analysis_index, analysis_index_kor, male_min_value, male_max_value, female_min_value, female_max_value, unit, gum_code FROM ANAL_2022.dbo.HCB_FACTOR_INFO'
        
        # TODO add try except
        cls.cursor.execute(sql)
        indexes = cls.cursor.fetchall()
        return cls.analysis_indexName, indexes