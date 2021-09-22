import datetime
import file_handler


class Product:
    def __init__(self, shop_name):
        self.shop_name = shop_name
        self.barcode = None
        self.name = None
        self.price = None
        self.brand = None
        self.number = None
        self.expire_time = None

    def record_product(self):
        all_done, bar, name_done, brnd = False, False, False, False
        while not all_done:
            if not self.barcode:
                barcode = input("Please Enter the barcode: ")
                try:
                    if barcode:
                        bar = True
                        print("Barcode accepted!")
                    else:
                        bar = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                if not bar:
                    continue
                else:
                    self.barcode = barcode
            if not self.name:
                name = input("Please Enter the name: ")
                try:
                    if name:
                        name_done = True
                        print("Name accepted!")
                    else:
                        name_done = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                if not name_done:
                    continue
                else:
                    self.name = name
            if not self.price:
                price = None
                try:
                    price = float(input("Please Enter the price: "))
                except Exception as error:
                    print(f"{error} Please try again.")
                if not price:
                    continue
                else:
                    print("Price accepted!")
                    self.price = price
            if not self.brand:
                brand = input("Please Enter the brand: ")
                try:
                    if brand:
                        brnd = True
                        print("Brand accepted!")
                    else:
                        brnd = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                if not brnd:
                    continue
                else:
                    self.brand = brand
            if not self.number:
                number = None
                try:
                    number = int(input("Please Enter the number of product: "))
                except Exception as error:
                    print(f"{error} Please try again.")
                if number == None:
                    continue
                else:
                    print("Number of product accepted!")
                    self.number = number
            if not self.expire_time:
                date_string = input("Enter the expiration date, should be YYYY-MM-DD: ")
                date_format = '%Y-%m-%d'
                date_obj = None
                try:
                    date_obj = datetime.datetime.strptime(date_string, date_format)
                    if date_obj < datetime.datetime.now():
                        date_obj = None
                        raise Exception("Its already expired!")
                except Exception as error:
                    print(f"{error} Please try again!")
                if not date_obj:
                    continue
                else:
                    print("Expiring date accepted!")
                    self.expire_time = date_obj
                    all_done = True
                    self.add_to_file()

    def add_to_file(self):
        ob = file_handler.FileHandler("products.csv")
        new_product = {"shop_name": self.shop_name, "barcode": self.barcode,
                       "name": self.name,"price": self.price, "brand": self.brand,
                       "number": self.number, "expire_time": self.expire_time}
        ob.add_to_file(new_product)
        print(f"\nThe product added successfully,\
        \nwith name: {self.name}\nbarcode: {self.barcode}\
        \nprice: {self.price}\nbrand: {self.brand}\nnumber: {self.number}\
        \nexpire time: {self.expire_time}\n")

    def show_products_list(self):
        ob = file_handler.FileHandler("products.csv")
        products = ob.read_file()
        products_matrix = []
        headers = ["barcode", "name", "price", "brand", "number", "expire time"]
        products_matrix.append(headers)
        for product in products:
            if product["shop_name"] == self.shop_name:
                row = [product["barcode"], product["name"], product["price"],
                       product["brand"], product["number"], product["expire_time"]]
                products_matrix.append(row)
        print("\nThe list of all products in this shop:\n")
        for row in products_matrix:
            for item in row:
                print(item.ljust(20), end="")
            print()
        print()
        self.warning()

    def warning(self):
        ob = file_handler.FileHandler("products.csv")
        products = ob.read_file()
        for product in products:
            if product["shop_name"] == self.shop_name:
                if int(product["number"]) < 10:
                    print(
                        f"WARNING:\nproduct with barcode: {product['barcode']}\
,name: {product['name']}, of brand: {product['brand']}, has only {product['number']} left!!!\n")
