import sqlite3

TABLENAME = "products"


class Product:
    def __init__(self, name, price, description, id = None):
        self.name = name    
        self.price = price
        self.description = description
        self.id = id

    @staticmethod
    def _exists_by_name(name)-> bool:
        cursor.execute(
            f"SELECT * FROM {TABLENAME} WHERE name = ?",
            (name,)
        )
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False
    @staticmethod
    def _exists_by_id(id)-> bool:
        cursor.execute(
            f"SELECT * FROM {TABLENAME} WHERE id = ?",
            (id,)
        )
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False

    def create_product(self)-> None:
        if self._exists_by_name(self.name):
            print("This product already exists")
        else:
            cursor.execute(
                f"INSERT INTO {TABLENAME} (name, price, description) VALUES (?, ?, ?)",
                (self.name, self.price, self.description)
            )
            myDB.commit()
            print("Product added successfully")
    
    @staticmethod
    def find_by_name(name)-> list:
        if Product._exists_by_name(name):
            cursor.execute(
                f"SELECT * FROM {TABLENAME} WHERE name = ?",
                (name,)
            )
            return cursor.fetchall()
        else:
            print("No product exists with this name")
            return None
    @staticmethod
    def find_by_id(id)-> list:
        if Product._exists_by_id(id):
            cursor.execute(
                f"SELECT * FROM {TABLENAME} WHERE id = ?",
                (id,)
            )
            return cursor.fetchone()            
        else:
            print("No product exists with this id")
            return None
    
    def update_product(self)-> None:
        if self._exists_by_id(self.id):
            cursor.execute(
                f"""UPDATE {TABLENAME} 
                SET name = ?, price = ?, description = ? 
                WHERE id = ?""",
                (self.name, self.price, self.description, self.id)
            )
            myDB.commit()
            print("Product updated successfully")
        else:
            print("This product does not exist to be updated")

    @staticmethod
    def delete_by_id(id)-> None:
        if Product._exists_by_id(id):
            cursor.execute(
                f"""DELETE FROM {TABLENAME} 
                WHERE id = ?""",
                (id,)
            )
            myDB.commit()
            print("Product deleted successfully")
        else:
            print("This product does not exist to be deleted")


    @staticmethod
    def return_all_products()-> list:
        cursor.execute(f"SELECT * FROM {TABLENAME}")
        return cursor.fetchall()

    
    
#Temporary function
def create_products():
    new_product1 = Product("Abacate", 9.10, "Abacate maduro e cremoso")
    new_product1.create_product()

    new_product2 = Product("Banana", 4.50, "Banana nanica, bem docinha")
    new_product2.create_product()

    new_product3 = Product("Maçã", 7.00, "Maçã vermelha, fresca e crocante")
    new_product3.create_product()

    new_product4 = Product("Laranja", 5.20, "Laranja suculenta para suco")
    new_product4.create_product()

    new_product5 = Product("Manga", 12.00, "Manga madura, doce e perfumada")
    new_product5.create_product()

myDB = sqlite3.connect("products.db")
cursor = myDB.cursor()
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {TABLENAME}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price FLOAT,
    description TEXT NOT NULL
);''')
myDB.commit()


#while True:
    
    #Program execution


#create_products()




myDB.close()