import sqlite3

class Product:
    def __init__(self, name, price, description, id=None):
        self.name = name    
        self.price = price
        self.description = description
        self.id = id


    def create_product_in_db(self):
        cursor.execute(f"INSERT INTO products (name, price, description) VALUES ('Uva', 2.99, 'One');")
    
    def read_product_in_db(product_name):
        if product_name in "Todos os nomes dos produtos":
            return "Os dados completos desse produto"
        else:
            return "This product don't exist"

    def update_product_in_db(self):
        print("Atualizando dados do produto no banco de dados")

    def delete_product_in_db(self):
        print("Produto removido do banco de dados")




    def print_all_products():
        print("Imprimindo o nome de todos os produtos")



myDB = sqlite3.connect("products.db")
cursor = myDB.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price FLOAT,
    description TEXT NOT NULL
);''')
myDB.commit()

#while True:
    
    #Execução do programa
    

cursor.execute("SELECT * FROM products")
result = cursor.fetchall()
print(result)

myDB.commit()
myDB.close()