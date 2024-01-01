# база данних для роботи з товарами
from dotenv import load_dotenv
import numpy as np 
from cs50 import SQL 


import threading

# дефолт бібліотеки пайтон
from random import choice
import os

""" ////////////////////////// VARIABLES //////////////////////////////////// """

############### SQL query ################
_Card__sql_query_for_category = "SELECT * FROM borcivkyShop WHERE Категорія=? AND Кількість <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
_Card__sql_query_for_price_range = "SELECT * FROM borcivkyShop WHERE Кількість <> 0 AND Ціна2 >= ? AND Ціна2 <= ?"
_Card__sql_query_for_all_products = "SELECT * FROM borcivkyShop WHERE Кількість <> 0"
_Card__sql_query_desc_orderById = "SELECT * FROM borcivkyShop WHERE Кількість <> 0 AND Знижка = 0 ORDER BY id DESC"
_Card__sql_query_price_byId = 'SELECT Ціна FROM borcivkyShop WHERE id=?'
_Card__sql_query_update_price2 = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
_Card__sql_query_update_price2_discount = 'UPDATE borcivkyShop SET Ціна2=? WHERE id=?'
_Card__sql_query_to_get_discountsProducts = "SELECT * FROM borcivkyShop WHERE Кількість <> 0 AND Знижка > 0"
_Card__sql_query_select_id = "SELECT * FROM borcivkyShop WHERE id=?"
_Card__sql_query_to_get_minPrice = 'SELECT Ціна2 FROM borcivkyShop WHERE Кількість <> 0 ORDER BY Ціна2 ASC'
_Card__sql_query_to_get_max_price = 'SELECT Ціна2 FROM borcivkyShop WHERE Кількість <> 0 ORDER BY Ціна2 DESC'
_Card__sql_query_select_category = 'SELECT * FROM borcivkyShop WHERE Категорія=?'
_Card__sql_query_get_unik_categories = 'SELECT DISTINCT Категорія FROM borcivkyShop'
_Card__sql_query_get_unik_brands = 'SELECT DISTINCT Бренд FROM borcivkyShop'
_Card__sql_query_get_by_brand = 'SELECT * FROM borcivkyShop WHERE Бренд=?'



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
    
    
    def get_database_info_of_cards(self, path, data, category = False, two_image = False):

        forCheck = {'categ': data['Категорія'], 'brand': data['Бренд'], 'model': data['Модель'].strip(), 'color': data['Колір']}
        checker = threading.BoundedSemaphore(value=5)
        for n in forCheck.keys():
            checker.acquire()
            forCheck[n] = self.check_for_space(self.check_for_slash(forCheck[n]))
            checker.release()

        name = f"{forCheck['model']}{forCheck['color']}"
            
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
                photos = self.check_photos_for_page(os.listdir(f'{path}/{forCheck['brand']}/{forCheck['model']}{forCheck['color']}'))
            else:
                photos = os.listdir(f'{path}/{forCheck['brand']}/{forCheck['model']}{forCheck['color']}')
        
        else:
            """
            В іншому випадку перебираємо всі фотографії кожного товару
            з всіх категорій
            """
            if two_image:
                photos = self.check_photos_for_page(os.listdir(f'{path}/{forCheck['categ']}/{forCheck['brand']}/{forCheck['model']}{forCheck['color']}'))
            else:
                photos = os.listdir(f'{path}/{forCheck['categ']}/{forCheck['brand']}/{forCheck['model']}{forCheck['color']}')

        if category:


            data['Розмір'] = data['Розмір'].split(' ')   
            data['photos'] = [(len(i), f'{path}/{forCheck['brand']}/{name}/{i}') for i in photos]
            return data
        
        else:

            data['Розмір'] = data['Розмір'].split(' ') 
            data['photos'] = [(len(i), f'{path}/{forCheck['categ']}/{forCheck['brand']}/{name}/{i}') for i in photos]

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
        
        return self.get_database_info_of_cards(f'static/images/{self.check_for_space(self.check_for_slash(category))}', data, category=True, two_image=True)
        
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
    
    def get_brands(self):
        return self.__db.execute(_Card__sql_query_get_unik_brands)


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

        c = self.get_categories()
        cl = [j['Категорія'] for j in c]

        while len(categ) != 4:
            cc = choice(cl)
            ccp = self.check_for_space(self.check_for_slash(cc))
            categories = choice(os.listdir(path + '/' + ccp))
            if cc not in categ:
                categ.append(cc)
            else:
                continue
            
            try:
                brend = choice(os.listdir(f"{path}/{ccp}/{categories}"))
            except:
                continue

            photos_list = os.listdir(f"{path}/{ccp}/{categories}/{brend}")

            if len(photos_list) < 1:
                continue

            img = [i for i in photos_list if len(i) == min([len(j) for j in photos_list])][0]


            yield {'photos': f'{path}/{ccp}/{categories}/{brend}/{img}', 'category': cc}



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
    
    def get_sort_products(self, sort, category=None):
        if category:
            if sort == 'max-sort':
                query = 'SELECT * FROM borcivkyShop WHERE Категорія=? AND Кількість <> 0 ORDER BY Ціна2 DESC'
            elif sort == 'min-sort':
                query = 'SELECT * FROM borcivkyShop WHERE Категорія=? AND Кількість <> 0 ORDER BY Ціна2 ASC'
            else:
                return False

            for i in self.__db.execute(query, category):
                yield self.get_all_by_category(category, i)

        else:
            if sort == 'max-sort':
                query = 'SELECT * FROM borcivkyShop WHERE Кількість <> 0 ORDER BY Ціна2 DESC'
            elif sort == 'min-sort':
                query = 'SELECT * FROM borcivkyShop WHERE Кількість <> 0 ORDER BY Ціна2 ASC'
            else:
                return False
            
            for i in self.__db.execute(query):
                yield self.get_all_product(i)

    def get_all(self):
        query = self.__db.execute('SELECT * FROM borcivkyShop')
        for i in range(len(query)):
            yield self.get_all_product(query[i])



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

    @staticmethod
    def is_float(str: str) -> bool:
        try:
            float(str)

            return True
        
        except ValueError as e:
            return False
        
    @staticmethod
    def convert_fn(arr: list) -> list:
        l = []

        for i in range(len(arr)):

            try:
                l.append(int(arr[i]))
            except ValueError:
                l.append(float(arr[i]))

        return sorted(l)

    @staticmethod
    def allnum_sort(arr: list) -> list:
        s = []

        while len(arr):
            r = [i for i in arr if len(i) == min([len(j) for j in arr])][0]
            ind = arr.index(r)

            s.append(r)
            del arr[ind]


        return s

    def get_sizes_for_filter(self) -> dict[list]:
        sizes = {'digits': [], 'string': [], 'another': []}

        get = self.__db.execute("SELECT Розмір FROM borcivkyShop")
        arr = [i['Розмір'].split() for i in get]

        for array in range(len(arr)):
            for i in range(len(arr[array])):
                cur = arr[array][i]

                if cur not in sizes['digits'] and (cur.isdigit() or self.is_float(cur)):
                    sizes['digits'].append(cur)
                    continue

                elif cur not in sizes['string'] and (cur.isalpha() or (cur[:1].isdigit() and cur[1:].isalpha())):
                    sizes['string'].append(cur)
                    continue

        sizes['digits'] = self.convert_fn(sizes['digits'])
        sizes['string'] = self.allnum_sort(sizes['string'])
        
        return sizes
    
    def get_by_size(self, size: str) -> dict:

        for i in self.__db.execute(_Card__sql_query_for_all_products):
            if size in i['Розмір'].split():
                yield self.get_all_product(i)


    def get_by_brand(self, brand: str) -> dict:

        for i in self.__db.execute(_Card__sql_query_get_by_brand, brand):
            yield self.get_all_product(i)

    def _get_all(self):
        for x in self.__db.execute("SELECT * FROM borcivkyShop"):
            yield self.get_database_info_of_cards('static/images', x)

    def get_load_status(self) -> int:
        return int(self.__db.execute("SELECT status FROM load")[0]['status'])
    
    def set_load_status(self, status) -> bool:
        if self.__db.execute('UPDATE load SET status=?', status):
            return True
        else: return False


    async def _create_products_table(self):

        try:
            self.__db.execute("""CREATE TABLE IF NOT EXISTS borcivkyShop(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Категорія TEXT NOT NULL,
                    Бренд TEXT NOT NULL,
                    Модель TEXT NOT NULL,
                    Колір TEXT NOT NULL,
                    Ціна INTEGER NOT NULL,
                    Ціна2 INTEGER,
                    Розмір TEXT NOT NULL, 
                    Кількість INTEGER NOT NULL,
                    Артикул INTEGER UNIQUE NOT NULL,
                    Опис TEXT,
                    Знижка INTEGER NOT NULL DEFAULT 0
            )""")
        
        except Exception as e:
            print(f"ERROR IN base_cls.py IN CREATE PRODUCTS TABLE: {e}")
            return False
        
        else:
            return True
        

