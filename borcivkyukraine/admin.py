from cs50 import SQL
from base_cls import Card

from random import randint

import asyncio
import uuid
import shutil
import os
import re

ose = os

class Admin(Card):

    def __init__(self):
        super().__init__()
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
            return {'status': True, 'msg': f'Змінена кількість товару id={id} на {value}'}
        else: return {'status': False, 'msg': f'Кількість товару id={id} не була змінена'}


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
        return re.search(r"(\.\w{3}|\.\w{4})$", name).group()
    

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
                self.__db._disconnect()
                return int(art)
             
    
    def insert_product_info(self, **kwargs):

        article = self.random_art(1000, 1000000000000)

        if self.__db.execute("""INSERT INTO borcivkyShop(Категорія, Бренд, Модель, Колір, Ціна, Ціна2, Розмір, Кількість, Артикул, Опис) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             kwargs['category'], kwargs['brand'], kwargs['model'], kwargs['color'], kwargs['price'], kwargs['price'], kwargs['sizes'], kwargs['much'], article, kwargs['description']):
            self.__db._disconnect()
            return True
        else: return False
    
    async def insert_product_info_postgre(self, **kwargs):

        if self.__db.execute("""INSERT INTO borcivkyShop(id, Категорія, Бренд, Модель, Колір, Ціна, Ціна2, Розмір, Кількість, Артикул, Опис, Знижка) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            kwargs['id'], kwargs['Категорія'], kwargs['Бренд'], kwargs['Модель'], kwargs['Колір'], kwargs['Ціна'], kwargs['Ціна2'], kwargs['Розмір'], kwargs['Кількість'], kwargs['Артикул'], kwargs['Опис'], kwargs['Знижка']):
            self.__db._disconnect()
            return True
        else: return False


    def rename_and_remove(self, pathTo, rename_img: str, rename_name: str, remove_img: str) -> bool:
        try:
            os.rename(pathTo + remove_img, pathTo + f'removedImg{self.return_format_photo(remove_img)}')
            os.rename(pathTo + rename_img, pathTo + f'{rename_name}{self.return_format_photo(rename_img)}')

            os.remove(pathTo + f'removedImg{self.return_format_photo(remove_img)}')
        
            return True
        
        except Exception as e:

            raise e



    def del_img(self, path, img):
        folder = os.listdir(path=os.path.abspath(path))

        match len(folder):

            case 1:
                raise ValueError('Товар має тільки одне фото тому воно не може бути видалено.')

            case 2:

                check = [i for i in folder if len(img) == min([len(j) for j in folder]) and i != img]

                if len(check) == 0:
                    os.remove(path + img)

                    return True
                else:
                    try:
                        self.rename_and_remove(path, check[0], 'tit', img)
                        return True
                    except Exception as e:
                        raise e

            case _:
                getMin = min([len(j) for j in folder])
                get = [i for i in folder if len(i) == getMin or len(i) == getMin + 1]

                if img in get:
                    getIndex = get.index(img)

                    match len(get[getIndex]):

                        case 7:
                            image = [i for i in folder if i != img and len(i) != 8]
                            try:
                                self.rename_and_remove(path, image[0], 'tit', img)
                                return True
                            except Exception as e:
                                raise e


                        case 8:
                            image = [i for i in folder if i != img and len(i) != 7]
                            
                            try:
                                self.rename_and_remove(path, image[0], 'stit', img)
                                return True
                            except Exception as e:
                                raise e
                            
                else:
                    try:
                        os.remove(path + img)

                        return True
                    except Exception as e:
                        raise e

    
    def rename_twix(self, path, rename_img_twix, img, *args):
        os.rename(path + rename_img_twix, path + f'qwer{self.return_format_photo(rename_img_twix)}')
        os.rename(path + img, path + f'{args[0]}{self.return_format_photo(img)}')
        os.rename(path + f'qwer{self.return_format_photo(rename_img_twix)}', path + f'{args[1]}{self.return_format_photo(rename_img_twix)}')
    
    
    def set_first(self, path, img):

        folder = os.listdir(path=os.path.abspath(path))

        title = [i for i in folder if len(i) == min([len(j) for j in folder]) and i != img]

        match len(folder):

            case 1:

                raise ValueError('Товар вже має титульну фотографію.')
        
            case _:

                if title:
                    try:
                        sect = [i for i in folder if len(i) == (min([len(j) for j in folder]) + 1)]
                        if sect and img == sect[0]:
                            self.rename_twix(path, title[0], img, *('tit', 'stit'))
                        else:
                            ui = uuid.uuid4()
                            os.rename(path + title[0], path + f'{ui}{self.return_format_photo(title[0])}')
                            os.rename(path + img, path + f'tit{self.return_format_photo(img)}')

                        return True

                    except Exception as e:
                        raise e


    def set_sec(self, path, img):

        folder = os.listdir(path=os.path.abspath(path))

        stit = [i for i in folder if len(i) == (min([len(j) for j in folder]) + 1) and i != img]

        if len(folder) > 1:

            if stit:
                try:
                    tit = [i for i in folder if len(i) == min([len(j) for j in folder])]
                    if tit and img == tit[0]:
                        self.rename_twix(path, stit[0], img, *('stit', 'tit'))
                    
                    else:
                        ui = uuid.uuid4()
                        os.rename(path + stit[0], path + f'{ui}{self.return_format_photo(stit[0])}')
                        os.rename(path + img, path + f'stit{self.return_format_photo(img)}')

                    return True
                except Exception as e:
                    raise e

        else:

            raise ValueError('Неможливо встановити другу фотографію якщо товар має тільки одну')


    async def update_category(self, id: int, category: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Категорія=? WHERE id=?", category, id):
            self.__db._disconnect()
            return True
        
        else:
            self.__db._disconnect()
            return False
        

    async def update_brand(self, id: int, brand: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Бренд=? WHERE id=?", brand, id):
            self.__db._disconnect()
            return True
        
        else: 
            self.__db._disconnect()
            return False

    
    async def update_model(self, id: int, model: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Модель=? WHERE id=?", model, id):
            self.__db._disconnect()
            return True
        
        else: 
            self.__db._disconnect()
            return False


    async def update_color(self, id: int, color: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Колір=? WHERE id=?", color, id):
            self.__db._disconnect()
            return True
        
        else:
            self.__db._disconnect()
            return False
        
    async def update_price(self, id: int, price: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Ціна=? WHERE id=? AND Знижка == 0", price, id):
            self.__db._disconnect()
            return True
        
        else: 
            self.__db._disconnect()
            return True

    async def update_sizes(self, id: int, size: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Розмір=? WHERE id=?", size, id):
            self.__db._disconnect()
            return True
        else:
            self.__db._disconnect() 
            return False
        

    async def update_much(self, id: int, m: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Кількість=? WHERE id=?", m, id):
            self.__db._disconnect()
            return True
        
        else:
            self.__db._disconnect()
            return False
        
    
    async def update_description(self, id: int, description: str) -> bool:
        if self.__db.execute("UPDATE borcivkyShop SET Опис=? WHERE id=?", description, id):
            self.__db._disconnect()
            return True
        
        else:
            self.__db._disconnect()
            return False
        


    async def update_all_async(self, **kwargs) -> bool:
        try:
            task1 = asyncio.create_task(self.update_category(int(kwargs['id']), kwargs['category']))
                
            task2 = asyncio.create_task(self.update_brand(int(kwargs['id']), kwargs['brand']))
                
            task3 = asyncio.create_task(self.update_model(int(kwargs['id']), kwargs['model']))
                
            task4 = asyncio.create_task(self.update_color(int(kwargs['id']), kwargs['color']))
                
            task5 = asyncio.create_task(self.update_price(int(kwargs['id']), kwargs['price']))
                
            task6 = asyncio.create_task(self.update_sizes(int(kwargs['id']), kwargs['sizes']))
                
            task7 = asyncio.create_task(self.update_much(int(kwargs['id']), kwargs['much']))
                
            task8 = asyncio.create_task(self.update_description(int(kwargs['id']), kwargs['description']))
                
            alls = await asyncio.gather(task1, task2, task3, task4, task5, task6, task7, task8)
            
            if all(alls):
                return True
            else:
                return False


        except Exception as e:
            raise e


    def update_all(self, **kwargs) -> bool:
        """ 

        **kwargs {category, brand, model, color, price, sizes, much, description}

        """

        try:
            task = asyncio.run(self.update_all_async(**kwargs))

            if task:
                return True
            else:
                return False

        except Exception as e:
            raise e