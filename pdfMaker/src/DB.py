import pymssql
# conn = pymssql.connect(server='192.168.0.25', user='sa', password='!command', database='ANAL_2022')
# cursor = conn.cursor()  
# cursor.execute('select * from dbo.HCB_DISEASE_FACTOR')

# row = cursor.fetchall()
# print(row)
# cursor.execute('SELECT c.CustomerID, c.CompanyName,COUNT(soh.SalesOrderID) AS OrderCount FROM SalesLT.Customer AS c LEFT OUTER JOIN SalesLT.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID GROUP BY c.CustomerID, c.CompanyName ORDER BY OrderCount DESC;')  
# row = cursor.fetchone()  
# while row:  
#     print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))     
#     row = cursor.fetchone()  

class HanshinDatabase(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HanshinDatabase, cls).__new__(cls)
            conn = pymssql.connect(server='192.168.0.25', user='sa', password='!command', database='ANAL_2022')
            cls.cursor = conn.cursor()  
            print('Login Database')
            
            return cls.instance
        else:
            print('Logined Database')
            return cls.instance
    
    def get_patientData(cls, cht_no, gum_no, inspc_date, name):
        pass

    def check_cht_no(cls, cht_no):
        pass
    
    def check_gum_no(cls, gum_no):
        pass

    def check_inspc_date(cls, inspc_date):
        pass

    def check_name(cls, name):
        pass