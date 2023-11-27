from cs50 import SQL
from base_cls import Card

from random import randint

import shutil
import os
import re

ose = os

class Admin(Card):

    def __init__(self):
        self.__db = SQL('sqlite:///borcivky.db')
        self.__db._autocommit = True



    def change_price_value(self, id: int, value: int) -> bool:

        if value > 0:
            if self.__db.execute('UPDATE borcivkyShop SET Ціна=?, Ціна2=? WHERE id=? AND Знижка=0', value, value, id):
                self.__db._disconnect()
                return True
            else:
                return False
        else:
            return False
        


    def change_discount_value(self, id: int, value: int) -> bool:

        if value in range(0, 101):
            self.__db.execute('UPDATE borcivkyShop SET Знижка=? WHERE id=?', value, id)
            self.__db._disconnect()
            return True
        else:
            return False
        


    def change_much_value(self, id: int, value: int) -> bool:

        if value >= 0:
            self.__db.execute('UPDATE borcivkyShop SET Кількість=? WHERE id=?', value, id)
            self.__db._disconnect()
            return True
        else: return False


    def delete(self, id: int) -> bool:
        if self.__db.execute("DELETE FROM borcivkyShop WHERE id=?", id):
            self.__db._disconnect()
            return True
        else:
            return False

    def delete_product(self, obj: dict[Card]) -> bool:
        category = self.check_for_space(self.check_for_slash(obj['Категорія']))
        brend = self.check_for_space(self.check_for_slash(obj['Бренд']))
        model = self.check_for_space(self.check_for_slash(obj['Модель']))
        color = self.check_for_space(self.check_for_slash(obj['Колір']))

        if self.delete(int(obj['id'])):
            path = ose.path.abspath(ose.curdir) + f"/static/images/{category}/{brend}/{model}{color}"
            shutil.rmtree(path)
            return True
        else: return 'DELETE FAILED'
        

    def done(self, id: int) -> bool:
        if self.__db.execute("UPDATE orders SET done=1 WHERE orderId=?", id):
            self.__db._disconnect()
            return True
        else:
            return False

    def get_path(self, **kwargs):
        category = self.check_for_space(kwargs['category'])
        brand = self.check_for_space(kwargs['brand'])
        model = self.check_for_space(kwargs['model'])
        color = self.check_for_space(self.check_for_slash(kwargs['color']))

        name = f'{model}{color}'

        return f'static/images/{category}/{brand}/{name}'
    
    def create_path_if_not_exists(self, path):
        sys_path = ose.path.abspath(ose.curdir)
        cur_path = ''
        for i in path.split('/'):
            cur_path += ('/' + i)
            try:
                ose.listdir(sys_path + cur_path)
            except FileNotFoundError as e:
                new_path = (sys_path + cur_path).replace(e.filename.split('/')[-1], '')
                create = ose
                create.chdir(new_path)
                create.mkdir(e.filename.split('/')[-1])
                create.chdir(sys_path)
                
                continue
        
        if ose.path.exists(sys_path + cur_path):
            return sys_path + cur_path
        else: return False

    def return_format_photo(self, name: str):
        return re.search(r"(\.\w+)", name).group()
    

    def random_art(self, a: int, b: int) -> int:
        article = self.__db.execute('SELECT Артикул FROM borcivkyShop')

        try:
            arr = [int(i['Артикул']) for i in article]
        except:
            return randint(100, 1000)

        while True:
            number = randint(a, b)

            num_to_str = str(number)

            first_part = int(len(num_to_str) / 2)

            second_part = int(first_part + randint(1, 6))

            art = num_to_str[first_part:second_part]

            if art in arr:
                continue
            else:
                return int(art)
             
    
    def insert_product_info(self, **kwargs):

        article = self.random_art(1000, 1000000000000)

        print(article)
        if self.__db.execute("""INSERT INTO borcivkyShop(Категорія, Бренд, Модель, Колір, Ціна, Ціна2, Розмір, Кількість, Артикул, Опис) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             kwargs['category'], kwargs['brand'], kwargs['model'], kwargs['color'], kwargs['price'], kwargs['price'], kwargs['sizes'], kwargs['much'], article, kwargs['description']):
            self.__db._disconnect()
            return True
        else: return False
        