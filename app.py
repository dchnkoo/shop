# фреймворк для побудови сайту
from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask.globals import request_ctx


import json

# база данних для роботи з товарами
from cs50 import SQL

# дефолт бібліотеки пайтон
from random import choice
import os

# Ініціалізуємо додаток flask
app = Flask(__name__, )

# під'єднуємо базу данних SQLite
db = SQL('sqlite:///borcivky.db')

# Створюмо курсор для виконання команд SQL
cursor = db


""" ////////////////////////// VARIABLES //////////////////////////////////// """

############### SQL query ################
__sql_query_for_category = "SELECT * FROM borcivkyShop WHERE Категорія=? AND Наявність <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
__sql_query_for_price_range = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
__sql_query_for_all_products = "SELECT * FROM borcivkyShop WHERE Наявність <> 0"
__sql_query_desc_orderById = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Знижка = 0 ORDER BY id DESC"
__sql_query_price_byId = 'SELECT Ціна FROM borcivkyShop WHERE id=?'
__sql_query_update_price2 = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
__sql_query_update_price2_discount = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
__sql_query_to_get_discountsProducts = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Знижка > 0"
__sql_query_select_id = "SELECT * FROM borcivkyShop WHERE id=?"
__sql_query_to_get_minPrice = 'SELECT Ціна2 FROM borcivkyShop WHERE Наявність <> 0 ORDER BY Ціна2 ASC'
__sql_query_to_get_max_price = 'SELECT Ціна2 FROM borcivkyShop WHERE Наявність <> 0 ORDER BY Ціна2 DESC'
__sql_query_select_category = 'SELECT * FROM borcivkyShop WHERE Категорія=?'
__sql_query_get_unik_categories = 'SELECT DISTINCT Категорія FROM borcivkyShop'


"""  ////////////////////// Блок з функціями //////////////////////////////  """




# domain methods
def get_domain():
    ctx = request_ctx
    return ctx.request.host_url

# banner methods
def random_image_for_banner():

    """
    Функція виводить рандомну фотографію на банер
    """

    path  = 'static/banner-image'

    return path + '/' + choice(os.listdir(path=path))







# check methods
def check_for_space(elem):
    """
    Перевіярємо рядок на наявність пробілів
    якщо вони присутні то видаляємо їх
    """
    try:
        name = elem.strip().split(' ')
    except:
        return elem
    else:
        res = ''
        for i in name:
            res += i
         
        return res

def check_for_slash(elem):
    """
    Перевіярємо рядок на наявність '/'
    якщо вони присутні то видаляємо їх
    """
    try:
        name = elem.strip().split('/')
    except:
        return elem
    else:
        res = ''
        for i in name:
            res += i
         
        return res

def check_id_database(id):
    try:
        data_id = int(id)
    except:
        return False
    else:
        if cursor.execute(__sql_query_select_id, data_id):
            return True
        else:
            return False
    

def check_category_database(category):
    if cursor.execute(__sql_query_select_category, category):
        return category
    else:
        return False


def check_photos_for_page(photos: list):
    result = []

    if len(photos) < 2:
        return photos

    for i in range(len(photos)):
        if len(photos[i]) <= 8:
            result.append(photos[i])
        else:
            continue
        
    return result


# get data methods
def get_database_info_of_cards(path, data, category = False, two_image = False):

    """
    Функція звертається до бази данних та повертає
    словник з повною інформацією про товар. 

    Якщо значення category=True то повертається інформація про всі
    товари з певної вказаної категорії в path
    """


    categ = check_for_space(data['Категорія'])
    brand = check_for_space(data['Бренд'])
    model = check_for_space(data['Модель'].strip())
    color = check_for_space(check_for_slash(data['Колір']))
        
            
    if category:
        """
        Отримуємо список всіх фотографії з вказаної
        категорії
        """ 
        if two_image:
            photos = check_photos_for_page(os.listdir(f'{path}/{brand}/{model}{color}'))
        else:
            photos = os.listdir(f'{path}/{brand}/{model}{color}')
    else:
        """
        В іншому випадку перебираємо всі фотографії кожного товару
        з всіх категорій
        """
        if two_image:
            photos = check_photos_for_page(os.listdir(f'{path}/{categ}/{brand}/{model}{color}'))
        else:
            photos = os.listdir(f'{path}/{categ}/{brand}/{model}{color}')

    # Всі папки з фотографіями мають слітні назви без пробілів
    # папка з фотографіями для фото має в назві модель та колір
    name = f"{model}{color}"

                             
    if category:

        # Якщо категорія вказана повертаємо словник з повною інфою
        # бібліотека cs50 одразу повертає нам словник з данними та назвами колонок в базі
        # тому немає необхідності створювати словник того ми просто додаємо до наявного
        # словника list з шляхами до папок з фотографіями

        if data['Знижка'] != 0:

            data['discountPrice'] = data['Ціна'] - calc_discount(data['Знижка'], data['Ціна'])
            update_discount_column_database(data['id'], data['discountPrice'])
            data['Розмір'] = data['Розмір'].split(' ')                         
            data['photos'] = list(map(lambda x: f'{path}/{brand}/{name}/{x}', photos))
            return data
        
        else:

            data['Розмір'] = data['Розмір'].split(' ')                         
            data['photos'] = list(map(lambda x: f'{path}/{brand}/{name}/{x}', photos))
            update_discount_column_database(data['id'], to_old_price=True)
            return data
    else:

        if data['Знижка'] != 0:
            data['discountPrice'] = data['Ціна'] - calc_discount(data['Знижка'], data['Ціна'])
            update_discount_column_database(data['id'], data['discountPrice'])
            data['Розмір'] = data['Розмір'].split(' ')                         
            data['photos'] = list(map(lambda x: f'{path}/{categ}/{brand}/{name}/{x}', photos))
            return data
        

        else:
        # в іншому випадку така сама ситуація але без конкретної категорії

            data['Розмір'] = data['Розмір'].split(' ') 
            data['photos'] = list(map(lambda x: f'{path}/{categ}/{brand}/{name}/{x}', photos))
            update_discount_column_database(data['id'], to_old_price=True)
            return data
    

