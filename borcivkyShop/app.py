import time
import json
import os

import hashlib
import shutil


# фреймворк для побудови сайту
from flask import Flask, render_template, request, redirect, current_app, url_for
from flask_mail import Mail, Message
from flask.globals import request_ctx
from random import randint

from concurrent.futures import ThreadPoolExecutor

from base_cls import Card, Orders
card = Card()
orders = Orders()

from admin import Admin
adm = Admin()


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
        'image': card.random_image_for_banner,
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
                            image=d['image'].result, 
                            min=d['min'].result,  max=d['max'].result, all_products=d['all_products'].result,
                            foot_category=d['foot_category'].result, oplata=oplata_methods)


# search.html
@app.route('/search', methods=['POST', 'GET'])
def search():
    print(get_user_IP())
    if request.method == 'GET':
        try:
            category = request.args.get('category')
            if category:
                if card.check_category_database(category) == False:
                    return redirect(get_domain())
                
            price_min = int(request.args.get('price-min'))
            price_max = int(request.args.get('price-max'))
        except:
            return redirect(get_domain())

        else:

            

            return render_template('search.html',
                                    get_categories=card.get_categories,
                                    foot_category=card.categories_for_footer,
                                    image=card.random_image_for_banner,
                                    min=card.min_price,  max=card.max_price,
                                    category=category,
                                    search_filter=card.getProducts_database(price_min, price_max, category),
                                    price_search=card.getProducts_database(price_min, price_max),
                                    oplata=oplata_methods)

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
                                image=card.random_image_for_banner,
                                oplata=oplata_methods, sort=sort)
    else:
        return render_template('sort.html', get_sort=card.get_sort_products(sort),
                                get_categories=card.get_categories,
                                foot_category=card.categories_for_footer,
                                min=card.min_price,  max=card.max_price, 
                                image=card.random_image_for_banner,
                                oplata=oplata_methods, sort=sort)




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
                            product=prod, oplata=oplata_methods)
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
                            image=card.random_image_for_banner,
                            newProductsPage=card.newProductsPage,
                            oplata=oplata_methods)

# discountPage.html
@app.route('/discounts')
def dsPAge():
    print(get_user_IP())
    return render_template('discountPage.html',
                            get_categories=card.get_categories,
                            foot_category=card.categories_for_footer,
                            min=card.min_price,  max=card.max_price, 
                            image=card.random_image_for_banner,
                            discount=card.discount,
                            oplata=oplata_methods)

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
                                    categories=card.get_categories, brands=card.get_brands)
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
                            match much:
                                case True:
                                    return app.response_class(
                                        response=json.dumps({'code' : 200, 'msg' : 'SUCCESS', 'id' : data['id']}),
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
                    case _:
                        return app.response_class(
                            response=json.dumps({'code' : 400, 'msg' : 'BAD REQUEST'}),
                            status=400,
                            mimetype='application/json')
            except:

                data = request.files
                inf = json.loads(request.form['data'])

                path = adm.create_path_if_not_exists(adm.get_path(category=inf['category'], brand=inf['brand'], model=inf['model'], color=inf['color']))
                if path:
                    print(data)
                    for i in data:
                        match i:
                            case 'file0':
                                data[i].save(path + '/' + data[i].filename)
                                
                                os.rename(f'{path}/{data[i].filename}', f'{path}/tit{adm.return_format_photo(data[i].filename)}')
                            case 'file1':
                                data[i].save(path + '/' + data[i].filename)
                                
                                os.rename(f'{path}/{data[i].filename}', f'{path}/stit{adm.return_format_photo(data[i].filename)}')
                            case _:
                                data[i].save(path + '/' + data[i].filename)

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
                    
                else:

                    return app.response_class(
                        response=json.dumps({'code': 500, 'msg': 'PRODUCT FAIL ADDED ON SERVER'}),
                        status=500,
                        mimetype='application/json'
                    )
                            
                

                

                

        case "DELETE":
            
            data = json.loads(request.data.decode())
            get = card.getProduct_for_page(int(data['id']))
            
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

            data = json.loads(request.data.decode())
            try:
                if adm.done(int(data['orderId'])):
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
            

        case _:
            return app.response_class(
                response=json.dumps({'code' : 500, 'msg' : 'Internal Server Error'}),
                status=500,
                mimetype='application/json')


""" /////////////////////// Якщо дебюжим в цьому документі запускається локальний сервер ////////////////////////// """
if __name__ == '__main__':
    app.run(debug=True, host=('0.0.0.0'), port=8000)