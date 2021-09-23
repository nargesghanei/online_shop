import file_handler


class Buy:
    def __init__(self, shop_name):
        self.shop_name = shop_name

    def view_products(self):
        ob = file_handler.FileHandler('products.csv')
        products = ob.read_file()
        print("\nHere is the list of products in this store:\n")
        i = 1
        for product in products:
            if product['shop_name'] == self.shop_name:
                print(f"{i} - name: {product['name']} of brand: {product['brand']} with price: {product['price']} tooman.")
                i += 1
        print()

    def search_a_product(self):
        ob = file_handler.FileHandler('products.csv')
        products = ob.read_file()
        searched = False
        print()
        while not searched:
            try:
                base = input("In which base do you want to search(name/brand)? ")
                if base == 'name':
                    searched = 'name'
                elif base == 'brand':
                    searched = 'brand'
                else:
                    raise Exception("There is not such a search base!")
            except Exception as error:
                print(f"{error} Please try again.")
            if not searched:
                continue
            if searched == 'name':
                find = False
                name = input("Enter the name of product: ")
                if name:
                    print(f"\nList of all {name} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['name'] == name:
                            find = True
                            print(f"Of brand: {product['brand']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any {name} in this store.\n")
            elif searched == 'brand':
                find = False
                brand = input("Enter the brand of product: ")
                if brand:
                    print(f"\nList of all products with brand {brand} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['brand'] == brand:
                            find = True
                            print(f"name: {product['name']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any product  of brand {brand} in this store.\n")