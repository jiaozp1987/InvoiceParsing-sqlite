from datetime import datetime
import sqlite3
import threading
import functools

PATH_DATABASE = './invoice.db'


def synchronized(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.lock:
            return func(self, *args, **kwargs)

    return wrapper


class SQLops:

    def __init__(self) -> None:
        self.lock = threading.Lock()

    # 添加
    @synchronized
    def add(self, invoice):
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        cur.execute(
            "insert into INVOICE_REGISTRATION (INVOICE_ID,FILE_NAME,FROM_NAME,FROM_ID,TO_NAME,TO_ID,TYPE_NAME,TYPE_ID,SUM_PRICE,INVOICE_DATE,CREATE_DATE) values (?,?,?,?,?,?,?,?,?,?,?)",
            (invoice.id, invoice.fileName, invoice.formName, invoice.formID, invoice.toName, invoice.toID,
             invoice.typeName,
             invoice.typeID, invoice.sumPrice, invoice.invoiceDate, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")),))
        conn.commit()
        conn.close()
        return cur.lastrowid

    # 查询
    @synchronized
    def find_by_id(self, invoice):
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        cur.execute(
            "select INVOICE_ID,FILE_NAME,FROM_NAME,FROM_ID,TO_NAME,TO_ID,TYPE_NAME,TYPE_ID,SUM_PRICE,INVOICE_DATE,CREATE_DATE from INVOICE_REGISTRATION where INVOICE_ID = ?  ",
            (invoice.id,))
        info = cur.fetchone()
        conn.close()
        return info