def getProducts_database(pricemin=None, pricemax=None, category=None, random = 0, limitation=0):
    if category:
        lim = 0

        if random > 0:
            categ = []

            for _ in range(random):
                ch = choice(cursor.execute(__sql_query_for_category, category, pricemin, pricemax))
                if ch not in categ:
                    categ.append(ch)
        else:
            categ = cursor.execute(__sql_query_for_category, category, pricemin, pricemax)
                # Перебираємо по базі данних всі колонки в яких є категеорія яку запитав юзер та наявність == true (тобто 1)


        for i in range(len(categ)):
            if limitation > 0:
                lim += 1

                if lim == limitation:
                    break
                yield get_all_by_category(category, categ[i])
            else:
                yield get_all_by_category(category, categ[i])

    elif pricemin and pricemax:
                # Перебираємо всі товари де наявність = true (тобто 1), та ціна в діапазоні яку вказав юзер
        for_price = cursor.execute(__sql_query_for_price_range, pricemin, pricemax)
        for i in range(len(for_price)):
            yield get_all_by_price(for_price[i])

    else: 
        lim = 0

        if random > 0:
            get_all = []

            for _ in range(random):
                ch = choice(cursor.execute(__sql_query_for_all_products))
                if ch not in get_all:
                    get_all.append(ch)
        else:
            get_all = cursor.execute(__sql_query_for_all_products)

            # Перебираємо всі товари де наявність == true, тобто 1
        for i in range(len(get_all)):
            yield get_all_product(get_all[i])

def get_all_by_category(category, data):
    """
    Функція шукає товари які обрав користувач через фільтр. 
    Пошук приймає назву категорії та діапазон ціни по якому 
    йде пошук.

    Повертає dict
    """         
    
    return get_database_info_of_cards(f'static/images/{category}', data, category=True, two_image=True)

def get_all_by_price(data):
    """
    Якщо користувач робить пошук тільки по діапазону ціни виконується ця функція.
    Приймає тільки мінімальну та максимальну ціну діапазону та перебирає всі категорії.

    Повертає dict.
    """

    return get_database_info_of_cards(f'static/images', data, two_image=True)

def min_price():

    """
    Функція повретає мінімальну ціну з бази даниих
    """

    return cursor.execute(__sql_query_to_get_minPrice)[0]['Ціна2']

def max_price():

    """
    Функція повертає максимальну ціну з бази данних
    """

    return cursor.execute(__sql_query_to_get_max_price)[0]['Ціна2']





# update database methods

def update_discount_column_database(id, price=None, to_old_price=False):
    if to_old_price:
        get_old_price = cursor.execute(__sql_query_price_byId, id)
        cursor.execute(__sql_query_update_price2, get_old_price[0]['Ціна'], id)
    else:
        cursor.execute(__sql_query_update_price2_discount, price, id)









# Page methods
def get_categories():
    return cursor.execute(__sql_query_get_unik_categories)


def newProductsPage():
     for i in cursor.execute(__sql_query_desc_orderById):

                # шлях до папки з категоріями
            yield get_database_info_of_cards('static/images', i, two_image=True)


def get_all_product(data):

    """
    Функція виводить всі товари незалежно від категорії та ціни.
    """
    return get_database_info_of_cards('static/images', data, two_image=True)


