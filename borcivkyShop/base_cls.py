# база данних для роботи з товарами
from cs50 import SQL
import numpy as np  

# дефолт бібліотеки пайтон
from random import choice
import os


""" ////////////////////////// VARIABLES //////////////////////////////////// """

############### SQL query ################
_Card__sql_query_for_category = "SELECT * FROM borcivkyShop WHERE Категорія=? AND Наявність <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
_Card__sql_query_for_price_range = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
_Card__sql_query_for_all_products = "SELECT * FROM borcivkyShop WHERE Наявність <> 0"
_Card__sql_query_desc_orderById = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Знижка = 0 ORDER BY id DESC"
_Card__sql_query_price_byId = 'SELECT Ціна FROM borcivkyShop WHERE id=?'
_Card__sql_query_update_price2 = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
_Card__sql_query_update_price2_discount = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
_Card__sql_query_to_get_discountsProducts = "SELECT * FROM borcivkyShop WHERE Наявність <> 0 AND Знижка > 0"
_Card__sql_query_select_id = "SELECT * FROM borcivkyShop WHERE id=?"
_Card__sql_query_to_get_minPrice = 'SELECT Ціна2 FROM borcivkyShop WHERE Наявність <> 0 ORDER BY Ціна2 ASC'
_Card__sql_query_to_get_max_price = 'SELECT Ціна2 FROM borcivkyShop WHERE Наявність <> 0 ORDER BY Ціна2 DESC'
_Card__sql_query_select_category = 'SELECT * FROM borcivkyShop WHERE Категорія=?'
_Card__sql_query_get_unik_categories = 'SELECT DISTINCT Категорія FROM borcivkyShop'

