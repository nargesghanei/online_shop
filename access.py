import product


class Access:
    def __init__(self, user):
        self.role = user["role"]
        self.user_name = user["username"]
        self.shop_name = user["shop_name"]
        self.work_time = user["work_time"]
        self.work_hour = user["work_hour"]

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
                pass
            elif choice == 6:
                pass
