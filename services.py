import sqlite3
from dataclasses import dataclass
from typing import Optional

from models import Product
from constants import TABLENAME, CATEGORIES


class ProductServices:
    def __init__(self, db_path: str = "market.db") -> None:
        self.db_path = db_path
        self._create_table_if_not_exists()

    #DB 
    def _conect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn

    def _create_table_if_not_exists(self) -> None: 
        with self._conect() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLENAME}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price FLOAT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL
            );''')
            conn.commit()


    #CRUD
    def create(self, product: Product) -> Product:
        with self._conect() as conn:
            cursor = conn.cursor()

            #Tests
            #product should no have an id, because id is automatically create by DB
            if product.id != None:
                print("product.id needs to be 'None'!")
                return None

            #Check if product have a valid category
            if product.category.upper() not in CATEGORIES:
                print("Invalid product.category")
                print(product.category)
                return None

            #Check if product.name alredy exists in DB, we don't want duplicate names in DB 
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE name = ?", (product.name,))
            response = cursor.fetchall()
            if response != []:
                print("This product name already exits!")
                return None

            
            #Create product in DB
            cursor.execute(
                    f"INSERT INTO {TABLENAME} (name, price, category, description) VALUES (?, ?, ?, ?)",
                    (product.name.upper(), product.price, product.category.upper(), product.description)
                )

            conn.commit()
            product.id = cursor.lastrowid
            return product
        
    def read(self, type: str = "all", key: Optional[str] = None) -> list:
        """
        Print products based on the query type
    
        Args:
            type: "all" for simple datas for all products, 
                  "category" for simple datas for all products present in corresponding category,
                  "unique" for all information about a product.

            key: product id or product name or category
        """
        if type != "all" and key == None:
            print("If type dont 'all' require insert one key")
            return None

        with self._conect() as conn:
            cursor = conn.cursor()

            if type.lower() == "all":
                cursor.execute(f"SELECT * FROM {TABLENAME}")
                response = cursor.fetchall()
                
                products = []

                for product in response:
                    inst_product = Product(id=product[0],
                                           name=product[1],
                                           price=product[2],
                                           category=product[3],
                                           description=product[4])
                    products.append(inst_product)    
                return products  

            elif type.lower() == "category":
                if key.upper() in CATEGORIES:
                    cursor.execute(f"SELECT * FROM {TABLENAME} WHERE category = ?", (key.upper(),))
                    response = cursor.fetchall()
                    
                    products = []

                    for product in response:
                        inst_product = Product(id=product[0],
                                               name=product[1],
                                               price=product[2],
                                               category=product[3],
                                               description=product[4])
                        products.append(inst_product)
                    return products
                else:
                    print("invalid category")
                    return None

            elif type.lower() == "unique":
                cursor.execute(f"SELECT * FROM {TABLENAME} WHERE name = ?", (key.upper(),))
                response = cursor.fetchone()

                #Case don't find anyone product name/key
                if not response:
                    cursor.execute(f"SELECT * FROM {TABLENAME} WHERE id = ?", (key.upper(),))
                    response = cursor.fetchone()

                    #Case don't find anyone product id/key
                    if not response:
                        return None

                #Create a product based in response  
                product = Product(id=response[0], name=response[1], price=response[2], category=response[3], description=response[4])
                return [product]

            else:
                print("Invalid type: arg")
                return None
    
    def update(self, updated_product: Product) -> Product:
        with self._conect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE id = ?", (updated_product.id,))
            response = cursor.fetchall()

            if response == []:
                print("Don't exits product if this id to be updated")
                return None
            
            if updated_product.category.upper() not in CATEGORIES:
                print("Invalid product.category")
                print(product.category)
                return None

            cursor.execute(f"""
                UPDATE {TABLENAME} 
                SET name = ?, price = ?, category = ?, description = ? 
                WHERE id = ?""",
                (updated_product.name.upper(), updated_product.price, updated_product.category.upper(), updated_product.description, updated_product.id)
            )

            conn.commit()
            return updated_product

    def delete(self, id) -> Product:
        with self._conect() as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE id = ?", (id,))
            response = cursor.fetchone()

            if not response:
                print("Don't exits product if this id to be deleted")
                return None

            #Save a product for return    
            deleted_product = Product(id=response[0], name=response[1], price=response[2], category=response[3], description=response[4])

            cursor.execute(f"""DELETE FROM {TABLENAME} WHERE id = ?""", (id,))

            conn.commit()
            return deleted_product
            