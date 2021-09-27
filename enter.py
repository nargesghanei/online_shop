import file_handler
from hashlib import sha256
import product
import logging


# This class is for entering to users account
class Enter:
    def __init__(self, username, password):
        logging.basicConfig(filename='records.log', filemode='a',
                            format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.username = username
        self.password = password
        result = sha256(self.password.encode())   # hash password
        self.hashed = result.hexdigest()

    # Check the users info
    def check_enter(self):
        ob = file_handler.FileHandler("users.csv")
        users = ob.read_file()    # read the file of users
        find = False
        try:
            for user in users:
                if user["username"] == self.username:   # username found
                    find = True
                    if user["password"] == self.hashed:    # password is true
                        print("\nYou entered successfully!\n")
                        ob = product.Product(user["shop_name"])      # go to shopping class
                        ob.warning()
                        return user
                    else:
                        raise Exception("Incorrect password!")
            if not find:
                raise Exception("Incorrect username!")
        except Exception as error:
            print(f"{error} Please try again.")
            logging.error(f"{error}  , Happened in checking enter.")
        return False
