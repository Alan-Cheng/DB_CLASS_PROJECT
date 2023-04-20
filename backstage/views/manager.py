from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = os.path.abspath(os.curdir) + '/static/product/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    #為了讓下拉式選單可以顯示所有的品牌，先將所有的品牌render到前端
    all_supplier = []
    for i in SUPPLIER.get_all_supplier():
        data = {
            '品牌': i[0],
        }
        all_supplier.append(data)

    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            image = data[5]
            if(image != None):
                os.remove(os.path.join(config(), image))

            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    
    book_data = book()
    return render_template('productManager.html',\
                           book_data = book_data,\
                            all_supplier = all_supplier,\
                            user=current_user.name)

def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '商品編號': i[0],
            '商品名稱': i[1],
            '商品售價': i[2],
            '品牌': i[3]
        }
        book_data.append(book)
    return book_data


@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = Product.get_product(pid)

        name = request.values.get('name')
        price = request.values.get('price')
        supplier = request.values.get('supplier')
        description = request.values.get('description')
        file = request.files['file']
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(config(), filename))
        
        pic = pid + filename[filename.index("."):]
        os.chdir(config())
        os.rename(filename, pic)

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        
        Product.add_product(
            {'pid' : pid,
             'pname' : name,
             'price' : price,
             'sname' : supplier,
             'pdesc':description,
             'pimage' : pic
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':

        new_file = request.files['file']
        pid = request.values.get('pid')
        pname = request.values.get('name')
        price = request.values.get('price')
        supplier = request.values.get('supplier')
        description = request.values.get('description')

        if new_file:
            data = Product.get_product(pid)
            image = data[5]
            if image:
                os.remove(os.path.join(config(), image))
            
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(config(), filename))
            pic = pid + filename[filename.index("."):]
            os.chdir(config())
            os.rename(filename, pic)
            
            input = (pname, price, supplier, description, pid)
            Product.update_product(input)
            
            img = (pic, pid)
            Product.update_image(img)
        
        else:
            input = (pname, price, supplier, description, pid)
            Product.update_product(input)
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()

        all_supplier = []
        for i in SUPPLIER.get_all_supplier():
            data = {
                '品牌': i[0],
            }
            all_supplier.append(data)

        return render_template('edit.html', data=product, all_supplier = all_supplier)

def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[2]
    supplier = data[3]
    description = data[4]
    

    s_description = None
    if(SUPPLIER.get_sDesc(supplier) != None):
        s_description = SUPPLIER.get_sDesc(supplier)

    product = {
        '商品編號': pid,
        '商品名稱': pname,
        '單價': price,
        '品牌': supplier,
        '商品敘述': description,
        '品牌敘述': s_description
    }
    return product  

#新增品牌管理
@manager.route('/supplierManager', methods=['GET', 'POST'])
@login_required
def supplierManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        sname = request.values.get('delete')
        data = SUPPLIER.delete_check(sname)
        
        if(data != None):
            flash('failed')
        else:
            SUPPLIER.delete_supplier(sname)
    
    elif 'edit' in request.values:
        sname = request.values.get('edit')
        return redirect(url_for('manager.editSupplier', sname=sname))
    
    supplier_data = supplier()
    return render_template('supplierManager.html', supplier_data = supplier_data, user=current_user.name)

def supplier():
    book_row = SUPPLIER.get_all_supplier()
    book_data = []
    for i in book_row:
        book = {
            '品牌': i[0],
            '品牌敘述': i[1],
        }
        book_data.append(book)
    return book_data

#品牌add
@manager.route('/addSupplier', methods=['GET', 'POST'])
def addSupplier():
    if request.method == 'POST':

        sname = request.values.get('sname')
        sdesc = request.values.get('sdesc')

        if(SUPPLIER.get_sDesc(sname) != None):
            return redirect(url_for('manager.supplierManager'))

        if (len(sname) < 1 or len(sdesc) < 1):
            return redirect(url_for('manager.supplierManager'))
        
        SUPPLIER.add_supplier(
            {'sname' : sname,
             'sdesc' : sdesc,
            }
        )

        return redirect(url_for('manager.supplierManager'))

    return render_template('supplierManager.html')

#品牌edit
@manager.route('/editSupplier', methods=['GET', 'POST'])
@login_required
def editSupplier():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':

        sname = request.values.get('sname')
        sdesc = request.values.get('sdesc')
  
        input = {
            'sname':sname, 
            'sdesc':sdesc
        }
        SUPPLIER.update_supplier(input)
        
        return redirect(url_for('manager.supplierManager'))

    else:
        product = show_supplier_info()
        return render_template('editSupplier.html', data=product)

def show_supplier_info():
    sname = request.args['sname']
    sdesc = SUPPLIER.get_sDesc(sname)[0]

    supplier = {
        '品牌': sname,
        '品牌敘述': sdesc,
    }
    return supplier


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = TRANSACTION.get_order()
        order_data = []
        for i in order_row:
            cid = i[3]
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': CONTAIN.get_total(cid),
                '訂單時間': i[2],
                '付款方式': i[4],
            }
            order_data.append(order)
            
        orderdetail_row = TRANSACTION.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)