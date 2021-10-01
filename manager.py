import logging
import product
from file_handler import FileHandler
import csv
from datetime import datetime


# This class handles accesses of manager
class Manager:
    def __init__(self, user):
        logging.basicConfig(filename='records.log', filemode='a', format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.role = user["role"]
        self.user_name = user["username"]
        self.shop_name = user["shop_name"]
        self.work_time = user["work_time"]
        self.work_hour = user["work_hour"]

    # Shows menu of accesses of manager
    def show_managers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 8:  # get choice until quitting
            print("1-Record product")
            print("2-Charge a product")
            print("3-View inventory")
            print("4-View customer purchase invoices")
            print("5-Invoice search")
            print("6-View customers list")
            print("7-Block a customer")
            print("8-Log out")
            try:
                choice = int(input("Choose an option: "))
                if not (1 <= choice <= 8):  # choice is out of range
                    raise Exception("There is not such an option!")
            except Exception as error:
                print(f"{error}. Please try again!")
                logging.error(f"{error} , Happened in mangers access menu.")

            if choice == 1:
                ob = product.Product(self.shop_name)
                ob.record_product()
            elif choice == 2:
                ob = product.Product(self.shop_name)
                ob.charge()
            elif choice == 3:
                ob = product.Product(self.shop_name)
                ob.show_products_list("manager")
            elif choice == 4:
                self.show_customers_invoices()
            elif choice == 5:
                self.invoice_search()
            elif choice == 6:
                Manager.show_customers_list()
            elif choice == 7:
                user_name = input("Enter the customers username: ")  # how wants to be blocked
                self.block(user_name)

    # Shows list of all customers
    @staticmethod
    def show_customers_list():
        ob = FileHandler("users.csv")
        users = ob.read_file()  # read from file of users
        i = 1  # counter
        print("\nAll customers list:\n")
        for user in users:
            if user["role"] == "client":  # if user is a client print it
                print(f"{i} - {user['username']}")
                i += 1
        print()

    # Block a user
    def block(self, username):
        ob = FileHandler("users.csv")
        users = ob.read_file()  # read users
        fields = ["role", "username", "password", "shop_name", "work_time", "work_hour", "block_list"]  # headers
        with open("users.csv", 'w') as my_file:  # rewrite the file to be updated
            writer = csv.DictWriter(my_file, fieldnames=fields)
            writer.writeheader()
            for user in users:
                if user['username'] != username:
                    ob.add_to_file(user)  # add all users again except blocked user
                else:
                    new_user = {"role": user['role'], "username": user['username'],
                                "password": user['password'], "shop_name": user['shop_name'],
                                "work_time": user['work_time'], "work_hour": user['work_hour'],
                                "block_list": f"{user['block_list']}-{self.shop_name}"}
                    # add name of shop to blocked list of user
        ob.add_to_file(new_user)  # append blocked user
        print(f"\nCustomer with id {username} is blocked from shop {self.shop_name} successfully!\n")

    # Shows invoices of all customers of users shop
    def show_customers_invoices(self):
        ob = FileHandler('invoices.csv')
        invoices = ob.read_file()
        start = True
        for invoice in invoices:
            start = True
            shops = eval(invoice['purchase'])
            for shop in shops:  # all bought stuff
                if shop[0] == self.shop_name:  # if buying is from users shop
                    if start:  # print username in first row
                        print(f"\nInvoices of client with username: {invoice['username']}:")
                        start = False
                        print(f"{shop[3]} {shop[1]} of brand {shop[2]} with total price {shop[4]}.")
                    else:
                        print(f"{shop[3]} {shop[1]} of brand {shop[2]} with total price {shop[4]}.")
        print()

    # This function searches invoices of clients base on date or username
    def invoice_search(self):
        ob = FileHandler('invoices.csv')
        invoices = ob.read_file()
        searched, choice = False, None
        while not searched:  # until get correct input
            try:
                print("\nSearching fields: ")
                print("1-Date")
                print("2-Username")
                choice = int(input("Please select one of the options: "))
                if not (1 <= choice <= 2):  # out of range
                    raise Exception("There is not such an option!")
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in searching invoices.")
            if choice == 1:  # search base on date
                date_done, date_obj = False, None
                date_format = '%Y-%m-%d'  # input format of date
                while not date_done:
                    try:
                        date = input("Enter the date (YYYY-MM-DD) : ")
                        date_obj = datetime.strptime(date, date_format)  # turn the input dated to a date object
                    except Exception as error:  # wrong format of input date
                        print(f"{error} Please try again!")
                        logging.error(f"{error}  , Happened in searching invoices.")
                    if not date_obj:  # if still did not get the right date
                        continue
                    else:
                        break
                searched, find = True, False
                date1 = [date_obj.year, date_obj.month, date_obj.day]  # search for today
                date2 = [date_obj.year, date_obj.month, date_obj.day - 1]  # search for yesterday
                for invoice in invoices:
                    # show invoices of today and yesterday
                    if eval(invoice['date']) == date1 or eval(invoice['date']) == date2:
                        for shop in eval(invoice['purchase']):
                            if shop[0] == self.shop_name:  # for invoices of this shop
                                print(
                                    f"Client with username {invoice['username']} had bought {shop[3]} {shop[1]} {shop[2]}\
with total payment of {shop[4]}\n")
                                find = True
                if not find:
                    print("There is not any invoices in this time.\n")
            elif choice == 2:  # search base on username
                searched, user_found, find = True, False, False
                username = input("Enter customer's username: ")

                for invoice in invoices:
                    if invoice['username'] == username:
                        user_found = True
                        for shop in eval(invoice['purchase']):
                            if shop[0] == self.shop_name:  # for invoices of this shop
                                print(f"Client in date {invoice['date']} had bought {shop[3]} {shop[1]} {shop[2]}\
with total payment of {shop[4]}\n")
                                find = True
                if not user_found:
                    print(f"Client with username {username} not found!")
                if (not find) and user_found:  # user was found but there is no invoices for this shop of this user
                    print("There is not any invoices for this user.\n")
