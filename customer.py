import logging
from file_handler import FileHandler
from datetime import datetime
from product import Product
import csv


# This class shows accesses of customer
class Customer:
    def __init__(self, user):
        logging.basicConfig(filename='records.log', filemode='a', format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.role = user["role"]
        self.user_name = user["username"]
        self.block_list = user["block_list"]
        self.available_stores = []
        self.chosen_store = None

    # This part until end is for second faze and its not complete yet
    def show_customers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 5:
            print("1-View previous invoices")
            print("2-View list of stores")
            print("3-Store search")
            print("4-Confirm purchase or edit")
            print("5-Log out")
            try:
                choice = int(input("Choose an option: "))
            except Exception as error:
                print(f"{error}. Please try again!")

            if choice == 1:
                self.show_pre_invoice()
            elif choice == 2:
                self.show_stores_list()
            elif choice == 3:
                self.search_store()
            elif choice == 4:
                print("\n1- Confirm a purchase")
                print("2- Edit your purchase")
                done, option = False, None
                while not done:
                    try:
                        option = int(input("Enter your option: "))
                        if not (1 <= option <= 2):
                            raise Exception("There is not such an option!")
                    except Exception as error:
                        print(f"{error} Please try again.")
                    if option == 1:
                        done = True
                        self.confirm()
                    elif option == 2:
                        done = True
                        self.edit()

    def show_stores_list(self):
        self.available_stores = []
        shops = Customer.read_from_file('users.csv')
        current_time = datetime.now().hour * 60 + datetime.now().minute
        blocked_shops = []
        for user in shops:
            if user['username'] == self.user_name:
                blocked = user['block_list']
                blocked_shops = blocked.split('-')
                break
        print("\nHere is the list of stores that are available now:\n")
        i = 1
        for shop in shops:
            if shop['role'] == 'manager':
                work_time = eval(shop['work_time'])
                if work_time[0] <= current_time <= work_time[1] and shop['shop_name'] not in blocked_shops:
                    print(f"Store number {i}: name: {shop['shop_name']}, work hours: {shop['work_hour']}")
                    self.available_stores.append(shop['shop_name'])
                    i += 1
        print()

    def search_store(self):
        self.show_stores_list()
        quitt = False
        print()
        while not quitt:
            try:
                chosen_store = input("Enter the store that you want to buy from or -1 to quit: ")
                if not chosen_store:
                    raise Exception("You should enter a shop name!")
                if chosen_store not in self.available_stores and chosen_store != '-1':
                    raise Exception("This store is not available!")
                if chosen_store == '-1':
                    quitt = True
                else:
                    quitt = True
                    self.chosen_store = chosen_store
                    print("Have a great shopping time!\n")
                    self.enter_to_a_store()
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in searching stores.")

    def enter_to_a_store(self):
        print(f"\nYou entered {self.chosen_store}, Thank you for choosing us!\n")
        choice = 0
        while choice != 3:
            print("What can we do for you?")
            print("1-View the list of products")
            print("2-Product search")
            print("3-quit this shop")
            try:
                choice = int(input("Choose an option: "))
                if not 1 <= choice <= 3:
                    raise Exception("There is not such an option!")
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in entering a store.")

            if choice == 1:
                ob = Product(self.chosen_store)
                ob.show_products_list("client")
            elif choice == 2:
                ob = Product(self.chosen_store)
                pre_invoice = ob.search_a_product()
                if pre_invoice:
                    self.add_to_pre_invoice(pre_invoice)

    def show_pre_invoice(self):
        pre_invoices = Customer.read_from_file('pre_invoice.csv')
        i, total_price = 1, 0
        print("\nYour all pre invoices: ")
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                print(f"{i} - From store {pre_invoice['shop_name']} {pre_invoice['number']}\
 {pre_invoice['name']} of brand {pre_invoice['brand']} with price {pre_invoice['payment']}.")
                i += 1
                total_price += float(pre_invoice['payment'])
        print(f"\nTotal price until now: {total_price} tooman.\n")

    def confirm(self):
        ob1 = FileHandler("pre_invoice.csv")
        pre_invoices = ob1.read_file()
        ob2 = FileHandler("invoices.csv")
        shop_list, total_price = [], 0
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                shopping = [pre_invoice['shop_name'], pre_invoice['name'],
                            pre_invoice['brand'], pre_invoice['number'], pre_invoice['payment']]
                total_price += float(pre_invoice['payment'])
                shop_list.append(shopping)
        new_invoice = {"date": [datetime.now().year, datetime.now().month, datetime.now().day],
                       "username": self.user_name, "purchase": shop_list,
                       "total_price": total_price}
        ob2.add_to_file(new_invoice)
        print(f"\nYour purchase with payment {new_invoice['total_price']}\
    tooman in {datetime.now()} recorded successfully!\n")
        logging.info(f"New invoice for client {new_invoice['username']} recorded.")

        headers = ["username", "shop_name", "name", "brand", "number", "payment"]
        with open("pre_invoice.csv", 'w') as my_file:
            writer = csv.DictWriter(my_file, fieldnames=headers)
            writer.writeheader()

        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                continue
            else:
                ob1.add_to_file(pre_invoice)
        print('\nYour purchase confirmed successfully!\n')

    def add_to_pre_invoice(self, pre_invoice):
        ob = FileHandler("pre_invoice.csv")
        new_pre_invoice = {"username": self.user_name, "shop_name": self.chosen_store,
                           "name": pre_invoice[0], "brand": pre_invoice[1], "number": pre_invoice[2],
                           "payment": pre_invoice[3]}
        ob.add_to_file(new_pre_invoice)
        print(f"from store {self.chosen_store}, {pre_invoice[2]} {pre_invoice[0]} of brand {pre_invoice[1]} with total\
 price {pre_invoice[3]} tooman was recorded for you.")

    def edit(self):
        ob = FileHandler("pre_invoice.csv")
        pre_invoices = ob.read_file()
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                print(f"{pre_invoice['number']} {pre_invoice['name']} of brand {pre_invoice['brand']} from shop\
 {pre_invoice['shop_name']} with price {pre_invoice['payment']} .")

        editing_shop = input("Which one do you want to delete? (name) ")

        headers = ["username", "shop_name", "name", "brand", "number", "payment"]
        with open("pre_invoice.csv", 'w') as my_file:
            writer = csv.DictWriter(my_file, fieldnames=headers)
            writer.writeheader()

        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name and pre_invoice['name'] == editing_shop:
                continue
            else:
                ob.add_to_file(pre_invoice)
        print("\nYour purchase edited successfully!\n")

    @staticmethod
    def read_from_file(file_name):
        ob = FileHandler(file_name)
        information = ob.read_file()
        return information
