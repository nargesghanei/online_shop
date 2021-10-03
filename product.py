import datetime
from file_handler import FileHandler
import csv
import logging


# This class is for all products and doing things related to them
class Product:
    def __init__(self, shop_name):
        logging.basicConfig(filename='records.log', filemode='a',
                            format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.shop_name = shop_name
        self.barcode = None
        self.name = None
        self.price = None
        self.brand = None
        self.number = None
        self.expire_time = None

    # add a new product
    def record_product(self):
        all_done, bar, name_done, brnd = False, False, False, False
        while not all_done:  # untill all info of a product add in a right way
            if not self.barcode:  # if barcode was not added
                barcode = input("Please Enter the barcode: ")
                try:
                    if barcode:
                        bar = True  # added successfully
                        print("Barcode accepted!")
                    else:
                        bar = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not bar:  # if barcode was not add yet do not go for other info and start from first of loop
                    continue
                else:
                    self.barcode = barcode
            if not self.name:  # if name was not added
                name = input("Please Enter the name: ")
                try:
                    if name:
                        name_done = True  # added successfully
                        print("Name accepted!")
                    else:
                        name_done = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not name_done:  # if name was not add yet do not go for other info and start from first of loop
                    continue
                else:
                    self.name = name
            if not self.price:  # if price was not added
                price = None
                try:
                    price = float(input("Please Enter the price: "))  # get a float number for price
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not price:  # if price was not add yet do not go for other info and start from first of loop
                    continue
                else:
                    print("Price accepted!")
                    self.price = price
            if not self.brand:  # if brand was not added
                brand = input("Please Enter the brand: ")
                try:
                    if brand:
                        brnd = True  # added successfully
                        print("Brand accepted!")
                    else:
                        brnd = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not brnd:  # if price was not add yet do not go for other info and start from first of loop
                    continue
                else:
                    self.brand = brand
            if not self.number:  # if number was not added
                number = None
                try:
                    number = int(input("Please Enter the number of product: "))
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not number:  # if price was not add yet do not go for other info and start from first of loop
                    continue
                else:
                    print("Number of product accepted!")
                    self.number = number  # added successfully
            if not self.expire_time:  # if expired date was not added
                # get the date in a special form of string
                date_string = input(
                    "Enter the expiration date, should be YYYY-MM-DD (If it does not get expired enter 2100-01-01): ")
                date_format = '%Y-%m-%d'  # get a format to date
                date_obj = None
                try:
                    # create a date object with string of date and format
                    date_obj = datetime.datetime.strptime(date_string, date_format)
                    if date_obj < datetime.datetime.now():  # if expired date is before today
                        date_obj = None
                        raise Exception("Its already expired!")
                except Exception as error:
                    print(f"{error} Please try again!")
                    logging.error(f"{error}  , Happened in recording a product.")
                if not date_obj:  # if date was not accepted go from first of loop
                    continue
                else:
                    print("Expiring date accepted!")
                    self.expire_time = date_obj
                    all_done = True  # all things added correctly, breaking loop variable got true value
                    self.add_to_file()  # add products information to file
                    logging.info(f"Product {self.barcode} for store {self.shop_name} added.")

    # add products info to file
    def add_to_file(self):
        ob = FileHandler("products.csv")
        new_product = {"shop_name": self.shop_name, "barcode": self.barcode,
                       "name": self.name, "price": self.price, "brand": self.brand,
                       "number": self.number, "expire_time": self.expire_time}
        ob.add_to_file(new_product)
        print(f"\nThe product added successfully,\
        \nwith name: {self.name}\nbarcode: {self.barcode}\
        \nprice: {self.price}\nbrand: {self.brand}\nnumber: {self.number}\
        \nexpire time: {self.expire_time}\n")

    # faze 2 ...
    def show_products_list(self, user):
        products = Product.read_from_file('products.csv')

        products_matrix = []
        if user == "manager":
            headers = ["barcode", "name", "price", "brand", "number", "expire time"]
        elif user == "client":
            headers = ["name", "price", "brand", "expire time"]
        else:
            print("Invalid command!")
            logging.error("Invalid command in show products!")
            return
        products_matrix.append(headers)

        for product in products:
            if product["shop_name"] == self.shop_name:
                if user == "manager":
                    row = [product["barcode"], product["name"], product["price"], product["brand"], product["number"],
                           product["expire_time"]]
                else:
                    row = [product["name"], product["price"], product["brand"], product["expire_time"]]
                products_matrix.append(row)
        print("\nThe list of all products in this shop:\n")
        for row in products_matrix:
            for item in row:
                print(item.ljust(20), end="")
            print()
        print()
        if user == "manager":
            self.warning()

    # show warning to manager if a product going to finish
    def warning(self):
        products = Product.read_from_file('products.csv')
        for product in products:
            if product["shop_name"] == self.shop_name:
                if int(product["number"]) < 10:  # warn manager for less than 10 number of a product
                    print(
                        f"WARNING:\nproduct with barcode: {product['barcode']}\
,name: {product['name']}, of brand: {product['brand']}, has only {product['number']} left!!!\n")
                if int(product['number']) == 0:  # if it was finished log it
                    logging.warning(f"Product {product['barcode']} of store {product['shop_name']} finished.")

    # extra: charge a product
    def charge(self):
        ob = FileHandler('products.csv')
        products = ob.read_file()
        # get the barcode of product that want to be added
        barcode = input("Enter the barcode of product that you want to charge: ")
        add = None
        for product in products:
            # if it was for managers shop and its barcode was like input one
            if product['shop_name'] == self.shop_name and product['barcode'] == barcode:
                print(f"\nProduct found.It has {product['number']} left.")
                added = False
                while not added:
                    try:
                        # get the number of adding
                        add = int(input("How many do you want to add? "))
                    except Exception as error:
                        print(f"{error}, Please Try again!")
                        logging.error(f"{error}  , Happened in charging a product.")
                    else:
                        added = True
        # headers
        fields = ["shop_name", "barcode", "name", "price", "brand", "number", "expire_time"]
        with open("products.csv", 'w') as my_file:  # rewrite the file to get update
            writer = csv.DictWriter(my_file, fieldnames=fields)
            writer.writeheader()
            for product in products:
                if product['barcode'] != barcode:  # write all products except the updated one
                    ob.add_to_file(product)
                else:
                    new_product = {"shop_name": product['shop_name'],
                                   "barcode": product['barcode'], "name": product['name'],
                                   "price": product['price'], "brand": product['brand'],
                                   "number": int(product['number']) + add,  # add the number to what it was
                                   "expire_time": product['expire_time']}
                    ob.add_to_file(new_product)  # append the updated product to file
                    print(f"\nProduct with barcode {barcode} updated successfully!\n")

    def search_a_product(self):
        ob = FileHandler('products.csv')
        products = ob.read_file()
        searched = False
        name, brand = None, None
        print()
        while not searched:
            try:
                base = input("In which base do you want to search(name/brand)? ")
                if base == 'name':
                    searched = 'name'
                elif base == 'brand':
                    searched = 'brand'
                else:
                    raise Exception("There is not such a search base!")
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in searching for a product.")
            if not searched:
                continue
            if searched == 'name':
                find = False
                name = input("Enter the name of product: ")
                if name:
                    print(f"\nList of all {name} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['name'] == name:
                            find = True
                            print(f"Of brand: {product['brand']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any {name} in this store.\n")
            elif searched == 'brand':
                find = False
                brand = input("Enter the brand of product: ")
                if brand:
                    print(f"\nList of all products with brand {brand} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['brand'] == brand:
                            find = True
                            print(f"name: {product['name']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any product  of brand {brand} in this store.\n")
            else:
                continue

            if searched == "name":
                brand = input(f"Enter the brand of {name} you want? ")
            elif searched == "brand":
                name = input(f"Enter the name of product you want from brand {brand}: ")
            headers = ["shop_name", "barcode", "name", "price", "brand",
                       "number", "expire_time"]
            buyed, number = None, 0
            for product in products:
                if product['name'] == name and product['brand'] == brand:
                    try:
                        number = int(input(f"How many {name} of {brand} do you want? "))
                        if number > int(product['number']):
                            raise Exception("Sorry! There is not enough of your choice.")
                    except Exception as error:
                        print(f"{error} Please try again!")
                        logging.error(f"{error}  , Happened in searching a product.")
                        break

                    buyed = product
                    break
            if buyed:
                with open("products.csv", 'w') as my_file:
                    writer = csv.DictWriter(my_file, fieldnames=headers)
                    writer.writeheader()
                    for product in products:
                        if not (product['name'] == name and product['brand'] == brand):
                            ob.add_to_file(product)
                        else:
                            updated = {"shop_name": product['shop_name'], "barcode": product['barcode'],
                                       "name": product['name'], "price": product['price'],
                                       "brand": product['brand'], "number": int(product['number']) - number,
                                       "expire_time": product['expire_time']}
                ob.add_to_file(updated)
                pre_invoice = [name, brand, number, float(updated['price']) * number]
                return pre_invoice

    @staticmethod
    def read_from_file(file_name):
        ob = FileHandler(file_name)
        information = ob.read_file()
        return information

