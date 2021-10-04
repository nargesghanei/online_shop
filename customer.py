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

    # This function shows access menu of the customer
    def show_customers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 5:  # 5 means quit
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
                self.show_previous_invoice()
            elif choice == 2:
                self.show_stores_list()
            elif choice == 3:
                self.search_store()
            elif choice == 4:
                print("\n1- Confirm a purchase")
                print("2- Edit your purchase")
                done, option = False, None
                while not done:  # until a right option be done
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

    # This function shows list of available stores
    def show_stores_list(self):
        self.available_stores = []
        shops = Customer.read_from_file('users.csv')
        current_time = datetime.now().hour * 60 + datetime.now().minute  # calculate the current time
        blocked_shops = []
        for user in shops:  # add name of shops that has been blocked this user to the list
            if user['username'] == self.user_name:
                blocked = user['block_list']
                blocked_shops = blocked.split('-')
                break
        print("\nHere is the list of stores that are available now: (searching...)\n")
        i = 1
        for shop in shops:
            if shop['role'] == 'manager':  # just show the stores
                work_time = eval(shop['work_time'])  # check if the work time of store includes current time
                if work_time[0] <= current_time <= work_time[1] and shop['shop_name'] not in blocked_shops:
                    print(f"Store number {i}: name: {shop['shop_name']}, work hours: {shop['work_hour']}")
                    self.available_stores.append(shop['shop_name'])  # add to available stores list
                    i += 1
        print()

    # This function searches a store that is available by name
    def search_store(self):
        self.show_stores_list()
        quitt = False
        print()
        while not quitt:  # until a shop be chose or client wants to quit
            try:
                chosen_store = input("Enter the store that you want to buy from or -1 to quit: ")
                if not chosen_store:  # nothing has been entered
                    raise Exception("You should enter a shop name!")
                if chosen_store not in self.available_stores and chosen_store != '-1':  # store is not available now
                    raise Exception("This store is not available!")
                if chosen_store == '-1':  # user wants to quit
                    quitt = True
                else:  # right shop name was input
                    quitt = True
                    self.chosen_store = chosen_store  # save the chosen store
                    print("Have a great shopping time!\n")
                    self.enter_to_a_store()
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in searching stores.")

    # This function handles the shopping stuff from chosen store
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
                if not 1 <= choice <= 3:  # out of range
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

    # This function shows all invoices of the customer till now
    def show_previous_invoice(self):
        invoices = Customer.read_from_file('invoices.csv')
        i, total_price = 1, 0
        print("\nYour all invoices: ")
        for invoice in invoices:
            if invoice['username'] == self.user_name:  # just invoices of this user
                for shop in eval(invoice['purchase']):  # for all purchases in an invoice
                    print(f"{i} - From store {shop[0]} {shop[3]} {shop[1]} of brand {shop[2]} with price {shop[4]}.")
                i += 1
                total_price += float(invoice['total_price'])  # calculate the final price of all purchases
        print(f"\nTotal price until now: {total_price} tooman.\n")

    # This function confirms a purchase and records it
    def confirm(self):
        ob1 = FileHandler("pre_invoice.csv")
        pre_invoices = ob1.read_file()
        ob2 = FileHandler("invoices.csv")
        shop_list, total_price = [], 0
        print("\nList of all stuff in your pre invoice:\n")
        for pre_invoice in pre_invoices:  # search in all pre invoices
            if pre_invoice['username'] == self.user_name:  # show pre invoices of this client
                shopping = [pre_invoice['shop_name'], pre_invoice['name'],
                            pre_invoice['brand'], pre_invoice['number'], pre_invoice['payment']]
                total_price += float(pre_invoice['payment'])
                shop_list.append(shopping)  # add this pre invoice to a list to be saved
                print(
                    f"From shop {shopping[0]} {shopping[3]} {shopping[1]} of brand {shopping[2]} with price {shopping[4]}")
        confirming = input("Do you want to confirm and pay?(y/n)").strip().lower()  # confirmed to be done
        if confirming == 'y':
            new_invoice = {"date": [datetime.now().year, datetime.now().month, datetime.now().day],
                           "username": self.user_name, "purchase": shop_list,
                           "total_price": total_price}
            ob2.add_to_file(new_invoice)  # add new invoice to file
            print(f"\nYour purchase with payment {new_invoice['total_price']}\
 tooman in {datetime.now()} recorded successfully!\n")
            logging.info(f"New invoice for client {new_invoice['username']} recorded.")

            # all this part is for deleting the pre invoice from file of pre invoices
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

    # This function add a unconfirmed purchase to pre invoices list
    def add_to_pre_invoice(self, pre_invoice):
        ob = FileHandler("pre_invoice.csv")
        new_pre_invoice = {"username": self.user_name, "shop_name": self.chosen_store,
                           "name": pre_invoice[0], "brand": pre_invoice[1], "number": pre_invoice[2],
                           "payment": pre_invoice[3]}
        ob.add_to_file(new_pre_invoice)
        print(f"from store {self.chosen_store}, {pre_invoice[2]} {pre_invoice[0]} of brand {pre_invoice[1]} with total\
 price {pre_invoice[3]} tooman was recorded for you.")

    # This function deletes a purchase from pre invoices file
    def edit(self):
        ob = FileHandler("pre_invoice.csv")
        pre_invoices = ob.read_file()
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:  # show pre invoices of this client
                print(f"{pre_invoice['number']} {pre_invoice['name']} of brand {pre_invoice['brand']} from shop\
 {pre_invoice['shop_name']} with price {pre_invoice['payment']} .")

        editing_shop = input("Which one do you want to delete? (name) ")  # choose one to delete
        # all this part is to delete the choice from file of pre invoices
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

    # This function reads a file and return info of that
    @staticmethod
    def read_from_file(file_name):
        ob = FileHandler(file_name)
        information = ob.read_file()
        return information
