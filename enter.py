import file_handler
from hashlib import sha256
import product


class Enter:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        result = sha256(self.password.encode())
        self.hashed = result.hexdigest()

    def check_enter(self):
        ob = file_handler.FileHandler("users.csv")
        users = ob.read_file()
        find = False
        try:
            for user in users:
                if user["username"] == self.username:
                    find = True
                    if user["password"] == self.hashed:
                        print("\nYou entered successfully!\n")
                        ob = product.Product(user["shop_name"])
                        ob.warning()
                        return user
                    else:
                        raise Exception("Incorrect password!")
            if not find:
                raise Exception("Incorrect username!")
        except Exception as error:
            print(f"{error} Please try again.")
        return False
