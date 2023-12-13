import time
import json
import os

import hashlib
import shutil

import socket

import asyncio
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

# фреймворк для побудови сайту
from flask import Flask, render_template, request, redirect, current_app, url_for, jsonify
from flask_mail import Mail, Message
from flask.globals import request_ctx
from random import randint

from concurrent.futures import ThreadPoolExecutor

from base_cls import Card, Orders
from db import PostgreDB

from admin import Admin
adm = Admin()



card = Card()
orders = Orders()
postgre = PostgreDB()



# Ініціалізуємо додаток flask
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dmshop1307@gmail.com'
app.config['MAIL_PASSWORD'] = 'frsu zwst uqxz aotm'

mail = Mail(app)



def send_mail(email, orderid, city, warhouse, recv=False):
    msg = Message(
        'Дякуємо за замовлення в нашому магазині BORCIVKY UKRAINE!',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email],
    )
    
    if recv:
        msg.body = f"Ваш номер замовлення {orderid}\nДоставка буде здійснена в місто {city} у {warhouse}.\n\nРеквізити:\n1. ...\n2. ...\nВ коментарях до оплати вкажіть номера замовлення ваш ПІБ та ваш номер телефону\n\nМайте гарний настрій! Будемо раді бачити вас знову)"
    else:
        msg.body = f"Ваш номер замовлення {orderid}\nДоставка буде здійснена в місто {city} у {warhouse}.\nМайте гарний настрій! Будемо раді бачити вас знову)"

    mail.send(msg)


oplata_methods = [
    'Накладним платежем',
    'Оплата за реквізитами PrivatBank або Monobank',
]



# domain methods
def get_domain():
    ctx = request_ctx
    return ctx.request.host_url

def get_user_IP():
    return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

""" //////////////////////////////////// Блок з ініціалізацією сторінок html /////////////////////////////////////////// """
# home.html
@app.route('/')
def home_page():
    print(get_user_IP())

    d = {
        'get_categories': card.get_categories,
        'get_brands': card.get_brands,
        'min': card.min_price,
        'max': card.max_price,
        'all_products': card.getProducts_database,
        'foot_category': card.categories_for_footer,
    }

    with ThreadPoolExecutor() as executor:

        for n in d.keys():
            d[n] = executor.submit(d[n])

        return render_template('home.html', 
                            get_categories=d['get_categories'].result,
                            min=d['min'].result,  max=d['max'].result, all_products=d['all_products'].result,
                            foot_category=d['foot_category'].result, oplata=oplata_methods, sz=card.get_sizes_for_filter,
                            get_brands=d['get_brands'].result)


# search.html
@app.route('/search', methods=['POST', 'GET'])
def search():
    print(get_user_IP())
    if request.method == 'GET':

        try:
            category = request.args.get('category')
            price_min = int(request.args.get('price-min'))
            price_max = int(request.args.get('price-max'))

            if category or (price_max and price_min):
                try:
                    if category:
                        if card.check_category_database(category) == False:
                            return redirect(get_domain())
                        
                except:
                    return redirect(get_domain())

                else:

                    

                    return render_template('search.html',
                                            get_categories=card.get_categories,
                                            foot_category=card.categories_for_footer,
                                            min=card.min_price,  max=card.max_price,
                                            category=category,
                                            search_filter=card.getProducts_database(price_min, price_max, category),
                                            price_search=card.getProducts_database(price_min, price_max),
                                            oplata=oplata_methods, sz=card.get_sizes_for_filter, get_brands=card.get_brands)

        except:
            size = request.args.get('size')
            
            if size:
                return render_template('search.html', price_search=card.get_by_size(size),
                                   get_categories=card.get_categories,
                                    foot_category=card.categories_for_footer,
                                    min=card.min_price,  max=card.max_price, category=category,
                                    oplata=oplata_methods, sz=card.get_sizes_for_filter, get_brands=card.get_brands)
            

            else:
                brand = request.args.get('brand')
                
                return render_template('search.html', price_search=card.get_by_brand(brand),
                                   get_categories=card.get_categories,
                                    foot_category=card.categories_for_footer,
                                    min=card.min_price,  max=card.max_price, category=category,
                                    oplata=oplata_methods, sz=card.get_sizes_for_filter, get_brands=card.get_brands)


    else:
        return redirect(get_domain())



