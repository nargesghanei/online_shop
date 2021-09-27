import file_handler
from hashlib import sha256
import logging


# This class is for registering client and managers
class Register:
    def __init__(self):
        logging.basicConfig(filename='records.log', filemode='a',
                            format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        choice = 0
        self.role = None
        self.user_name = None
        self.pass_word = None
        self.pass_word_again = False
        self.hashed = None
        self.shop_name = None
        self.work_hour_m = None
        self.work_hour = None
        self.block_list = None
        while choice != 3:
            print("1-Register as a manager.")
            print("2-Register as a client.")
            print("3-Back.")
            print()
            try:
                choice = int(input("Please Enter your option:  "))
                if not 1 <= choice <= 3:    # choice is out of range
                    raise Exception("There is not such an option!")
            except Exception as error:
                print(f"{error}, Please Enter number between 1 to 3!")
                logging.error(f"{error}  , Happened in registering menu.")
            if choice == 1:
                self.role = "manager"
                self.managers_registration()
                choice = 3
            elif choice == 2:
                self.role = "client"
                self.clients_registration()
                choice = 3

    # This function is for registering a manager
    def managers_registration(self):
        all_true = True
        pass_again = False
        name_of_shop = False
        while all_true:      # while all things put in correct way
            if not self.user_name:     # if username was not added
                user_name = input("Please Enter your phone number as your user name: ")
                valid_user_name = Register.user_name_validation(user_name)
                if not valid_user_name:  # username was not valid go for first of loop
                    continue
                else:
                    self.user_name = user_name
            if not self.pass_word:        # if password was not added
                pass_word = input("Please Enter a password: ")
                valid_pass_word = self.pass_word_validation(pass_word)
                if not valid_pass_word:      # password was not valid go for first of loop
                    continue
                else:
                    self.pass_word = pass_word
                    result = sha256(self.pass_word.encode())       # hash the password
                    self.hashed = result.hexdigest()
            if not self.pass_word_again:    # if password again was not added
                password_again = input("Please Enter your password again: ")
                try:
                    if self.pass_word == password_again:
                        pass_again = True
                        print("Password saved successfully!")
                    else:      # pass again is not the same as first password
                        pass_again = False
                        raise Exception("Please enter the same password!")
                except Exception as error:
                    print(f"{error} Please try again!")
                    logging.error(f"{error}  , Happened in registering.")
                if not pass_again:   # password again was not true go for first of loop
                    continue
                else:
                    self.pass_word_again = True
            if not self.shop_name:         # if name was not added
                shop_name = input("Please Enter the name of your shop center: ")
                try:
                    if shop_name:
                        name_of_shop = True
                        print("Shop name accepted!")
                    else:
                        name_of_shop = False
                        raise Exception("You should at least enter sth!")
                except Exception as error:
                    print(f"{error} Please try again.")
                    logging.error(f"{error}  , Happened in registering.")
                if not name_of_shop:      # name was not valid go for first of loop
                    continue
                else:
                    self.shop_name = shop_name
            if not self.work_hour_m:    # if name was not added
                # get the open and close time in a special form
                work_hour = tuple(input("Enter the opening and closing time, (ex: 08:30,18:45): ").split(','))
                work_hour_last = Register.time_validate(work_hour[0], work_hour[1])
                if work_hour_last:
                    print("Work interval accepted!")
                    self.work_hour_m = work_hour_last
                    self.work_hour = work_hour
                    all_true = False
                else:
                    continue
        print(f"\nManager registered successfully with \nusername: {self.user_name}\
            \nshop name: {self.shop_name}\nwork_hour: {self.work_hour[0]} to {self.work_hour[1]}\n")
        self.add_to_file()     # all things added truly, add the store and manager to file
        logging.info(f"Store {self.shop_name} with manager {self.user_name} added.")

    # This function is for registering a manager
    def clients_registration(self):
        all_true = True
        pass_again = False
        while all_true:      # while all things put in correct way
            if not self.user_name:   # while all things put in correct way
                user_name = input("Please Enter your phone number as your user name: ")
                valid_user_name = Register.user_name_validation(user_name)
                if not valid_user_name:      # username was not valid go for first of loop
                    continue
                else:
                    self.user_name = user_name
            if not self.pass_word:          # if password was not added
                pass_word = input("Please Enter a password: ")
                valid_pass_word = self.pass_word_validation(pass_word)
                if not valid_pass_word:          # password was not valid go for first of loop
                    continue
                else:
                    self.pass_word = pass_word
                    result = sha256(self.pass_word.encode())     # hash the password
                    self.hashed = result.hexdigest()
            if not self.pass_word_again:      # if password again was not added
                password_again = input("Please Enter your password again: ")
                try:
                    if self.pass_word == password_again:     # pass again is not the same as first password
                        pass_again = True
                        print("Password saved successfully!")
                    else:
                        pass_again = False
                        raise Exception("Please enter the same password!")
                except Exception as error:
                    print(f"{error} Please try again!")
                    logging.error(f"{error}  , Happened in registering.")
                if not pass_again:   # password again was not true go for first of loop
                    continue
                else:
                    all_true = False
                    self.pass_word_again = True

        print(f"\nClient registered successfully with \nusername: {self.user_name}\n")
        self.add_to_file()     # all things added truly, add the client to file
        logging.info(f"Client with username {self.user_name} added.")

    # This function checks validation of username
    @staticmethod
    def user_name_validation(user_name):
        try:
            ob = file_handler.FileHandler("users.csv")
            users = ob.read_file()
            for user in users:
                if user["username"] == user_name:    # check if it was repeated
                    raise Exception("This username is already taken!")
            if user_name.isnumeric() and len(user_name) == 11:    # it should be phone number and 11 digits
                print("User name accepted!")
                return True
            else:
                raise Exception("Invalid username!")
        except Exception as error:
            print(f"{error}, Please try again!")
            logging.error(f"{error}  , Happened in registering.")
        return False

    # This function checks the validation of password
    @staticmethod
    def pass_word_validation(pass_word):
        val = True
        try:
            special_sym = ['$', '@', '#', '%', '_']     # should be one of these characters in pass

            # ALL THINGS THAT MAKE PASSWORD INVALID
            if len(pass_word) < 8:
                val = False
                raise Exception('Password should be at least 8 characters!')

            elif len(pass_word) > 20:
                val = False
                raise Exception('Password should not be greater than 20 characters!')

            elif not any(char.isdigit() for char in pass_word):
                val = False
                raise Exception('Password should have at least one numeral!')

            elif not any(char.isupper() for char in pass_word):
                val = False
                raise Exception('Password should have at least one uppercase letter')

            elif not any(char.islower() for char in pass_word):
                val = False
                raise Exception('Password should have at least one lowercase letter')

            elif not any(char in special_sym for char in pass_word):
                val = False
                raise Exception('Password should have at least one of the symbols $@#%_')

        except Exception as error:
            print(f"{error}, Please try again!")
            logging.error(f"{error}  , Happened in registering.")

        if val:
            print("Password accepted!")
        return val

    # This function checks the time validation
    @staticmethod
    def time_validate(opening, closing):
        try:
            # turn the time to minutes that it could easily compared
            time1 = list(map(int, opening.split(":")))
            opening = time1[0] * 60 + time1[1]
            time2 = list(map(int, closing.split(":")))
            closing = time2[0] * 60 + time2[1]
            # invalid numbers for time
            if (0 > time1[0] or time1[0] > 24 or 0 > time2[0] or time2[0] > 24
                    or 0 > time1[1] or time1[1] > 59 or 0 > time2[1] or time2[1] > 59):
                raise Exception("Invalid time")
            if opening > closing:
                raise Exception("Invalid range")
        except Exception as error:
            print(f"{error}. Please try again!")
            logging.error(f"{error}  , Happened in registering.")
            return False
        return opening, closing

    # add user to users file
    def add_to_file(self):
        new_user = {"role": self.role, "username": self.user_name,
                    "password": self.hashed, "shop_name": self.shop_name,
                    "work_time": self.work_hour_m, "work_hour": self.work_hour,
                    "block_list": self.block_list}
        try:
            ob = file_handler.FileHandler("users.csv")
            ob.add_to_file(new_user)
        except Exception as error:
            print(error)
            logging.error(f"{error}  , Happened in saving.")