def discount():
    for i in cursor.execute(__sql_query_to_get_discountsProducts):

                # шлях до папки з категоріями
        if i['Знижка'] != 0:
            discount = get_database_info_of_cards('static/images', i, two_image=True)
            discount['discountPrice'] = discount['Ціна'] - calc_discount(discount['Знижка'], discount['Ціна'])

            yield discount

def categories_for_footer():

    """
    Виводить категорії для секції футер
    'В нас також можливо придбати'
    """

    categ = []
    path = 'static/images'

    categories = os.listdir(path)


    while len(categ) != 4:
        categories = choice(os.listdir(path))
        if categories not in categ:
            categ.append(categories)
        else:
            continue

        brend = choice(os.listdir(f"{path}/{categories}"))

        product = choice(os.listdir(f"{path}/{categories}/{brend}"))

        img = os.listdir(f"{path}/{categories}/{brend}/{product}")

        for j in range(len(img)):
            if len(img[j][:img[j].index('.')]) <= 3:
                image = img[j]
        yield {'photos': f'{path}/{categories}/{brend}/{product}/{image}', 'category': categories}


def getProduct_for_page(id):

    """
    Коли користувач на сайті натискає на товар то ця функція дістає інфу
    про нього та виводить на окрему сторніку з товаром 'product_page.html'
    """
     
    if product := cursor.execute(__sql_query_select_id, id):

        return get_database_info_of_cards('static/images', product[0])
    
    else: 
        return False



          
# calculate methods
def calc_discount(dscnt, price):
    return int(price * (dscnt / 100)) 

    

""" //////////////////////////////////// Блок з ініціалізацією сторінок html /////////////////////////////////////////// """
# home.html
@app.route('/')
def home_page():
    return render_template('home.html', 
                           get_categories=get_categories,
                           image=random_image_for_banner, 
                           min=min_price,  max=max_price,all_products=getProducts_database,
                           foot_category=categories_for_footer)


# search.html
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        try:
            category = request.args.get('category')
            if category:
                if check_category_database(category) == False:
                    return redirect(get_domain())
                
            price_min = int(request.args.get('price-min'))
            price_max = int(request.args.get('price-max'))
        except:
            return redirect(get_domain())

        else:
            return render_template('search.html',
                                    get_categories=get_categories,
                                    foot_category=categories_for_footer,
                                    image=random_image_for_banner,
                                    min=min_price,  max=max_price,
                                    category=category,
                                    search_filter=getProducts_database(price_min, price_max, category),
                                    price_search=getProducts_database(price_min, price_max))

    else:
        return redirect(get_domain())


# Коли користувач заповнив форму замовлення 
# данні надсилаються сюди
@app.route('/fastOrder', methods=['POST'])
def fastForm():
    if request.method == 'POST':
        name = request.form['name']
        second_name = request.form['second_name']
        phone_number = request.form['phone']
        user_email = request.form['userEmail']
        productId = request.form['productId']

        try:
            if check_id_database(int(productId)):
                print(name, second_name, phone_number, user_email, productId)
                return app.response_class(
                    response=json.dumps({"status":"success","code":200}),
                    status=200,
                    mimetype='application/json'
                )
            else: 
                return app.response_class(
                    response=json.dumps({"status":"Bad Request","code":400}),
                    status=400,
                    mimetype='application/json'
                )
        except:
            return redirect(get_domain())
    else: 
        return redirect(get_domain())


# product_page.html 
@app.route('/ProductPage')
def ProductPage():
    id = request.args.get('id')
    if check_id_database(id) != False:
        prod = getProduct_for_page(id)



        return render_template('product_page.html',  
                            foot_cards=getProducts_database(random=4, limitation=5),
                            min=min_price,  max=max_price,
                            product=prod)
    else:
        return redirect(get_domain())

# new_products.html
@app.route('/newProducts')
def newProducts():
    return render_template('new_products.html',
                            get_categories=get_categories,
                            foot_category=categories_for_footer,
                            min=min_price,  max=max_price, 
                            image=random_image_for_banner,
                            newProductsPage=newProductsPage)

# discountPage.html
@app.route('/discounts')
def dsPAge():
    return render_template('discountPage.html',
                            get_categories=get_categories,
                            foot_category=categories_for_footer,
                            min=min_price,  max=max_price, 
                            image=random_image_for_banner,
                            discount=discount)

@app.route('/infoBuyAndDelivery')
def infoPage():
    return render_template('info.html',
                            min=min_price,  max=max_price)

""" /////////////////////// Якщо дебюжим в цьому документі запускається локальний сервер ////////////////////////// """
if __name__ == '__main__':
    app.run(debug=True, host=('0.0.0.0'), port=80)