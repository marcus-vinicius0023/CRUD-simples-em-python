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
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
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
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
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
            conn.commit()
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
    
    #Needs complete product, self.id is a old product id in db
    def update_product(self)-> None:
        if self._exists_by_id(self.id):
            cursor.execute(
                f"""UPDATE {TABLENAME} 
                SET name = ?, price = ?, description = ? 
                WHERE id = ?""",
                (self.name, self.price, self.description, self.id)
            )
            conn.commit()
            print("Product updated successfully")
        else:
            print("This product does not exist to be updated")

    @staticmethod
    def delete_by_id(id)-> None:
        if Product._exists_by_id(id):
            cursor.execute(
                f"""DELETE FROM {TABLENAME} 
                WHERE id = ?""",
                id
            )
            conn.commit()
            print("Product deleted successfully")
        else:
            print("This product does not exist to be deleted")


    @staticmethod
    def print_all_products()-> None:
        cursor.execute(f"SELECT * FROM {TABLENAME}")
        all_products = cursor.fetchall()

        for product in all_products:
            print(product)


class Prompt:

    @staticmethod
    def _loop_y_n(first_question, seccond_question) -> str:
        while True:
            user_response = input(first_question + " (y or n)\n:")
            if user_response.lower() == "y":
                name = input(seccond_question)
                return name
            elif user_response.lower() == "n":
                return None

    @staticmethod
    def first_prompt():
        print("         Products Register\n---------------------------------------")
        print(
            "1- Create a new product\n"
            "2- Print product\n"
            "3- Update a product\n"
            "4- Delete a product\n"

            "\n0- to quite"
        )      
    
        response = input("\nInput: ")  
        if response == "1":
            Prompt.create_()

        elif response == "2":
            Prompt.print_()

        elif response == "3":
            Prompt.update_()

        elif response == "4":
            Prompt.delete_()

        elif response == "0":
            return False
        
        print("Invalid answer")
            
    @staticmethod
    def _get_product_data():
        name = input("Send product name: ")
        if not isinstance(name, str):
            return "invalid product name"
      
        price = float(input("Send product price: "))
        if not isinstance(price, float):
            return "invalid product price"
    
        description = input("Send product description")
        if not isinstance(description, str):
            return "Invalid product price"


        new_product = Product(name, price, description)
        return new_product

    @staticmethod
    def create_():
        name = input("Send product name: ")
        if not isinstance(name, str):
            return "invalid product name"
      
        price = float(input("Send product price: "))
        if not isinstance(price, float):
            return "invalid product price"
    
        description = input("Send product description")
        if not isinstance(description, str):
            return "Invalid product price"

        new_product = Product(name, price, description)
        new_product.create_product()

    @staticmethod
    def print_():
        print("         Products Register\n---------------------------------------")
        print(
            "1- Print all products\n"
            "2- Print one product\n"
            
            "\n0- to quite"
        )  
        response = input("\nInput: ")    
        
        if response == "0":
            return
        elif response == "1":
            Product.print_all_products()
            Prompt.first_prompt()
        elif response == "2":
            response = input("\nInsert Name or ID: ")

            by_name = Product.find_by_name(response)
            if by_name:
                print(by_name)
                return

            by_id = Product.find_by_id(response)
            if by_id:
                print(by_id)
                return

    @staticmethod
    def update_():
        id = None
        Product.print_all_products()
        print("")
        while True:
            id = input("How product you want a change? Send his id: ")
            if Product.find_by_id(id):
                break

        old_product = Product.find_by_id(id)
       
        name = old_product[1]
        price = old_product[2]
        description = old_product[3]
        
        print(old_product)

        new_name = Prompt._loop_y_n("You want change a product name?", "Subimit a new product name: ")
        if new_name:
            name = new_name

        new_price = Prompt._loop_y_n("You want change a product price?", "Subimit a new product price: ")
        if new_price:
            price = new_price 

        new_description= Prompt._loop_y_n("You want change a product description?", "Subimit a new product description: ")
        if new_description:
            description = new_description
        
        

        final_product = Product(name, price, description, old_product[0])
        final_product.update_product()
        print(Product.find_by_id(id))
 
    @staticmethod
    def delete_():
        id = None
        print("")
        while True:
            Product.print_all_products()
            id = input("How product you want a delete? Send his id: ")
            if Product.find_by_id(id):
                break
    
        Product.delete_by_id(id)
    


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

def create_db_body():

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLENAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price FLOAT NOT NULL,
        description TEXT NOT NULL
    );''')
    conn.commit()
create_db_body()


while True:
    res = Prompt.first_prompt()

    if res == False:
        break


conn.close()