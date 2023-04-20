from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER(name, account, password, identity) VALUES (:name, :account, :password, :identity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(cid, pid):
        sql = 'DELETE FROM CONTAIN WHERE CID=:cid and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'cid': cid, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM TRANSACTION WHERE MID = :id ORDER BY TTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, CONTAIN WHERE CART.MID = :id AND CART.CID = CONTAIN.CID AND tNo IS NULL'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id AND tNo IS NULL'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART(mid, ctime, cid) VALUES (:id, TO_DATE(:time, :format ), cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time, 'format':'yyyy/mm/dd hh24:mi:ss'})
        DB.commit()

    def set_cart(cid, tno):
        sql = 'UPDATE CART SET tNo=:tno WHERE cid=:cid'
        DB.execute_input( DB.prepare(sql), {'cid': cid, 'tno':tno})
        DB.commit()
       
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        sql ='SELECT * FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_product():
        sql = 'SELECT * FROM PRODUCT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO PRODUCT VALUES (:pid, :pname, :price, :sname, :pdesc, :pimage)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, SNAME=:supplier, PDESC=:description WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]
    
    #新增
    def update_image(img):
        sql = 'UPDATE PRODUCT SET PIMAGE=:img WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), img)
        DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    
    #新增的function
    def add_record(cid, tno):
        contain_list = CONTAIN.get_record(cid)
        for contain in contain_list:
            pid = contain[2]
            amount = contain[1]
            price = Product.get_price(pid)
            total = amount * price
            input = {'tno': tno, 'pid': pid, 'amount':amount, 'salePrice': price, 'total': total}
            sql = 'INSERT INTO RECORD VALUES (:tno, :pid, :amount, :salePrice, :total)'
            DB.execute_input(DB.prepare(sql), input)
            DB.commit()

class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM TTIME), SUM(TOTAL)\
                FROM TRANSACTION NATURAL JOIN RECORD\
                WHERE EXTRACT(MONTH FROM TTIME)=:mon\
                GROUP BY EXTRACT(MONTH FROM TTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM TTIME), COUNT(TNO)\
                FROM TRANSACTION\
                WHERE EXTRACT(MONTH FROM TTIME)=:mon\
                GROUP BY EXTRACT(MONTH FROM TTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def supplier_sale():
        sql = 'SELECT SUM(TOTAL), SNAME\
                FROM(SELECT * FROM PRODUCT,RECORD\
                WHERE PRODUCT.PID = RECORD.PID)\
                GROUP BY SNAME'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(TOTAL), MEMBER.MID, MEMBER.NAME \
                FROM TRANSACTION, MEMBER, RECORD\
                WHERE TRANSACTION.MID = MEMBER.MID \
                    AND MEMBER.IDENTITY = :identity \
                    AND TRANSACTION.TNO = RECORD.TNO \
                GROUP BY MEMBER.MID, MEMBER.NAME \
                ORDER BY SUM(TOTAL) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME \
            FROM TRANSACTION, MEMBER \
            WHERE TRANSACTION.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity \
            GROUP BY MEMBER.MID, MEMBER.NAME \
            ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))
    
    #訂單流失分析用的SQL

    def month_exist_order(i):
        sql = 'SELECT EXTRACT(MONTH FROM TTIME), COUNT(TNO)\
                FROM TRANSACTION\
                WHERE EXTRACT(MONTH FROM TTIME)=:mon\
                GROUP BY EXTRACT(MONTH FROM TTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def month_total_order(i):
        sql = 'SELECT EXTRACT(MONTH FROM CTIME), COUNT(TNO)\
                FROM CART\
                WHERE EXTRACT(MONTH FROM CTIME)=:mon\
                GROUP BY EXTRACT(MONTH FROM CTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))


#以下為新增的ＳＱＬ
class TRANSACTION():
    def add_order(input):
        sql = 'INSERT INTO TRANSACTION(mid, ttime, cid, payment) VALUES (:mid, TO_DATE(:time, :format ), :cid, :payment)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def get_orderdetail():
        sql = 'SELECT DISTINCT R.TNO, P.PNAME, R.SALEPRICE, R.AMOUNT\
                FROM RECORD R, PRODUCT P\
                WHERE R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_tno(cid):
        sql = 'SELECT TNO FROM TRANSACTION WHERE CID = :cid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'cid': cid}))
    
    def get_order():
        sql = 'SELECT T.TNO, M.NAME, T.TTIME, T.CID, T.PAYMENT\
            FROM TRANSACTION T, MEMBER M\
            WHERE T.MID = M.MID'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def delete_order(tno):
        sql = 'DELETE FROM TRANSACTION WHERE TNO = :tno'
        DB.execute_input(DB.prepare(sql), {'tno': tno})
        DB.commit()
        sql = 'DELETE FROM RECORD WHERE TNO = :tno'
        DB.execute_input(DB.prepare(sql), {'tno': tno})
        DB.commit()

class CONTAIN():
    def check_product(cid, pid):
        sql = 'SELECT * FROM CONTAIN WHERE CID = :cid and PID = :pid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'cid': cid, 'pid': pid}))

    def add_product(input):
        sql = 'INSERT INTO CONTAIN(cid, units, pid) VALUES (:cid, 1, :pid)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_amount(cid, pid):
        sql = 'SELECT units FROM CONTAIN WHERE CID = :cid and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'cid': cid, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE CONTAIN SET UNITS=:amount WHERE PID=:pid and CID=:cid'
        DB.execute_input(DB.prepare(sql), input)

    def get_record(cid):
        sql = 'SELECT * FROM CONTAIN WHERE CID = :cid'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'cid': cid}))
    
    def get_total(cid):
        sql = 'SELECT units, pid FROM CONTAIN WHERE CID = :cid'
        product_units = DB.fetchall(DB.execute_input( DB.prepare(sql), {'cid':cid}))

        total = 0
        for order_product in product_units:
            total += int(order_product[0]) * int(Product.get_price(order_product[1]))
        return total
    
class SUPPLIER():
    def get_sDesc(sname):
        sql = 'SELECT SDESC FROM SUPPLIER WHERE SNAME = :sname'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'sname': sname}))
    
    def add_supplier(input):
        sql = 'INSERT INTO SUPPLIER(sname, sdesc) VALUES (:sname, :sdesc)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def update_sDesc(input):
        sql = 'UPDATE SUPPLIER SET SDESC=:sdesc WHERE SNAME=:sname'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_check(sname):
        sql = 'SELECT P.pid, S.sname \
        FROM product p, supplier s\
        WHERE p.sname = s.sname AND s.sname = :sname'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'sname':sname}))
    
    def delete_supplier(sname):
        sql = 'DELETE FROM SUPPLIER WHERE SNAME = :sname'
        DB.execute_input(DB.prepare(sql), {'sname': sname})
        DB.commit()

    def update_supplier(input):
        sql = 'UPDATE SUPPLIER SET SNAME=:sname, SDESC=:sdesc WHERE SNAME=:sname'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_all_supplier():
        sql = 'SELECT * FROM SUPPLIER'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def add_supplier(input):
        sql = 'INSERT INTO SUPPLIER VALUES (:sname, :sdesc)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()