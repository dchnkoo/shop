# фреймворк для побудови сайту
from flask import Flask, render_template, request, redirect, current_app
from flask_mail import Mail, Message
from flask.globals import request_ctx
from random import randint
import time

from concurrent.futures import ThreadPoolExecutor

from base_cls import Card, Orders
card = Card()
orders = Orders()

import json

# Ініціалізуємо додаток flask
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dmshop1307@gmail.com'
app.config['MAIL_PASSWORD'] = 'frsu zwst uqxz aotm'

mail = Mail(app)

def send_mail(email, orderid, city, warhouse):
    msg = Message(
        'Дякуємо за замовлення в нашому магазині BORCIVKY UKRAINE!',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email],
    )
    msg.body = f"Ваш номер замовлення {orderid}\nДоставка буде здійснена в місто {city} у {warhouse}.\nМайте гарний настрій! Будемо раді бачити вас знову)"

    mail.send(msg)


oplata_methods = [
    'Накладним платежем',
    'Онлайн оплата через Нову Пошту',
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
                    print(d)
                    orders.insert_order(**d)

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

""" /////////////////////// Якщо дебюжим в цьому документі запускається локальний сервер ////////////////////////// """
if __name__ == '__main__':
    app.run(debug=True, host=('0.0.0.0'), port=80)