@app.route('/sort')
def sort():
    sort = request.args.get('by')
    if request.args.get('category'):
        categ = request.args.get('category')

        return render_template('sort.html', get_sort=card.get_sort_products(sort, categ),
                                get_categories=card.get_categories,
                                foot_category=card.categories_for_footer,
                                min=card.min_price,  max=card.max_price, 
                                oplata=oplata_methods, sort=sort, sz=card.get_sizes_for_filter, get_brands=card.get_brands)
    else:
        return render_template('sort.html', get_sort=card.get_sort_products(sort),
                                get_categories=card.get_categories,
                                foot_category=card.categories_for_footer,
                                min=card.min_price,  max=card.max_price, 
                                oplata=oplata_methods, sort=sort, sz=card.get_sizes_for_filter, get_brands=card.get_brands)




# Коли користувач заповнив форму замовлення 
# данні надсилаються сюди
@app.route('/fastOrder', methods=['POST'])
def fastForm():
        datas = json.loads(request.form['data'])

        try:
            for d in datas:
                if not card.check_id_database(int(d['idProduct'])):
                    return app.response_class(
                        response=json.dumps({"status":"Bad Request","code":400}),
                        status=400,
                        mimetype='application/json')
                else:
                    orderId = randint(1_000_000, 9_000_000)
                    d['orderId'] = orderId
                    d['time'] = time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time())) 
                    orders.insert_order(**d)

                    if d['opls'] == 'Оплата за реквізитами PrivatBank або Monobank':
                        send_mail(d['userEmail'], d['orderId'], d['City'], d['vidil'], recv=True)
                    else: 
                        send_mail(d['userEmail'], d['orderId'], d['City'], d['vidil'])
                
        except:
            return app.response_class(
                        response=json.dumps({"status":"Bad Request","code":400}),
                        status=400,
                        mimetype='application/json')
        else:   
        
            return app.response_class(
                response=json.dumps({"status":"success","code":200}),
                status=200,
                mimetype='application/json'
            )


# product_page.html 
@app.route('/ProductPage')
def ProductPage():
    print(get_user_IP())
    id = request.args.get('id')
    if card.check_id_database(id) != False:
        prod = card.getProduct_for_page(id)

        return render_template('product_page.html',  
                            foot_cards=card.getProducts_database(random=4, limitation=5),
                            min=card.min_price,  max=card.max_price,
                            product=prod, oplata=oplata_methods, get_brands=card.get_brands)
    else:
        return redirect(get_domain())

# new_products.html
@app.route('/newProducts')
def newProducts():
    print(get_user_IP())
    return render_template('new_products.html',
                            get_categories=card.get_categories,
                            foot_category=card.categories_for_footer,
                            min=card.min_price,  max=card.max_price, 
                            newProductsPage=card.newProductsPage,
                            oplata=oplata_methods, sz=card.get_sizes_for_filter, get_brands=card.get_brands)

# discountPage.html
@app.route('/discounts')
def dsPAge():
    print(get_user_IP())
    return render_template('discountPage.html',
                            get_categories=card.get_categories,
                            foot_category=card.categories_for_footer,
                            min=card.min_price,  max=card.max_price, 
                            discount=card.discount,
                            oplata=oplata_methods, sz=card.get_sizes_for_filter, get_brands=card.get_brands)

@app.route('/infoBuyAndDelivery')
def infoPage():
    print(get_user_IP())
    return render_template('info.html',
                            min=card.min_price,  max=card.max_price, oplata=oplata_methods)


@app.route('/admin')
def admin():
    return render_template('log_admin.html')


@app.route('/get', methods=['POST'])
def gte():
    try:

        data = json.loads(request.data.decode())

        d = list(filter(lambda x: card.check_id_database(x['idProduct']) , data))

        return app.response_class(
            response=json.dumps({'status' : 200, 'data' : d})
        )
    except:
        return app.response_class(
            response=json.dumps({'status' : 400, 'data' : 'trash empty'})
        )



