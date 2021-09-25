import product
import file_handler
import csv
from datetime import datetime
import buy


class Access:
    def __init__(self, user):
        self.role = user["role"]
        self.user_name = user["username"]
        self.shop_name = user["shop_name"]
        self.work_time = user["work_time"]
        self.work_hour = user["work_hour"]
        self.block_list = user["block_list"]
        self.available_stores = []
        self.chosen_store = None

    def show_access_menu(self):
        if self.role == "manager":
            self.show_managers_access()
        elif self.role == "client":
            self.show_customers_access()

    def show_managers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 7:
            print("1-Record product")
            print("2-View inventory")
            print("3-View customer purchase invoices")
            print("4-Invoice search")
            print("5-View customers list")
            print("6-Block a customer")
            print("7-Log out")
            try:
                choice = int(input("Choose an option: "))
            except Exception as error:
                print(f"{error}. Please try again!")

            if choice == 1:
                ob = product.Product(self.shop_name)
                ob.record_product()
            elif choice == 2:
                ob = product.Product(self.shop_name)
                ob.show_products_list()
            elif choice == 3:
                self.show_customers_invoices()
            elif choice == 4:
                pass
            elif choice == 5:
                Access.show_customers_list()
            elif choice == 6:
                user_name = input("Enter the customers username: ")
                self.block(user_name)

    @staticmethod
    def show_customers_list():
        ob = file_handler.FileHandler("users.csv")
        users = ob.read_file()
        i = 1
        print("\nAll customers list:\n")
        for user in users:
            if user["role"] == "client":
                print(f"{i} - {user['username']}")
                i += 1
        print()

    def block(self, username):
        ob = file_handler.FileHandler("users.csv")
        users = ob.read_file()
        fields = ["role", "username", "password", "shop_name", "work_time",
                  "work_hour", "block_list"]
        with open("users.csv", 'w') as my_file:
            writer = csv.DictWriter(my_file, fieldnames=fields)
            writer.writeheader()
            for user in users:
                if user['username'] != username:
                    ob.add_to_file(user)
                else:
                    new_user = {"role": user['role'], "username": user['username'],
                                "password": user['password'], "shop_name": user['shop_name'],
                                "work_time": user['work_time'], "work_hour": user['work_hour'],
                                "block_list": f"{user['block_list']}-{self.shop_name}"}
        ob.add_to_file(new_user)
        print(f"\nCustomer with id {username} is blocked from shop {self.shop_name} successfully!\n")

    def show_customers_invoices(self):
        ob = file_handler.FileHandler('invoices.csv')
        invoices = ob.read_file()
        start = True
        for invoice in invoices:
            start = True
            shops = eval(invoice['purchase'])
            for shop in shops:
                if shop[0] == self.shop_name:
                    if start:
                        print(f"\nInvoices of client with username: {invoice['username']}:")
                        start = False
                        print(f"{shop[3]} {shop[1]} of brand {shop[2]} with total price {shop[4]}.")
                    else:
                        print(f"{shop[3]} {shop[1]} of brand {shop[2]} with total price {shop[4]}.")


    def show_customers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 5:
            print("1-View previous invoices")
            print("2-View list of stores")
            print("3-Store search")
            print("4-Select a store")
            print("5-Log out")
            try:
                choice = int(input("Choose an option: "))
            except Exception as error:
                print(f"{error}. Please try again!")

            if choice == 1:
                pass
            elif choice == 2:
                self.show_stores_list()
            elif choice == 3:
                self.search_store()
            elif choice == 4:
                self.enter_to_a_store()
            elif choice == 5:
                self.show_pre_invoice()
            elif choice == 6:
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

    def show_stores_list(self):
        ob = file_handler.FileHandler('users.csv')
        shops = ob.read_file()
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
        quit = False
        print()
        while not quit:
            try:
                chosen_store = input("Enter the store that you want to buy from: ")
                if not chosen_store:
                    raise Exception("You should enter a shop name!")
                if chosen_store not in self.available_stores:
                    raise Exception("This store is not available!")
                else:
                    quit = True
                    self.chosen_store = chosen_store
                    print("Have a great shopping time!\n")
            except Exception as error:
                print(f"{error} Please try again.")

    def enter_to_a_store(self):
        print(f"\nYou entered {self.chosen_store}, Thank you for choosing us!\n")
        choice = 0
        while choice != 4:
            print("What can we do for you?")
            print("1-View the list of products")
            print("2-Product search")
            print("3-Confirm purchase or edit")
            print("4-quit this shop")
            try:
                choice = int(input("Choose an option: "))
                if not 1 <= choice <= 6:
                    raise Exception("There is not such an option!")
            except Exception as error:
                print(f"{error} Please try again.")

            if choice == 1:
                ob = buy.Buy(self.chosen_store, self.user_name)
                ob.view_products()
            elif choice == 2:
                ob = buy.Buy(self.chosen_store, self.user_name)
                ob.search_a_product()
            elif choice == 3:
                pass

    def show_pre_invoice(self):
        ob = file_handler.FileHandler("pre_invoice.csv")
        pre_invoices = ob.read_file()
        i, total_price = 1, 0
        print("\nYour all pre invoices: ")
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                print(f"{i} - From store {pre_invoice['shop_name']} {pre_invoice['number']}\
 {pre_invoice['name']} of brand {pre_invoice['brand']} with price {pre_invoice['payment']}.")
                i += 1
                total_price += float(pre_invoice['payment'])
        print(f"\nTotal price untill now: {total_price} tooman.\n")

    def confirm(self):
        ob1 = file_handler.FileHandler("pre_invoice.csv")
        pre_invoices = ob1.read_file()
        ob2 = file_handler.FileHandler("invoices.csv")
        shop_list, total_price = [], 0
        for pre_invoice in pre_invoices:
            if pre_invoice['username'] == self.user_name:
                shopping = [pre_invoice['shop_name'], pre_invoice['name'],
                            pre_invoice['brand'], pre_invoice['number'], pre_invoice['payment']]
                total_price += float(pre_invoice['payment'])
                shop_list.append(shopping)
        new_invoice = {"username": self.user_name, "purchase": shop_list,
                       "total_price": total_price}
        ob2.add_to_file(new_invoice)
