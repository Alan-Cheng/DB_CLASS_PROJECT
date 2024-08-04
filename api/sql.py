import mysql.connector
from typing import Optional

class DB:
    def __init__(self):
        # Connect to MySQL database
        self.connection = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='3CSHOP'
        )

    def connect(self):
        return self.connection.cursor()

    def execute(self, cursor, sql, params=None):
        cursor.execute(sql, params)
        return cursor

    def fetchall(self, cursor):
        return cursor.fetchall()

    def fetchone(self, cursor):
        return cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

db = DB()

class Member:
    @staticmethod
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = %s"
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (account,)))
        cursor.close()
        return result

    @staticmethod
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def create_member(input):
        sql = 'INSERT INTO MEMBER (name, account, password, identity) VALUES (%s, %s, %s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['name'], input['account'], input['password'], input['identity']))
        db.commit()
        cursor.close()

    @staticmethod
    def delete_product(cid, pid):
        sql = 'DELETE FROM CONTAIN WHERE CID=%s AND PID=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (cid, pid))
        db.commit()
        cursor.close()

    @staticmethod
    def get_order(userid):
        sql = 'SELECT * FROM TRANSACTION WHERE MID = %s ORDER BY TTIME DESC'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (userid,)))
        cursor.close()
        return result

    @staticmethod
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (userid,)))
        cursor.close()
        return result

class Cart:
    @staticmethod
    def check(user_id):
        sql = 'SELECT * FROM CART, CONTAIN WHERE CART.MID = %s AND CART.CID = CONTAIN.CID AND tNo IS NULL'
        cursor = db.connect()
        try:
            db.execute(cursor, sql, (user_id,))
            result = cursor.fetchone()  # 读取第一条结果
            cursor.fetchall()  # 确保所有结果都被读取
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            result = None
        finally:
            cursor.close()
        return result

    @staticmethod
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = %s AND tNo IS NULL'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (user_id,)))
        cursor.close()
        return result

    @staticmethod
    def add_cart(user_id, time):
        sql = 'INSERT INTO CART (mid, ctime) VALUES (%s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (user_id, time))
        db.commit()
        cursor.close()

    @staticmethod
    def set_cart(cid, tno):
        sql = 'UPDATE CART SET tNo=%s WHERE cid=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (tno, cid))
        db.commit()
        cursor.close()

class Product:
    @staticmethod
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def get_product(pid):
        sql = 'SELECT * FROM PRODUCT WHERE PID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid,)))
        cursor.close()
        return result

    @staticmethod
    def get_all_product():
        sql = 'SELECT * FROM PRODUCT'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid,)))
        cursor.close()
        return result[0]

    @staticmethod
    def add_product(input):
        sql = 'INSERT INTO PRODUCT (PID, PNAME, PRICE, SNAME, PDESC, PIMAGE) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['pid'], input['pname'], input['price'], input['sname'], input['pdesc'], input['pimage']))
        db.commit()
        cursor.close()

    @staticmethod
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = %s'
        cursor = db.connect()
        db.execute(cursor, sql, (pid,))
        db.commit()
        cursor.close()

    @staticmethod
    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME=%s, PRICE=%s, SNAME=%s, PDESC=%s WHERE PID=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (input[0], input[1], input[2], input[3], input[4]))
        db.commit()
        cursor.close()

    @staticmethod
    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid,)))
        cursor.close()
        return result[0]

    @staticmethod
    def update_image(img):
        sql = 'UPDATE PRODUCT SET PIMAGE=%s WHERE PID=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (img['img'], img['pid']))
        db.commit()
        cursor.close()

