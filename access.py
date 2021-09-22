import product
import file_handler
import csv


class Access:
    def __init__(self, user):
        self.role = user["role"]
        self.user_name = user["username"]
        self.shop_name = user["shop_name"]
        self.work_time = user["work_time"]
        self.work_hour = user["work_hour"]
        self.block_list = user["block_list"]

    def show_access_menu(self):
        if self.role == "manager":
            self.show_managers_access()
        elif self.role == "client":
            pass

    def show_managers_access(self):
        print(f"\nYou are a {self.role}.\n")
        choice = 0
        while choice != 7:
            print("1-Record product")
            print("2-View inventory")
            print("3-View customer purchase invoices")
            print("4-Invoice Search")
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
                pass
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
