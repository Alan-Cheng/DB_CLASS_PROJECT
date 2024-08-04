import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import *

store = Blueprint('bookstore', __name__, template_folder='../templates')

@store.route('/', methods=['GET', 'POST'])
@login_required
def bookstore():
    result = Product.count()
    count = math.ceil(result[0]/6)
    flag = 0
    
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 6
        end = page * 6
        search = request.values.get('keyword')
        keyword = search
        
        cursor.prepare('SELECT * FROM PRODUCT WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2],
                '商品圖片': i[5],
            }
            book_data.append(book)
            total = total + 1
        
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
            
        count = math.ceil(total/6)
        
        return render_template('bookstore.html', single=single, keyword=search, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    

    
    elif 'pid' in request.args:
        pid = request.args['pid']
        data = Product.get_product(pid)
        
        pname = data[1]
        price = data[2]
        sname = data[3]
        description = data[4]

        image = 'default.png'  #在此更改圖片
        if(data[5] != None):
            image = data[5]

        sdesc = '尚未新增品牌介紹'
        if(SUPPLIER.get_sDesc(sname) != None):
            sdesc = SUPPLIER.get_sDesc(sname)[0]
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '單價': price,
            '品牌': sname,
            '商品敘述': description,
            '商品圖片': image,
            '品牌介紹': sdesc
        }

        return render_template('product.html', data = product, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 6
        end = page * 6
        
        book_row = Product.get_all_product()
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2],
                '商品圖片': i[5]
            }
            book_data.append(book)
            
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
        
        return render_template('bookstore.html', book_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM PRODUCT WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        book_data = []
        total = 0
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2],
                '商品圖片': i[5]
            }

            book_data.append(book)
            total = total + 1
            
        if(len(book_data) < 6):
            flag = 1
        
        count = math.ceil(total/6)    
        
        return render_template('bookstore.html', keyword=search, single=single, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        book_row = Product.get_all_product()
        book_data = []
        temp = 0
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2],
                '商品圖片': i[5]
            }
            if len(book_data) < 6:
                book_data.append(book)
        
        return render_template('bookstore.html', book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)

# 會員購物車
@store.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            data = Cart.get_cart(current_user.id)
            
            if( data == None): #假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Cart.add_cart(current_user.id, time) # 幫他加一台購物車
                data = Cart.get_cart(current_user.id) 
            cid = int(data[0]) # 取得購物車編號(cId)
            pid = request.values.get('pid') # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            product = CONTAIN.check_product(cid, pid)

            # 如果購物車裡面沒有的話 把他加一個進去
            if(product == None):
                CONTAIN.add_product( {'cid': cid, 'pid':pid} )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                amount = CONTAIN.get_amount(cid, pid)
                CONTAIN.update_product({'amount':amount+1, 'pid':pid, 'cid':cid})

        elif "delete" in request.form :
            pid = request.values.get('delete')
            cid = Cart.get_cart(current_user.id)[0]
            
            Member.delete_product(cid, pid)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('bookstore.bookstore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('bookstore.order'))

        elif "order" in request.form:
            cid = Cart.get_cart(current_user.id)[0]
            total = CONTAIN.get_total(cid)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            TRANSACTION.add_order( {'mid': current_user.id, 
                                    'time':time, 
                                    'cid':cid, 
                                    'format':format, 
                                    'payment':'轉帳',
                                    } )

            tno = TRANSACTION.get_tno(cid)[0][0]
            Cart.set_cart(cid, tno)

            Record.add_record(cid, tno)

            return render_template('complete.html', user=current_user.name)

    product_data = only_cart()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=product_data, user=current_user.name)

@store.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    cid = data[0]
    product_row = CONTAIN.get_record(cid)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[2])
        product = {
            '商品編號': i[2],
            '商品名稱': pname,
            '商品價格': Product.get_price(i[2]),
            '數量': i[1]
        }
        product_data.append(product)
    
    total = CONTAIN.get_total(cid)

    return render_template('order.html', data=product_data, total=total, user=current_user.name)

@store.route('/orderlist', methods=['GET', 'POST'])
def orderlist():
    #新增取消訂單的功能
    if 'delete' in request.values:
        tno = request.values.get('delete')
        data = TRANSACTION.delete_order(tno)


    if "oid" in request.args :
        pass
    
    user_id = current_user.id

    data = Member.get_order(user_id)
    orderlist = []

    for i in data:
        temp = {
            '訂單編號': i[0],
            '訂單總價': CONTAIN.get_total(i[3]),
            '訂單時間': i[2]
        }
        orderlist.append(temp)
    
    orderdetail_row = TRANSACTION.get_orderdetail()
    orderdetail = []

    for j in orderdetail_row:
        temp = {
            '訂單編號': j[0],
            '商品名稱': j[1],
            '商品單價': j[2],
            '訂購數量': j[3]
        }
        orderdetail.append(temp)


    return render_template('orderlist.html', data=orderlist, detail=orderdetail, user=current_user.name)

def change_order():
    data = Cart.get_cart(current_user.id)
    cid = data[0] # 使用者有購物車了，取得購物車編號
    product_row = CONTAIN.get_record(cid)

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        # i[0]：cid / i[1]：商品數量 / i[2]：pid
        if int(request.form[i[2]]) != i[1]:
            CONTAIN.update_product({
                'amount':request.form[i[2]],
                'pid':i[2],
                'cid':cid,
                #'total':int(request.form[i[1]])*int(Product.get_price(i[2]))
            })
            print('change')

    return 0


def only_cart():
    count = Cart.check(current_user.id)
    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    cid = data[0]
    product_row = CONTAIN.get_record(cid)
    product_data = []

    for i in product_row:
        pid = i[2]
        pname = Product.get_name(pid)
        price = Product.get_price(pid)
        amount = i[1]
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '數量': amount
        }
        product_data.append(product)
    
    return product_data