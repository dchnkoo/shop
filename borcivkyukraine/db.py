from dotenv import load_dotenv
import psycopg2

import os
import regex
import shutil
 
import asyncio
from admin import Admin
from base_cls import Orders


class PostgreDB(Admin, Orders):

    def __init__(self):
        super().__init__()
        load_dotenv()   
        self.databaseinfo = {
            "DATABASE_URL": os.getenv('DATABASE_URL'),
        }
        
    
    @staticmethod
    def _db_commit_close(db, cursor) -> None:
        db.commit()
        cursor.close()


    @staticmethod
    def _close_db_connection(db, cur) -> None:
        cur.close()

    def _connect_to_db(self):
        return psycopg2.connect(self.databaseinfo['DATABASE_URL'], sslmode='require')


    def _create_table_borcivky_shop(self, db, cur) -> None:

        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS borcivkyShop(
                            id SERIAL PRIMARY KEY,
                            tit BYTEA NOT NULL,
                            tit2 BYTEA,
                            static1 BYTEA,
                            static2 BYTEA,
                            Категорія TEXT NOT NULL,
                            Бренд TEXT NOT NULL,
                            Модель TEXT NOT NULL,
                            Колір TEXT NOT NULL,
                            Ціна INTEGER NOT NULL,
                            Ціна2 INTEGER NOT NULL,
                            Розмір TEXT NOT NULL,
                            Кількість INTEGER NOT NULL,
                            Артикул INTEGER NOT NULL,
                            Опис TEXT NOT NULL,
                            Знижка INTEGER DEFAULT 0
            )""")

        except psycopg2.errors.InFailedSqlTransaction:
                return False
        
        else:
            db.commit()
            return True
        

    def _create_table_orders_shop(self, db, cur) -> None:

        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS orders(
                            id SERIAL PRIMARY KEY,
                            "orderId" INTEGER,
                            "orderProductId" INTEGER,
                            "orderSize" TEXT,
                            "Name" TEXT,
                            "SecondName" TEXT,
                            phone TEXT,
                            "Email" TEXT,
                            city TEXT,
                            "Warhouse" TEXT,
                            "Pay" TEXT,
                            date TEXT,
                            count INTEGER,
                            done INTEGER
            )""")

        except psycopg2.errors.InFailedSqlTransaction:
            return False
        
        else:

            db.commit()
            return True
            



    @staticmethod
    def _get_bynary_photos(photos: dict) -> dict[list]:
        tm = list(photos.keys())
        for i in tm:
            if i not in ['tit', 'tit2', 'static1', 'static2']:
                del photos[i]

        keys = list(photos.keys())
        values = list(photos.values())

        if len(values) >= 1:
            for x in range(len(values)):
                with open(values[x], 'rb') as f:
                    p = f.read()
                    ind = values.index(values[x])

                    del values[ind]
                    values.insert(ind, p)

            return {'keys': keys, 'bphotos': list(map(lambda x: psycopg2.Binary(x), values))}
        else:
            return []


    @staticmethod
    def _unpack_dict_values(**kwargs):
        return {'keys': ', '.join([*kwargs.keys()]), 'values': tuple([*kwargs.values()])}


    def insert_info_into_product_table(self, photos: list | str, info: dict, db, cur) -> bool:
        self._create_table_borcivky_shop(db, cur)

        inf = self._unpack_dict_values(**info)
        bphoto = self._get_bynary_photos(photos)
        

        try:
            cur.execute(f"""INSERT INTO borcivkyShop(
                    {','.join(bphoto['keys'])}, {inf['keys']}
            ) VALUES(
                {','.join(['%s' for _ in bphoto['keys']])}, {','.join(['%s' for _ in inf['values']])} 
            );""", tuple(bphoto['bphotos'] + list(inf['values'])))

        except Exception as e:
            return e
        
        else:
            db.commit()
            return True


    def _update_column_database_discount(self, id, db, price=None, to_old_price=False):
        cur = db.cursor()
        
        if to_old_price:
            cur.execute('SELECT Ціна FROM borcivkyShop WHERE id=%s', (id, ))
            get_old_price = cur.fetchone()
            cur.execute("UPDATE borcivkyShop SET Ціна2=%s WHERE id=%s", (get_old_price[0], id))

        else:
            cur.execute('UPDATE borcivkyShop SET Ціна2=%s WHERE id=%s', (price, id))

        self._db_commit_close(db, cur)


    @staticmethod
    def calc_discount(dscnt: int, price: int) -> int:
        return int(price * (dscnt / 100))

    
    def _convert_to_key_values(self, keys: tuple, value: tuple) -> dict:
        return dict(zip([desc[0] for desc in keys], value))

        
    def get_all_data(self, cur):
        cur.execute("SELECT * FROM borcivkyShop")

        data = cur.fetchall()
        keys = cur.description

        for x in range(len(data)):
            yield self._convert_to_key_values(keys, data[x])
        
    
    async def load_photo(self, obj: dict) -> bool:
        try:
            keys = list(obj.keys())

            for x in keys:
                if x in ['tit', 'tit2', 'static1', 'static2'] and obj[x]:
                    path = self.create_path_if_not_exists(self.get_path(category=obj['Категорія'],
                                                                brand=obj['Бренд'],
                                                                model=obj['Модель'],
                                                                color=obj['Колір']))
                    
                    with open(path + '/' + x + '.jpg', 'wb') as img:
                        img.write(obj[x])

                continue  
        except Exception as e:
            raise e
        
        else:
            return True


    async def rm_images(self):
        try:
            shutil.rmtree(os.path.abspath('static/images'))

        except Exception as e:
            print(f'ERROR db.py IN rm_images: {e}')
            return False
        
        else:
            return True
            
    @staticmethod
    def _edit_obj_before_insert(obj):
        ph = {}

        for v in range(len(obj['photos'])):
            print(obj['photos'])
            lp = regex.findall(r'([^\*\/:?«<>|]+)', obj['photos'][v][1])
            lastChild = len(lp[-1])

            match lastChild:

                case n if n <= 7:
                    ph['tit'] = obj['photos'][v][1]
                case n if n == 8:
                    ph['tit2'] = obj['photos'][v][1]
                case _:
                    if 'static1' not in list(ph.keys()):
                        ph['static1'] = obj['photos'][v][1]
                    else:
                        ph['static2'] = obj['photos'][v][1]


        obj['Розмір'] = ' '.join(obj['Розмір']).strip()
        
        del obj['photos']
        try:
            del obj['discountPrice']
        except KeyError:
            pass
        
        return {'photos': ph, 'obj': obj}


    async def load_all_data_to_site(self, obj):
        task1 = asyncio.create_task(self.load_photo(obj))
        task2 = asyncio.create_task(self.insert_product_info_postgre(**obj))

        alls = await asyncio.gather(task1, task2)
        if all(alls):
            return True
        else: return False


    async def execute_load(self, db, cur):
        try:
            await self.drop_orders_base('orders')
            await self.drop_orders_base('borcivkyShop')
            await self._create_orders_table()
            await self._create_products_table()
            await self.insert_all_orders_from_postgre(db, cur)

            await self.rm_images()

            for x in self.get_all_data(cur):
                await self.load_all_data_to_site(x)
        except Exception as e:
            print(e)
            return False

        else:
            return True

    async def _insert_info_orders_table(self, db, cur):
        try:
            self._drop_product_data_base(db, cur, 'orders')
            self._create_table_orders_shop(db, cur)

            for x in self.get_orders():
                try:
                    del x['data']
                except KeyError:
                    pass
                
                try:
                    cur.execute(f"""INSERT INTO orders(
                            {','.join([f'"{i}"' for i in list(x.keys())])} 
                    ) VALUES(
                            {','.join(['%s' for _ in list(x.values())])}
                    )""", tuple(list(x.values())))

                except psycopg2.Error as e:
                    db.rollback()  # Відкат транзакції у випадку помилки
                    print(f"Error during SQL execution: {e}")
                    continue
                except Exception as e:
                    db.rollback()  # Відкат транзакції у випадку будь-якої іншої помилки
                    print(f"An unexpected error occurred: {e}")
                    continue
                else:
                    db.commit()

        except Exception as e:
            print(f"An error occurred: {e}")

        else:
            return True


    async def insert_all_orders_from_postgre(self, db, cur):

        try:
            
            for i in self.get_all_orders(db, cur):
                self.insert_orders(i)
        except Exception as e:
            print(f'Error an occured in insert from postgre: {e}')
            return False
        else:
            return True

        
    def get_all_orders(self, db, cur):
        cur = db.cursor()

        cur.execute("SELECT * FROM orders")

        data = cur.fetchall()
        keys = cur.description


        for x in range(len(data)):
            yield self._convert_to_key_values(keys, data[x])



    def _drop_product_data_base(self, db, cur, table):
        try:
            cur.execute(f"DROP TABLE IF EXISTS {table}")
            db.commit()
            return True
        except Exception as e:
            db.rollback()  # Відкат транзакції у випадку помилки
            print(f"An error occurred: {e}")
            return False



    async def upload_to_postgre_products(self, db, cur):
        self._drop_product_data_base(db, cur, 'borcivkyshop')

        for i in self._get_all():
            obj = self._edit_obj_before_insert(i)
            self.insert_info_into_product_table(obj['photos'], obj['obj'], db, cur)

        return True
    
    async def execute_upload(self, db, cur):
        task1 = asyncio.create_task(self.upload_to_postgre_products(db, cur))
        task2 = asyncio.create_task(self._insert_info_orders_table(db, cur))

        return await asyncio.gather(task1, task2)