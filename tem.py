
import  sqlite3
conn=sqlite3.connect("invoice.db")
print("数据库创建成功!")

conn.execute("""
CREATE TABLE INVOICE_REGISTRATION(
            INVOICE_ID TEXT PRIMARY KEY NOT NULL ,
            FILE_NAME TEXT ,
            FROM_NAME TEXT , 
            FROM_ID TEXT,
            TO_NAME TEXT , 
            TO_ID TEXT,
            TYPE_NAME TEXT,
            TYPE_ID TEXT,
            SUM_PRICE TEXT,
            INVOICE_DATE TEXT,
            CREATE_DATE TEXT)
""")
print ("INVOICE_REGISTRATION表创建成功！")