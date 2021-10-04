import file_handler
from hashlib import sha256
import logging
import product


def register():
    logging.basicConfig(filename='records.log', filemode='a', format='%(asctime)s  -  %(levelname)s - %(message)s',
                        level=logging.INFO)
    choice = 0
    while choice != 3:
        print("1-Register as a manager.")
        print("2-Register as a client.")
        print("3-Back.")
        print()
        try:
            choice = int(input("Please Enter your option:  "))
            if not 1 <= choice <= 3:  # choice is out of range
                raise Exception("There is not such an option!")
        except Exception as error:
            print(f"{error}, Please Enter number between 1 to 3!")
            logging.error(f"{error}  , Happened in registering menu.")
        if choice == 1:
            managers_registration()
            choice = 3
        elif choice == 2:
            clients_registration()
            choice = 3


# This function is for entering to users account
def check_enter(username, password):
    logging.basicConfig(filename='records.log', filemode='a', format='%(asctime)s  -  %(levelname)s - %(message)s',
                        level=logging.INFO)
    result = sha256(password.encode())  # hash password
    hashed = result.hexdigest()
    ob = file_handler.FileHandler("users.csv")
    users = ob.read_file()  # read the file of users
    find = False
    try:
        for user in users:
            if user["username"] == username:  # username found
                find = True
                if user["password"] == hashed:  # password is true
                    print("\nYou entered successfully!\n")
                    ob = product.Product(user["shop_name"])  # go to shopping class
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


# This function is for registering a manager
def managers_registration():
    role = "manager"
    user_name = None
    pass_word = None
    pass_word_again = False
    hashed = None
    shop_name = None
    work_hour_m = None
    work_hour = None
    block_list = None
    all_true = True
    pass_again = False
    name_of_shop = False
    while all_true:  # while all things put in correct way
        if not user_name:  # if username was not added
            username = input("Please Enter your phone number as your user name: ")
            valid_user_name = user_name_validation(username)
            if not valid_user_name:  # username was not valid go for first of loop
                continue
            else:
                user_name = username
        if not pass_word:  # if password was not added
            password = input("Please Enter a password: ")
            valid_pass_word = pass_word_validation(password)
            if not valid_pass_word:  # password was not valid go for first of loop
                continue
            else:
                pass_word = password
                result = sha256(pass_word.encode())  # hash the password
                hashed = result.hexdigest()
        if not pass_word_again:  # if password again was not added
            password_again = input("Please Enter your password again: ")
            try:
                if pass_word == password_again:
                    pass_again = True
                    print("Password saved successfully!")
                else:  # pass again is not the same as first password
                    pass_again = False
                    raise Exception("Please enter the same password!")
            except Exception as error:
                print(f"{error} Please try again!")
                logging.error(f"{error}  , Happened in registering.")
            if not pass_again:  # password again was not true go for first of loop
                continue
            else:
                pass_word_again = True
        if not shop_name:  # if name was not added
            shopname = input("Please Enter the name of your shop center: ")
            try:
                if shopname:
                    name_of_shop = True
                    print("Shop name accepted!")
                else:
                    name_of_shop = False
                    raise Exception("You should at least enter sth!")
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in registering.")
            if not name_of_shop:  # name was not valid go for first of loop
                continue
            else:
                shop_name = shopname
        if not work_hour_m:  # if name was not added
            # get the open and close time in a special form
            work_hour = tuple(input("Enter the opening and closing time, (ex: 08:30,18:45): ").split(','))
            work_hour_last = time_validate(work_hour[0], work_hour[1])
            if work_hour_last:
                print("Work interval accepted!")
                work_hour_m = work_hour_last
                work_hour = work_hour
                all_true = False
            else:
                continue
    print(f"\nManager registered successfully with \nusername: {user_name}\
        \nshop name: {shop_name}\nwork_hour: {work_hour[0]} to {work_hour[1]}\n")
    new_user = {"role": role, "username": user_name,
                "password": hashed, "shop_name": shop_name,
                "work_time": work_hour_m, "work_hour": work_hour,
                "block_list": block_list}
    add_to_file(new_user)  # all things added truly, add the store and manager to file
    logging.info(f"Store {shop_name} with manager {user_name} added.")


# This function is for registering a manager
def clients_registration():
    role = "client"
    user_name = None
    pass_word = None
    pass_word_again = False
    hashed = None
    shop_name = None
    work_hour_m = None
    work_hour = None
    block_list = None
    all_true = True
    pass_again = False
    while all_true:  # while all things put in correct way
        if not user_name:  # while all things put in correct way
            username = input("Please Enter your phone number as your user name: ")
            valid_user_name = user_name_validation(username)
            if not valid_user_name:  # username was not valid go for first of loop
                continue
            else:
                user_name = username
        if not pass_word:  # if password was not added
            password = input("Please Enter a password: ")
            valid_pass_word = pass_word_validation(password)
            if not valid_pass_word:  # password was not valid go for first of loop
                continue
            else:
                pass_word = password
                result = sha256(pass_word.encode())  # hash the password
                hashed = result.hexdigest()
        if not pass_word_again:  # if password again was not added
            password_again = input("Please Enter your password again: ")
            try:
                if pass_word == password_again:  # pass again is not the same as first password
                    pass_again = True
                    print("Password saved successfully!")
                else:
                    pass_again = False
                    raise Exception("Please enter the same password!")
            except Exception as error:
                print(f"{error} Please try again!")
                logging.error(f"{error}  , Happened in registering.")
            if not pass_again:  # password again was not true go for first of loop
                continue
            else:
                all_true = False
                pass_word_again = True

    print(f"\nClient registered successfully with \nusername: {user_name}\n")
    new_user = {"role": role, "username": user_name,
                "password": hashed, "shop_name": shop_name,
                "work_time": work_hour_m, "work_hour": work_hour,
                "block_list": block_list}
    add_to_file(new_user)  # all things added truly, add the client to file
    logging.info(f"Client with username {user_name} added.")


# This function checks validation of username
def user_name_validation(user_name):
    try:
        ob = file_handler.FileHandler("users.csv")
        users = ob.read_file()
        for user in users:
            if user["username"] == user_name:  # check if it was repeated
                raise Exception("This username is already taken!")
        if user_name.isnumeric() and len(user_name) == 11:  # it should be phone number and 11 digits
            print("User name accepted!")
            return True
        else:
            raise Exception("Invalid username!")
    except Exception as error:
        print(f"{error}, Please try again!")
        logging.error(f"{error}  , Happened in registering.")
    return False


# This function checks the validation of password
def pass_word_validation(pass_word):
    val = True
    try:
        special_sym = ['$', '@', '#', '%', '_']  # should be one of these characters in pass

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
def add_to_file(user):
    try:
        ob = file_handler.FileHandler("users.csv")
        ob.add_to_file(user)
    except Exception as error:
        print(error)
        logging.error(f"{error}  , Happened in saving.")