class Card:
    def __init__(self):
        self.__db = SQL('sqlite:///borcivky.db')


    @staticmethod
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
        
    @staticmethod 
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
        
    @staticmethod
    def check_photos_for_page(photos: list):

        if len(photos) < 2:
            return photos
        
        return np.array(photos)[list(map(lambda x: len(x) <= 8, photos))]
    
    @staticmethod
    def random_image_for_banner():

        """
        Функція виводить рандомну фотографію на банер
        """

        path  = 'static/banner-image'

        return path + '/' + choice(os.listdir(path=path))

    def get_database_info_of_cards(self, path, data, category = False, two_image = False):

        categ = self.check_for_space(data['Категорія'])
        brand = self.check_for_space(data['Бренд'])
        model = self.check_for_space(data['Модель'].strip())
        color = self.check_for_space(self.check_for_slash(data['Колір']))
        name = f"{model}{color}"
            
        if data['Знижка'] != 0:
                data['discountPrice'] = data['Ціна'] - self.calc_discount(data['Знижка'], data['Ціна'])
                self.update_discount_column_database(data['id'], data['discountPrice'])       
        else:
            self.update_discount_column_database(data['id'], to_old_price=True)

        if category:
            """
            Отримуємо список всіх фотографії з вказаної
            категорії
            """ 
            if two_image:
                photos = self.check_photos_for_page(os.listdir(f'{path}/{brand}/{model}{color}'))
            else:
                photos = os.listdir(f'{path}/{brand}/{model}{color}')
        else:
            """
            В іншому випадку перебираємо всі фотографії кожного товару
            з всіх категорій
            """
            if two_image:
                photos = self.check_photos_for_page(os.listdir(f'{path}/{categ}/{brand}/{model}{color}'))
            else:
                photos = os.listdir(f'{path}/{categ}/{brand}/{model}{color}')

        if category:

            data['Розмір'] = data['Розмір'].split(' ')                         
            data['photos'] = list(map(lambda x: f'{path}/{brand}/{name}/{x}', photos))
            return data
        
        else:

            data['Розмір'] = data['Розмір'].split(' ') 
            data['photos'] = list(map(lambda x: f'{path}/{categ}/{brand}/{name}/{x}', photos))
            return data


        
    def check_id_database(self, id):

        """
        Перевіряє чи присутній id товару 
        в базі данних
        """

        try:
            id = int(id)
        except:
            return False
        else:
            if self.__db.execute(_Card__sql_query_select_id, id):
                return True
            else:
                return False
            
    def check_category_database(self, category):

        """
        Перевіряє на нявність категорії

        Якщо категорія присутня тоді функція повертає
        назву категорії

        Якщо категорія відсутня return False
        """

        if self.__db.execute(_Card__sql_query_select_category, category):
            return category
        else:
            return False
        

    def get_all_by_category(self, category, data):
        """
        Функція шукає товари які обрав користувач через фільтр. 
        Пошук приймає назву категорії та діапазон ціни по якому 
        йде пошук.

        Повертає dict
        """         
        
        return self.get_database_info_of_cards(f'static/images/{category}', data, category=True, two_image=True)
        
    def get_all_by_price(self, data):
        """
        Якщо користувач робить пошук тільки по діапазону ціни виконується ця функція.
        Приймає тільки мінімальну та максимальну ціну діапазону та перебирає всі категорії.

        Повертає dict.
        """

        return self.get_database_info_of_cards(f'static/images', data, two_image=True)
    

    def min_price(self):

        """
        Функція повретає мінімальну ціну з бази даниих
        """

        return self.__db.execute(_Card__sql_query_to_get_minPrice)[0]['Ціна2']
    
    def max_price(self):

        """
        Функція повертає максимальну ціну з бази данних
        """

        return self.__db.execute(_Card__sql_query_to_get_max_price)[0]['Ціна2']


    def update_discount_column_database(self, id, price=None, to_old_price=False):
        if to_old_price:
            get_old_price = self.__db.execute(_Card__sql_query_price_byId, id)
            self.__db.execute(_Card__sql_query_update_price2, get_old_price[0]['Ціна'], id)
        else:
            self.__db.execute(_Card__sql_query_update_price2_discount, price, id)


    def get_categories(self):
        return self.__db.execute(_Card__sql_query_get_unik_categories)


    def newProductsPage(self):
        for i in self.__db.execute(_Card__sql_query_desc_orderById):

                    # шлях до папки з категоріями
                yield self.get_database_info_of_cards('static/images', i, two_image=True)


    def get_all_product(self, data):

        """
        Функція виводить всі товари незалежно від категорії та ціни.
        """
        return self.get_database_info_of_cards('static/images', data, two_image=True)


    def discount(self):
        for i in self.__db.execute(_Card__sql_query_to_get_discountsProducts):

                    # шлях до папки з категоріями
            if i['Знижка'] != 0:
                discount = self.get_database_info_of_cards('static/images', i, two_image=True)
                discount['discountPrice'] = discount['Ціна'] - self.calc_discount(discount['Знижка'], discount['Ціна'])

                yield discount


    def categories_for_footer(self):

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



    def getProduct_for_page(self, id):

        """
        Коли користувач на сайті натискає на товар то ця функція дістає інфу
        про нього та виводить на окрему сторніку з товаром 'product_page.html'
        """
        
        if product := self.__db.execute(_Card__sql_query_select_id, id):

            return self.get_database_info_of_cards('static/images', product[0])
        
        else: 
            return False


    # calculate methods
    def calc_discount(self, dscnt, price):
        return int(price * (dscnt / 100)) 


    def getProducts_database(self, pricemin=None, pricemax=None, category=None, random = 0, limitation=0):
        if category:
            lim = 0

            if random > 0:
                categ = []

                for _ in range(random):
                    ch = choice(self.__db.execute(_Card__sql_query_for_category, category, pricemin, pricemax))
                    if ch not in categ:
                        categ.append(ch)
            else:
                categ = self.__db.execute(_Card__sql_query_for_category, category, pricemin, pricemax)
                    # Перебираємо по базі данних всі колонки в яких є категеорія яку запитав юзер та наявність == true (тобто 1)


            for i in range(len(categ)):
                if limitation > 0:
                    lim += 1

                    if lim == limitation:
                        break
                    
                yield self.get_all_by_category(category, categ[i])

        elif pricemin and pricemax:
                    # Перебираємо всі товари де наявність = true (тобто 1), та ціна в діапазоні яку вказав юзер
            for_price = self.__db.execute(_Card__sql_query_for_price_range, pricemin, pricemax)
            for i in range(len(for_price)):
                yield self.get_all_by_price(for_price[i])

        else: 
            lim = 0

            if random > 0:
                get_all = []

                for _ in range(random):
                    ch = choice(self.__db.execute(_Card__sql_query_for_all_products))
                    if ch not in get_all:
                        get_all.append(ch)
            else:
                get_all = self.__db.execute(_Card__sql_query_for_all_products)

                # Перебираємо всі товари де наявність == true, тобто 1
            for i in range(len(get_all)):
                yield self.get_all_product(get_all[i])