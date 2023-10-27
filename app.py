# фреймворк для побудови сайту
from flask import Flask, render_template, request, redirect
from flask.globals import request_ctx

from base_cls import Card
card = Card()

import json

# Ініціалізуємо додаток flask
app = Flask(__name__, )

# domain methods
def get_domain():
    ctx = request_ctx
    return ctx.request.host_url


""" //////////////////////////////////// Блок з ініціалізацією сторінок html /////////////////////////////////////////// """
# home.html
@app.route('/')
def home_page():
    return render_template('home.html', 
                           get_categories=card.get_categories,
                           image=card.random_image_for_banner, 
                           min=card.min_price,  max=card.max_price,all_products=card.getProducts_database,
                           foot_category=card.categories_for_footer)


# search.html
@app.route('/search', methods=['POST', 'GET'])
def search():
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
                                    price_search=card.getProducts_database(price_min, price_max))

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
            if card.check_id_database(int(productId)):
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
    if card.check_id_database(id) != False:
        prod = card.getProduct_for_page(id)



        return render_template('product_page.html',  
                            foot_cards=card.getProducts_database(random=4, limitation=5),
                            min=card.min_price,  max=card.max_price,
                            product=prod)
    else:
        return redirect(get_domain())

# new_products.html
@app.route('/newProducts')
def newProducts():
    return render_template('new_products.html',
                            get_categories=card.get_categories,
                            foot_category=card.categories_for_footer,
                            min=card.min_price,  max=card.max_price, 
                            image=card.random_image_for_banner,
                            newProductsPage=card.newProductsPage)

# discountPage.html
@app.route('/discounts')
def dsPAge():
    return render_template('discountPage.html',
                            get_categories=card.get_categories,
                            foot_category=card.categories_for_footer,
                            min=card.min_price,  max=card.max_price, 
                            image=card.random_image_for_banner,
                            discount=card.discount)

@app.route('/infoBuyAndDelivery')
def infoPage():
    return render_template('info.html',
                            min=card.min_price,  max=card.max_price)

""" /////////////////////// Якщо дебюжим в цьому документі запускається локальний сервер ////////////////////////// """
if __name__ == '__main__':
    app.run(debug=True, host=('0.0.0.0'), port=80)