insert_order_information = 'INSERT INTO orders(orderId, orderProductId, ordersize, Name, SecondName, phone, Email,city,Warhouse,Pay,date,count,done) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'



class Orders(Card):

    def __init__(self):
        super().__init__()
        self._db = SQL('sqlite:///borcivky.db')


    async def _create_orders_table(self):

        try:
            self._db.execute("""CREATE TABLE IF NOT EXISTS orders(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            orderId INTEGER NOT NULL,
                            orderProductId INTEGER,
                            orderSize TEXT,
                            Name TEXT,
                            SecondName TEXT,
                            phone TEXT,
                            Email TEXT,
                            city TEXT,
                            Warhouse TEXT,
                            Pay TEXT,
                            date DATETIME,
                            count INTEGER,
                            done BOOL
            );""")

        except Exception as e:
            print(f"ERROR IN base_cls.py CREATE ORDERS TABLE: {e}")
            return False
        
        else:

            return True


    def insert_order(self, done=0, **kwards):

        self._db.execute(insert_order_information, 
                          kwards['orderId'], kwards['idProduct'],
                          kwards['ordersize'], kwards['userName'], kwards['secondName'],
                          kwards['userPhone'], kwards['userEmail'], kwards['City'], kwards['vidil'],
                          kwards['opls'], kwards['time'], kwards['value'], done)


    def get_orders(self) -> dict:

        for i in self._db.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 1000'):
            if i['orderProductId'] != None:
                i['data'] = self.getProduct_for_page(int(i['orderProductId']))
            
            yield i

    
    async def drop_orders_base(self, table):
        try:
            self._db.execute(f"DROP TABLE IF EXISTS {table}")
            return True
        except Exception as e:
            print(f'ERROR IN base_cls.py: {e}')
            return False


    def insert_orders(self, obj) -> bool:
        if self._db.execute(f"""INSERT INTO orders(
                {','.join(list(obj.keys()))} 
        ) VALUES(
                {','.join(['?' for _ in list(obj.values())])} 
        )""", *tuple(obj.values())):
            return True
        else: return False


a = Orders()

a._create_products_table()
a._create_orders_table()