class Record:
    @staticmethod
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=%s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (tno,)))
        cursor.close()
        return result[0]

    @staticmethod
    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = %s AND TNO = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid, tno)))
        cursor.close()
        return result

    @staticmethod
    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid,)))
        cursor.close()
        return result[0]

    @staticmethod
    def add_product(input):
        sql = 'INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL) VALUES (%s, %s, %s, %s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['tno'], input['pid'], input['amount'], input['salePrice'], input['total']))
        db.commit()
        cursor.close()

    @staticmethod
    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = %s'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (tno,)))
        cursor.close()
        return result

    @staticmethod
    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = %s AND PID=%s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (tno, pid)))
        cursor.close()
        return result[0]

    @staticmethod
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=%s, TOTAL=%s WHERE PID=%s AND TNO=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (input['amount'], input['total'], input['pid'], input['tno']))
        db.commit()
        cursor.close()

    @staticmethod
    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=%s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (pid,)))
        cursor.close()
        return result

    @staticmethod
    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = %s'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (tno,)))
        cursor.close()
        return result[0]

    @staticmethod
    def add_record(cid, tno):
        contain_list = CONTAIN.get_record(cid)
        for contain in contain_list:
            pid = contain[2]
            amount = contain[1]
            price = Product.get_price(pid)
            total = amount * price
            input = {'tno': tno, 'pid': pid, 'amount': amount, 'salePrice': price, 'total': total}
            sql = 'INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL) VALUES (%s, %s, %s, %s, %s)'
            cursor = db.connect()
            db.execute(cursor, sql, (tno, pid, amount, price, total))
            db.commit()
            cursor.close()

class Analysis:
    @staticmethod
    def month_price(i):
        sql = 'SELECT MONTH(TTIME), SUM(TOTAL) FROM TRANSACTION NATURAL JOIN RECORD WHERE MONTH(TTIME)=%s GROUP BY MONTH(TTIME)'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (i,)))
        cursor.close()
        return result

    @staticmethod
    def month_count(i):
        sql = 'SELECT MONTH(TTIME), COUNT(TNO) FROM TRANSACTION WHERE MONTH(TTIME)=%s GROUP BY MONTH(TTIME)'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (i,)))
        cursor.close()
        return result

    @staticmethod
    def supplier_sale():
        sql = '''
            SELECT SUM(TOTAL) AS total_sales, SNAME 
            FROM (
                SELECT RECORD.TOTAL, PRODUCT.SNAME 
                FROM PRODUCT 
                JOIN RECORD ON PRODUCT.PID = RECORD.PID
            ) AS product_sales
            GROUP BY SNAME
        '''
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def member_sale():
        sql = 'SELECT SUM(TOTAL), MEMBER.MID, MEMBER.NAME FROM TRANSACTION JOIN MEMBER ON TRANSACTION.MID = MEMBER.MID JOIN RECORD ON TRANSACTION.TNO = RECORD.TNO WHERE MEMBER.IDENTITY = %s GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(TOTAL) DESC'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, ('user',)))
        cursor.close()
        return result

    @staticmethod
    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM TRANSACTION JOIN MEMBER ON TRANSACTION.MID = MEMBER.MID WHERE MEMBER.IDENTITY = %s GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, ('user',)))
        cursor.close()
        return result

    @staticmethod
    def month_exist_order(i):
        sql = 'SELECT MONTH(TTIME), COUNT(TNO) FROM TRANSACTION WHERE MONTH(TTIME)=%s GROUP BY MONTH(TTIME)'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (i,)))
        cursor.close()
        return result

    @staticmethod
    def month_total_order(i):
        sql = 'SELECT MONTH(CTIME), COUNT(TNO) FROM CART WHERE MONTH(CTIME)=%s GROUP BY MONTH(CTIME)'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (i,)))
        cursor.close()
        return result