ad = {}
@app.route('/admin/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))

        m = hashlib.sha256()
        m.update(data['pass'].encode('UTF-8'))

        l = hashlib.sha256()
        l.update(data['login'].encode('UTF-8'))

        if l.hexdigest() == '2fdc664fe50c6388a49920da198599346e837e92d85d99f52690230da43db29a':
            if m.hexdigest() == '97d82ff4ea08e1cfe6c841c1e32fa4798f12c970cbfb0e80d1e79776b71f8d6d':
                adminp = hashlib.sha256()
                adminp.update(f'{get_user_IP()}{randint(1,100)}'.encode('UTF-8'))

                ad[get_user_IP()] = adminp.hexdigest()
                url_for('panel', key=ad[get_user_IP()])
                
                return app.response_class(
                    response=json.dumps({'url' : get_domain()+f'admin/{ad[get_user_IP()]}/panel', 'code': 200}),
                    status=200,
                    mimetype='application/json'
                ) 
            
            else:
                return app.response_class(
                    response=json.dumps({"status":"Bad Request","code":400}),
                    status=400,
                    mimetype='application/json'
                )
        else:
            return app.response_class(
                    response=json.dumps({"status":"Bad Request","code":400}),
                    status=400,
                    mimetype='application/json'
                )
    else:
        return redirect(get_domain() + 'admin')
    


@app.route(f'/admin/<key>/panel')
def panel(key):
    try:
        if key == ad[get_user_IP()]:
            url_for('product_admin', key=key)
            url_for('change', key=key)
            return render_template('panel.html',
                                    all=card.get_all, 
                                    orders=orders.get_orders,
                                    categories=card.get_categories, brands=card.get_brands,
                                    ips=ad, cur_user=get_user_IP())
        else:
            return redirect(get_domain() + 'admin')
    except:
        return redirect(get_domain() + 'admin')



@app.route('/admin/<key>/panel/product')
def product_admin(key):
    try:
        if key == ad[get_user_IP()]:
            prod=card.getProduct_for_page(int(request.args.get('id')))

            sizes = ''

            for i in prod['Розмір']:
                sizes += f'{i} '


            return render_template('product_ad.html', prod=prod, 
                                   categories=card.get_categories, brands=card.get_brands, size=sizes)
        else:
            return redirect(get_domain() + 'admin')
    except:
        return redirect(get_domain() + 'admin')



@app.route('/admin/<key>/panel/change', methods=['POST', 'DELETE', 'PATCH', 'PUT'])
def change(key):

    match request.method:

        case 'POST':

            try:
                data = json.loads(request.data.decode())

                match data['type']:
                    
                    case 'Кількість':
                        try:
                            much = adm.change_much_value(int(data['id']), int(data['value']))
                            match much['status']:
                                case True:
                                    
                                    return app.response_class(
                                        response=json.dumps({'code' : 200, 'msg' : much['msg'], 'id' : data['id']}),
                                        status=200,
                                        mimetype='application/json')
                                
                                case False:
                                    return app.response_class(
                                        response=json.dumps({'code' : 400, 'msg' : 'Значення кількості повинно бути більше нуля', 'id' : data['id']}),
                                        status=400,
                                        mimetype='application/json')

                        except:
                            return app.response_class(
                                response=json.dumps({'code' : 400, 'msg' : 'Значення кількості повинно бути числом', 'id' : data['id']}),
                                status=400,
                            mimetype='application/json')


                    case 'Знижка':
                        try:
                            dicsount = adm.change_discount_value(int(data['id']), int(data['value']))
                            match dicsount:

                                case True:
                                    
                        
                                    return app.response_class(
                                        response=json.dumps({'code' : 200, 'msg' : 'SUCCESS'}),
                                        status=200,
                                        mimetype='application/json')
                            
                                case False:
                                    return app.response_class(
                                        response=json.dumps({'code' : 400, 'msg' : 'Значення знижки повинно бути в діапазоні від 0 до 100', 'id' : data['id']}),
                                        status=400,
                                        mimetype='application/json')

                        except:
                            return app.response_class(
                                response=json.dumps({'code' : 400, 'msg' : 'Значення знижки повинно бути числом без спеціальних символів', 'id' : data['id']}),
                                    status=400,
                                    mimetype='application/json')

                    case 'Ціна2':
                        try:
                            price = adm.change_price_value(int(data['id']), int(data['value']))
                            match price:
                                case True:
                                    
                        
                                    return app.response_class(
                                    response=json.dumps({'code' : 200, 'msg' : 'SUCCESS'}),
                                        status=200,
                                        mimetype='application/json')

                                case False:
                                    return app.response_class(
                                    response=json.dumps({'code' : 400, 'msg' : 'Ціна товару не може бути змінена поки на нього діє знижка або не може бути змінена на число менше 0', 'id' : data['id']}),
                                        status=400,
                                        mimetype='application/json')
                        except:
                            return app.response_class(
                                    response=json.dumps({'code' : 400, 'msg' : 'Ціна товару не має містити спеціальних символів', 'id' : data['id']}),
                                        status=400,
                                        mimetype='application/json')
                        

                    case 'load_data_to_site':
                        
                        try:

                            db = postgre._connect_to_db()
                            cur = db.cursor()

                            load = asyncio.run(postgre.execute_load(db, cur))

                            cur.close()
                            db.close()
                            
                            if load:
                                return jsonify({'status': 200, 'load': True})
                            else:
                                return jsonify({'status': 400, 'load': False})
                            
                        except Exception as e:
                            return jsonify({'status': 400, 'load': e})
                    

                    case 'load_data':

                        try:
                            db = postgre._connect_to_db()
                            cur = db.cursor()

                            load_to = asyncio.run(postgre.execute_upload(db, cur))

                            cur.close()
                            db.close()

                            if load_to:
                                return jsonify({'status': 200, 'load': True})
                            else:
                                return jsonify({'status': 400, 'load': False})

                        except Exception as e:
                            return jsonify({'status': 400, 'load': e})



                    case 'exit':

                        try:
                            del ad[data['ip']]

                            return jsonify({'status': 200})
                        
                        except Exception as e:
                            print(e)

                            return jsonify({'status': 400, 'msg': e})


                    case _:
                        return app.response_class(
                            response=json.dumps({'code' : 400, 'msg' : 'BAD REQUEST'}),
                            status=400,
                            mimetype='application/json')
            except:

                fil = request.files
                inf = json.loads(request.form['data'])

                path = adm.create_path_if_not_exists(adm.get_path(category=inf['category'], brand=inf['brand'], model=inf['model'], color=inf['color']))
                if path:
                    print(fil)
                    for i in fil:
                        match i:
                            case 'file0':
                                fil[i].save(path + '/' + fil[i].filename)
                                
                                os.rename(f'{path}/{fil[i].filename}', f'{path}/tit{adm.return_format_photo(fil[i].filename)}')
                            case 'file1':
                                fil[i].save(path + '/' + fil[i].filename)
                                
                                os.rename(f'{path}/{fil[i].filename}', f'{path}/stit{adm.return_format_photo(fil[i].filename)}')
                            case _:
                                fil[i].save(path + '/' + fil[i].filename)

                    try: 
                        if adm.insert_product_info(**inf):
                            
                
                            return app.response_class(
                                response=json.dumps({'code': 200, 'msg': 'PRODUCT SUCCES ADDED'}),
                                status=200,
                                mimetype='application/json'
                            )
                        
                        else:
                            shutil.rmtree(path)
                            return app.response_class(
                                response=json.dumps({'code': 400, 'msg': 'PRODUCT FAIL ADDED'}),
                                status=400,
                                mimetype='application/json'
                            )
                    except Exception as e:
                        shutil.rmtree(path)
                        return app.response_class(
                                response=json.dumps({'code': 400, 'msg': e}),
                                status=400,
                                mimetype='application/json'
                            )

                    
                else:

                    return app.response_class(
                        response=json.dumps({'code': 500, 'msg': 'PRODUCT FAIL ADDED ON SERVER'}),
                        status=500,
                        mimetype='application/json'
                    )
                            
                

                

                

        case "DELETE":
            
            dele = json.loads(request.data.decode())
            get = card.getProduct_for_page(int(dele['id']))
            
            if get:
                delete = adm.delete_product(get)

                match delete:
                    case True:
                        
            
                        return app.response_class(
                            response=json.dumps({'code' : 200, 'msg' : 'DELETE SUCCES'}),
                            status=200,
                            mimetype='application/json'
                        )
                    case _:
                        return app.response_class(
                            response=json.dumps({'code' : 400, 'msg' : delete}),
                            status=400,
                            mimetype='application/json'
                        )
            else:
                
    
                return app.response_class(
                            response=json.dumps({'code' : 200, 'msg' : 'DELETE SUCCES'}),
                            status=200,
                            mimetype='application/json')

        
        case 'PATCH':

            patch = json.loads(request.data.decode())
            try:
                if adm.done(int(patch['orderId'])):
                    
        
                    return app.response_class(
                            response=json.dumps({'code' : 200, 'msg' : 'SUCCESS PATCH'}),
                            status=200,
                            mimetype='application/json'
                        )
                else:
                    return app.response_class(
                            response=json.dumps({'code' : 400, 'msg' : 'FAIL PATCH'}),
                            status=400,
                            mimetype='application/json'
                        )
            except:
                return app.response_class(
                            response=json.dumps({'code' : 400, 'msg' : 'FAIL PATCH'}),
                            status=400,
                            mimetype='application/json'
                        )
        

        case 'PUT':
            
            try:
                put = json.loads(request.data.decode())
                
                try:
                    match put["method"]:
                        case 'del_img':
                            if adm.del_img(put["path_img"], put["img_name"]):
                                
                    
                                return app.response_class(
                                    response=json.dumps({'code': 200, 'msg' : 'success'})
                                )
                            
                            else:

                                return app.response_class(

                                    response=json.dumps({'code': 400, 'msg': 'Видалення не було виконано'})
                                )
                            
                        case 'set_first':
                            if adm.set_first(put["path_img"], put["img_name"]):
                                
                    
                                return app.response_class(
                                    response=json.dumps({'code': 200, 'msg' : 'success'})
                                )

                            else:
                                return app.response_class(

                                    response=json.dumps({'code': 400, 'msg': 'Дію не було виконано'})
                                )
                        
                        case 'set_sec':
                            if adm.set_sec(put["path_img"], put["img_name"]):
                                
                    
                                return app.response_class(
                                    response=json.dumps({'code': 200, 'msg' : 'success'})
                                )

                            else:
                                return app.response_class(
                                  response=json.dumps({'code': 400, 'msg': 'Дію не було виконано'})
                                )
                except Exception as e:

                    return app.response_class(
                        resopnse=json.dumps({'code': 400, 'msg': e})
                        )



            except json.decoder.JSONDecodeError:

                f = request.files
                d = json.loads(request.form['data'])


                i = card.getProduct_for_page(int(d['id']))
                pr = os.path.abspath(adm.get_path(category=i['Категорія'], brand=i['Бренд'], model=i['Модель'], color=i['Колір']))

                p = adm.create_path_if_not_exists(adm.get_path(category=d['category'], brand=d['brand'], model=d['model'], color=d['color']))

                if pr != p.replace('/', '\\'):
                    try:
                        for i in os.listdir(pr):
                            shutil.copyfile(pr + '/' + i, p + '/' + i)

                        shutil.rmtree(pr)

                    except shutil.SameFileError as e:
                        with open('logs.txt', 'a+') as y:
                            y.write(f'IT"S same file {e.filename} - {e.filename2}')

                
                if list(f.to_dict()):


                    folder = os.listdir(p)
                    if len(folder) == 4 or (len(folder) + len(f)) > 4:
                        return app.response_class(response=json.dumps({'code': 400, 'msg': 'Неможливо додати більше 4 фото'}))


                    title1 = [i for i in folder if len(i) == min([len(j) for j in folder])]
                    stitle2 = [i for i in folder if len(i) == (min([len(j) for j in folder]) + 1)]
                    
                    if title1 and stitle2:
                        for i in f:
                            f[i].save(p + '/' + f[i].filename)
                        

                    elif title1 and not stitle2:
                        
                        stit = f[list(f.keys())[0]]

                        stit.save(p + '/' + stit.filename)

                        os.rename(p + '/' + stit.filename, p + '/' f'stit{adm.return_format_photo(stit.filename)}')

                        if len(f) > 1:
                            for i in range(1, len(f)):

                                f[list(f.keys())[i]].save(p + '/' + f[list(f.keys())[i]].filename)

                if adm.update_all(**d):
                    
        
                    return app.response_class(
                        response=json.dumps({'code' : 200, 'msg' : 'CHANGES SUCCESS'}),
                        status=200,
                        mimetype='application/json')
                
                else: 
                    return app.response_class(
                        response=json.dumps({'code' : 400, 'msg' : 'CHANGES FAILED'}),
                        status=400,
                        mimetype='application/json')



        case _:
            return app.response_class(
                response=json.dumps({'code' : 500, 'msg' : 'Internal Server Error'}),
                status=500,
                mimetype='application/json')



""" /////////////////////// Якщо дебюжим в цьому документі запускається локальний сервер ////////////////////////// """
def find_free_port():

    loacal_ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]

    return {'port': int(os.environ.get("PORT", 50000)), 'ips': loacal_ips}

if __name__ == '__main__':
    port = find_free_port()

    http_server = WSGIServer((port['ips'][0], port['port']), app, handler_class=WebSocketHandler)
    print(f"Server runnig on http://{port['ips'][0]}:{port['port']}")


    load = card.get_load_status()

    if load:
        db = postgre._connect_to_db()
        cur = db.cursor()

        asyncio.run(postgre.execute_load(db, cur))

        cur.close()
        db.close()
        card.set_load_status(0)


    http_server.serve_forever()