class TRANSACTION:
    @staticmethod
    def add_order(input):
        sql = 'INSERT INTO TRANSACTION (mid, ttime, cid, payment) VALUES (%s, %s, %s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['mid'], input['time'], input['cid'], input['payment']))
        db.commit()
        cursor.close()

    @staticmethod
    def get_orderdetail():
        sql = 'SELECT DISTINCT R.TNO, P.PNAME, R.SALEPRICE, R.AMOUNT FROM RECORD R JOIN PRODUCT P ON R.PID = P.PID'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def get_tno(cid):
        sql = 'SELECT TNO FROM TRANSACTION WHERE CID = %s'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (cid,)))
        cursor.close()
        return result

    @staticmethod
    def get_order():
        sql = 'SELECT T.TNO, M.NAME, T.TTIME, T.CID, T.PAYMENT FROM TRANSACTION T JOIN MEMBER M ON T.MID = M.MID'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result

    @staticmethod
    def delete_order(tno):
        sql = 'DELETE FROM TRANSACTION WHERE TNO = %s'
        cursor = db.connect()
        db.execute(cursor, sql, (tno,))
        db.commit()

        sql = 'DELETE FROM RECORD WHERE TNO = %s'
        db.execute(cursor, sql, (tno,))
        db.commit()
        cursor.close()

class CONTAIN:
    @staticmethod
    def check_product(cid, pid):
        sql = 'SELECT * FROM CONTAIN WHERE CID = %s AND PID = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (cid, pid)))
        cursor.close()
        return result

    @staticmethod
    def add_product(input):
        sql = 'INSERT INTO CONTAIN (CID, units, PID) VALUES (%s, 1, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['cid'], input['pid']))
        db.commit()
        cursor.close()

    @staticmethod
    def get_amount(cid, pid):
        sql = 'SELECT units FROM CONTAIN WHERE CID = %s AND PID=%s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (cid, pid)))
        cursor.close()
        return result[0]

    @staticmethod
    def update_product(input):
        sql = 'UPDATE CONTAIN SET UNITS=%s WHERE PID=%s AND CID=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (input['amount'], input['pid'], input['cid']))
        db.commit()
        cursor.close()

    @staticmethod
    def get_record(cid):
        sql = 'SELECT * FROM CONTAIN WHERE CID = %s'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql, (cid,)))
        cursor.close()
        return result

    @staticmethod
    def get_total(cid):
        sql = 'SELECT units, pid FROM CONTAIN WHERE CID = %s'
        cursor = db.connect()
        product_units = db.fetchall(db.execute(cursor, sql, (cid,)))
        cursor.close()

        total = 0
        for order_product in product_units:
            total += int(order_product[0]) * int(Product.get_price(order_product[1]))
        return total

class SUPPLIER:
    @staticmethod
    def get_sDesc(sname):
        sql = 'SELECT SDESC FROM SUPPLIER WHERE SNAME = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (sname,)))
        cursor.close()
        return result

    @staticmethod
    def add_supplier(input):
        sql = 'INSERT INTO SUPPLIER (sname, sdesc) VALUES (%s, %s)'
        cursor = db.connect()
        db.execute(cursor, sql, (input['sname'], input['sdesc']))
        db.commit()
        cursor.close()

    @staticmethod
    def update_sDesc(input):
        sql = 'UPDATE SUPPLIER SET SDESC=%s WHERE SNAME=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (input['sdesc'], input['sname']))
        db.commit()
        cursor.close()

    @staticmethod
    def delete_check(sname):
        sql = 'SELECT P.pid, S.sname FROM product p JOIN supplier s ON p.sname = s.sname WHERE s.sname = %s'
        cursor = db.connect()
        result = db.fetchone(db.execute(cursor, sql, (sname,)))
        cursor.close()
        return result

    @staticmethod
    def delete_supplier(sname):
        sql = 'DELETE FROM SUPPLIER WHERE SNAME = %s'
        cursor = db.connect()
        db.execute(cursor, sql, (sname,))
        db.commit()
        cursor.close()

    @staticmethod
    def update_supplier(input):
        sql = 'UPDATE SUPPLIER SET SNAME=%s, SDESC=%s WHERE SNAME=%s'
        cursor = db.connect()
        db.execute(cursor, sql, (input['sname'], input['sdesc'], input['sname']))
        db.commit()
        cursor.close()

    @staticmethod
    def get_all_supplier():
        sql = 'SELECT * FROM SUPPLIER'
        cursor = db.connect()
        result = db.fetchall(db.execute(cursor, sql))
        cursor.close()
        return result
