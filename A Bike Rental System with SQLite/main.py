import datetime
import random
import sqlite3
import time


class Database:

    def __init__(self):
        self.bike_id = 0
        self.connect_database()

    def connect_database(self):
        # Connected to the database
        self.connect = sqlite3.connect("bike_rental.db")
        self.cursor = self.connect.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,name TEXT,speed TEXT,typ TEXT,stock INT,price INT)")

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS order_history(id INTEGER PRIMARY KEY,bike_id INT,order_typ TEXT,order_time TEXT,name TEXT,speed TEXT,typ TEXT,piece INT,unit_price INT,total_price INT)")

        self.connect.commit()

    def get_latest_id(self, table_name):
        # Returns last id, we need this to make user not to try to buy or choose bike never existed
        self.cursor.execute(f"SELECT MAX(id) FROM {table_name}")

        self.latest_id = self.cursor.fetchall()[0][0]

        return self.latest_id


class Shop(Database):

    def __init__(self, name):
        super().__init__()
        self.name = name
        # self.exit_id = []
        # self.info_id = []

    def welcome(self):

        # Prints bikes to the screen
        welcome_message = f"WELCOME TO {self.name}'S BIKE SHOP".upper()
        print(welcome_message)
        print("-" * len(welcome_message))
        print("\033[93mYou can choose a perfect bike that you want. Explore the Bike World !\033[m")

        while True:

            self.cursor.execute("SELECT * FROM products")

            all_products = self.cursor.fetchall()

            convert_all_str = lambda x: [str(y) for y in x]

            title = "NO  |-- ID --| |----- NAME -----| |-- SPEED LEVEL --| |------ TYPE ------| |---- STOCK ----| |------- PRICE -------|"
            print("-" * len(title))
            print(title)
            for i, j in enumerate(all_products, start=1):
                print("{} -   {}".format(i, "              ".join(convert_all_str(j))), "TRY")

            print("-" * len(title))
            return all_products

    def add_products(self, data_type, var1, var2, var3, text):
        # adds values to database by their variable type
        if data_type == "string":

            while True:

                product_value = input(text).lower().title()

                if product_value == var1 or product_value == var2 or product_value == var3:
                    break
                else:
                    print("You entered invalid value. Please enter one of the options")
                    continue

            return product_value


        elif data_type == "integer":

            while True:

                try:
                    product_value = int(input(text))

                    if product_value < 0:
                        print("Please enter value more than '-1'")
                        continue
                    break
                except ValueError:
                    print("You entered invalid value. Please enter integer number")

            return product_value

    def add_random_products(self):

        # adds values randomly to table by given values

        name = ["Moon", "Knight", "Star", "Light", "Bear", "Sun"]
        speed = ["Slow", "Medium", "Fast"]
        typ = ["Daily Life", "Race", "Mountain"]
        stock = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        price = [3999, 4999, 5999, 6999, 7999, 8999]
        for i in range(6):
            database.cursor.execute("INSERT INTO products ('name','speed','typ',stock,price) VALUES (?,?,?,?,?)",
                                    (
                                        name[i], random.choice(speed), random.choice(typ), random.choice(stock),
                                        random.choice(price),))

            database.connect.commit()

    def get_any_info(self, info_name, info_id, table_name):
        # for example, we can get stock or cost value from database
        self.cursor.execute(f"SELECT {info_name} FROM {table_name} WHERE id = ?", (info_id,))

        result = self.cursor.fetchall()[0][0]
        # for example, product with ID = 3 has 15 stocks

        return result

    def update_any_info(self, info_type, info_name, info_id, table_name, new_value):
        # for example, we can update stock or cost value
        if info_type == "integer":
            self.cursor.execute(f"UPDATE {table_name} SET {info_name} = {new_value} WHERE id = ?", (info_id,))


        elif info_type == "string":
            self.cursor.execute(f"UPDATE {table_name} SET {info_name} = '{new_value}' WHERE id = ?", (info_id,))

        self.connect.commit()


class Money_Machine(Database):
    CURRENCY = "TRY"

    TRY_BANKNOTE_VALUES = {
        "200 TRY": 200,
        "100 TRY": 100,
        "50 TRY": 50,
        "20 TRY": 20,
        "10 TRY": 10,
        "5 TRY": 5,
        "1 TRY": 1
    }

    def __init__(self):
        self.money_received = 0
        self.profit = 0
        super().__init__()

    def process_coins(self, cost):

        # returns the total calculated from banknotes and coins inserted
        # if amount of inserted coins or banknotes is equal to cost during loop
        # it stops the loop, so user doesn't need to insert more coins.

        for banknote in self.TRY_BANKNOTE_VALUES:

            number_of_money = round(cost / self.TRY_BANKNOTE_VALUES[banknote])

            if number_of_money > 0:
                print("-" * 35)
                while True:
                    try:
                        money_received = int(
                            input(f"(You can pay with {number_of_money} banknotes)\nHow many {banknote} ?: ")) * \
                                         self.TRY_BANKNOTE_VALUES[banknote]
                        if money_received < 0:
                            print("\033[31mError. You can't enter value less than zero!\033[m")
                            continue
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")
                self.money_received += money_received
                cost -= money_received

            # For example, If product costs 15999

            # How many 200 TRY ?
            # You have to pay with 80 200 TRY bills:  ( 200 * 80 = 16000 )

            # How many 100 TRY ?
            # .....
        return self.money_received

    def make_payment(self, cost):
        self.process_coins(cost)
        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            print(f"\033[93mHere is {change:,.2f} {self.CURRENCY} in change.\033[m")
            self.profit += cost
            self.money_received = 0
            return True
        else:
            print("\033[33mSorry that's not enough money. Money refunded.\033[m")
            self.money_received = 0
            return False

    # def show_summary(self, order_id, total_cost, how_many, order_time):
    #
    #     forewords = [
    #         "Bike ID: ",
    #         "Bike name: ",
    #         "Speed level of bike: ",
    #         "Type of bike: ",
    #         "Bike total stock: ",
    #         "Unit price: ",
    #         "Total bike received: ",
    #         "Total price: ",
    #         "Order time: "
    #     ]
    #
    #     self.cursor.execute(f"SELECT id,name,speed,typ,stock,price FROM products WHERE id = ?",(order_id,))
    #     values = list(self.cursor.fetchone())
    #     values2 = [how_many, total_cost, order_time]
    #     k = 1
    #     for i in values + values2:
    #         print(f"{k} - {forewords[k - 1]}{i}")
    #         if k == 9:
    #             break
    #         k += 1


class Order_History(Database):

    def __init__(self):
        super().__init__()

    def menu(self):
        while True:

            self.cursor.execute("SELECT id,bike_id,order_typ,order_time,name,piece FROM order_history")

            all_products = self.cursor.fetchall()

            convert_all_str = lambda x: [str(y) for y in x]

            title = "|- ORDER ID -|  |- BIKE ID -| |--- ORDER TYPE ---| |------- ORDER TIME -------| |------ NAME ------| |- ORDER QUANTITY -|"

            print("-" * len(title))
            print(title)
            for i in all_products:
                print("        {}".format("            ".join(convert_all_str(i))))

            print("-" * len(title))
            return all_products

    def show_order_history(self, id, id_type):

        forewords = [
            "Order ID: ",
            "Bike ID: ",
            # (Purchase/Rent/Cancel/Return)
            "Order type: ",
            "Order time: ",
            "Bike name: ",
            "Speed level of bike: ",
            "Type of bike: ",
            "Number of pieces: ",
            "Unit price: ",
            "Total price: ",
        ]
        if id_type == "Order ID":

            self.cursor.execute(
                f"SELECT * FROM order_history WHERE id = ?", (id,))

        elif id_type == "Bike ID":
            self.cursor.execute(
                f"SELECT * FROM order_history WHERE bike_id = ?", (id,))

        values = list(self.cursor.fetchone())
        # values2 = [how_many, total_cost]
        k = 1
        for i in values:
            print(f"{k} - {forewords[k - 1]}{i}")
            if k == 10:
                break
            k += 1


database = Database()
bike_shop = Shop("GURUR")
money_machine = Money_Machine()
order_history = Order_History()

is_active = True
while is_active:

    # # adds values randomly to table by given values
    # bike_shop.add_random_products()

    while True:

        if not bike_shop.welcome():

            print("\033[33mUnfortunately, there is no product. Would you like to add some ? (Yes/No)\033[m")
            while True:
                answer = input("Enter your answer: ")
                if answer.lower().capitalize() == "No":
                    print("Okay...")
                    break

                if answer.lower().capitalize() == "Yes":
                    product_name = input("Enter the name of the product: ")
                    # this variable does not meet the requirements of the function I wrote, so I wrote it separately
                    product_speed = bike_shop.add_products(
                        data_type="string",
                        var1="Slow",
                        var2="Medium",
                        var3="Fast",
                        text="Enter the speed level of the product(Slow/Medium/Fast): "
                    )
                    product_type = bike_shop.add_products(
                        data_type="string",
                        var1="Daily Life",
                        var2="Race",
                        var3="Mountain",
                        text="Enter the type of the product(Daily Life/Race/Mountain): "
                    )
                    product_stock = bike_shop.add_products(
                        data_type="integer",
                        var1=None,
                        var2=None,
                        var3=None,
                        text="Enter the stock quantity of the product: "
                    )
                    product_cost = bike_shop.add_products(
                        data_type="integer",
                        var1=None,
                        var2=None,
                        var3=None,
                        text="Enter the price of the product: "
                    )
                    database.cursor.execute(
                        "INSERT INTO products ('name','speed','typ',stock,price) VALUES (?,?,?,?,?)",
                        (product_name, product_speed, product_type, product_stock, product_cost,))

                    database.connect.commit()
                    print(
                        f"\033[1;32mThe registration of the product named {product_name} has been successfully completed.\033[m")

                else:
                    print("You entered invalid answer. Please try again.")
                    continue
            break

        # if there is bike in database, these codes work

        print('''                  
                                    -------------------------------------- 
                                   |                                      |
                                   |    What would you like to do ?       |
                                   |    1 - Buy Bike                      |
                                   |    2 - Rent Bike                     | 
                                   |    3 - Show My Order History         |
                                   |    Write 'Exit' to close program     |
                                   |                                      |
                                    --------------------------------------
        ''')

        choice = input("Enter your choice: ").lower().capitalize()
        match choice:
            # Buy a bike
            case "1":
                while True:
                    try:
                        # rent a bike
                        bike_id = int(input("Enter ID of product that you want to buy: "))

                        if bike_id > database.get_latest_id("products") or bike_id <= 0:
                            print("\033[31mError. Please choose an available option.\033[m")
                        break
                    except ValueError:
                        print("\033[31mError. You entered invalid value\033[m")

                stock_info = bike_shop.get_any_info(info_name="stock", info_id=bike_id, table_name="products")
                price_info = bike_shop.get_any_info(info_name="price", info_id=bike_id, table_name="products")
                name_info = bike_shop.get_any_info(info_name="name", info_id=bike_id, table_name="products")
                typ_info = bike_shop.get_any_info(info_name="typ", info_id=bike_id, table_name="products")
                speed_info = bike_shop.get_any_info(info_name="speed", info_id=bike_id, table_name="products")

                while True:
                    try:
                        print(f"Current stock is : {stock_info}")
                        how_many = int(input("How many bikes would you like to buy ?: "))

                        if how_many > stock_info:
                            print("\033[31mError. You can't buy more than current stock.\033[m")
                            # print(f"Current stock is : {stock_info}")
                            continue
                        if how_many == 0:
                            print("You didn't buy any bike. Returning back to the main menu")

                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")

                total_cost = price_info * how_many
                # this code makes 'total cost' yellow
                total_cost_yellow = f"\033[93m{total_cost:,.2f}\033[m"

                print(f"{how_many} {name_info} cost {total_cost_yellow} {money_machine.CURRENCY}")

                sufficient_money = money_machine.make_payment(total_cost)

                if sufficient_money and stock_info >= how_many:
                    print("\033[32mDone! We are preparing your bike now. Please wait.\033[m")
                    time.sleep(2)
                    # executes the following codes after 2 seconds

                    print("-" * 35)
                    print("\033[32mYour order has been shipped.\033[m")
                    print("-" * 35)
                    print("-" * 35)
                    print("\033[93mEstimated time of arrival : 1 Day\033[m")
                    print("-" * 35)

                    # We are updating stocks
                    updated_stock = stock_info - how_many
                    bike_shop.update_any_info(
                        info_type="integer", info_name="stock", info_id=bike_id, table_name="products",
                        new_value=updated_stock)

                    # We record the date and time of receipt of the product
                    today = datetime.datetime.today()
                    today_format = today.strftime("%d/%m/%Y %H:%M:%S")
                    # Like this  12/08/2022 15:30:05

                    # We are entering values to order history to check them whenever we want
                    database.cursor.execute(
                        "INSERT INTO order_history (bike_id,'order_typ','order_time','name','speed','typ',piece,unit_price,total_price) VALUES (?,?,?,?,?,?,?,?,?)",
                        (bike_id, "Purchase", today_format, name_info, speed_info, typ_info, how_many, price_info,
                         total_cost))

                    # updating data
                    database.connect.commit()

                    # I assignn it to the variable of the superclass so that I can use it in different places whenever I want
                    database.bike_id = bike_id

                    print("\033[32mThank you for choosing us\033[m")
                    choice3 = input("Press enter any value to continue: ")
                    print("-" * 110)
                    continue

            case "2":
                while True:
                    try:
                        # rent a bike
                        bike_id = int(input("Enter ID of product that you want to rent: "))

                        if bike_id > database.get_latest_id("products") or bike_id <= 0:
                            print("\033[31mError. Please choose an available option.\033[m")
                        break
                    except ValueError:
                        print("\033[31mError. You entered invalid value\033[m")

                stock_info = bike_shop.get_any_info(info_name="stock", info_id=bike_id, table_name="products")
                price_info = bike_shop.get_any_info(info_name="price", info_id=bike_id, table_name="products")
                name_info = bike_shop.get_any_info(info_name="name", info_id=bike_id, table_name="products")
                typ_info = bike_shop.get_any_info(info_name="typ", info_id=bike_id, table_name="products")
                speed_info = bike_shop.get_any_info(info_name="speed", info_id=bike_id, table_name="products")

                while True:
                    try:
                        print(f"\033[93mCurrent stock is : {stock_info}\033[m")
                        how_many = int(input("How many bikes would you like to rent ?: "))
                        if how_many > stock_info:
                            print("\033[31mError. You can't rent more than current stock.\033[m")
                            # print(f"\033[93mCurrent stock is : {stock_info}\033[m")
                            continue
                        if how_many == 0:
                            print("You didn't rent any bike. Returning back to the main menu")
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")

                while True:
                    service_selection = input(
                        "Which rental service would you like to use?( Hourly / Daily ): ").lower().capitalize()

                    if service_selection == "Hourly":
                        order_type = "Rent(Hourly)"
                        # this code makes 'total cost' yellow
                        # I equated the hourly rate to 0.5 percent of the product's selling price (an hour)
                        total_rent_cost = (price_info * how_many) / 200
                        total_rent_cost_yellow = f"\033[93m{total_rent_cost}\033[m"
                        print(f"{how_many} {name_info} cost {total_rent_cost_yellow} {money_machine.CURRENCY} an hour")
                        break
                    elif service_selection == "Daily":
                        order_type = "Rent(Daily)"
                        # this code makes 'total cost' yellow
                        # I equated the daily rate to 0.4 percent of the product's selling price (an hour)
                        # I want to get one day price that's why I multiply it with 24
                        total_rent_cost = (price_info * how_many) / 250
                        total_rent_cost_yellow = f"\033[93m{(total_rent_cost * 24)}\033[m"
                        print(f"{how_many} {name_info} cost {total_rent_cost_yellow} {money_machine.CURRENCY} per day")
                        break
                    else:
                        print("\033[31mError. Please choose an available option.\033[m")

                print("\033[32mDone! We are preparing your bike now. Please wait.\033[m")
                time.sleep(2)
                # executes the following codes after 2 seconds

                print("-" * 35)
                print("\033[32mYou can get it from our bike vending machines.\033[m")
                print("-" * 35)

                print("-" * 35)
                print("\033[32mYou will pay, when you return the bike.\033[m")
                print("-" * 35)

                print("-" * 35)
                print("For more information, you can visit 'Show My Order History' section.")
                print("-" * 35)

                # We are updating stocks
                updated_stock = stock_info - how_many
                bike_shop.update_any_info(
                    info_type="integer", info_name="stock", info_id=bike_id, table_name="products",
                    new_value=updated_stock)

                # We record the date and time of receipt of the product
                today = datetime.datetime.today()
                today_format = today.strftime("%d/%m/%Y %H:%M:%S")

                # We are entering values to order history to check them whenever we want
                database.cursor.execute(
                    "INSERT INTO order_history (bike_id,'order_typ','order_time','name','speed','typ',piece,unit_price,total_price) VALUES (?,?,?,?,?,?,?,?,?)",
                    (bike_id, order_type, today_format, name_info, speed_info, typ_info, how_many, price_info,
                     total_rent_cost))

                # updating data
                database.connect.commit()

                # I assign it to the variable of the superclass so that I can use it in different places whenever I want
                database.bike_id = bike_id

                print("\033[32mThank you for choosing us\033[m")
                choice3 = input("Press enter any value to continue: ")
                print("-" * 110)
                continue

            case "3":
                print("-" * 19)
                print("\033[95mYOUR ORDER HISTORY: \033[m")
                print("-" * 19)
                print("\033[93mFrom this section, you can find all information about your orders.\033[m")
                print("\033[93mEnter 'ORDER ID' of order history that you want to see more detailed.\033[m")

                if not order_history.menu():
                    print(("*" * 45).center(90))
                    print("You didn't buy anything yet.".center(90))
                    print("Let's go to the main page,".center(90))
                    print("and meet with the bike of your dreams :)".center(90))
                    print(("*" * 45).center(90))

                # Show order history without details
                while True:
                    try:
                        choice = int(input("Enter ORDER ID to see details( Enter '0' to return back to the menu ): "))

                        if choice == 0:
                            break

                        # We avoid errors
                        if choice > database.get_latest_id("order_history") or choice < 0:
                            print("\033[31mError. Please choose an available option.\033[m")
                            continue
                        print("-" * 40)
                        # Show order history with details by chosen ID
                        order_history.show_order_history(id_type="Order ID", id=choice)
                        print("-" * 40)
                        while True:
                            print("\033[93mWhat would you like to do ?\n\033[m"
                                  "1 - Return my bike( Only for purchased bikes )\n"
                                  "2 - Pay for the bike( Only for rented bikes )\n"
                                  "3 - Exit\n")
                            choice4 = input("Enter your choice: ")

                            order_info = bike_shop.get_any_info(info_name="order_typ", info_id=choice,
                                                                table_name="order_history")
                            price_info = bike_shop.get_any_info(info_name="total_price", info_id=choice,
                                                                table_name="order_history")
                            name_info = bike_shop.get_any_info(info_name="name", info_id=choice,
                                                               table_name="order_history")
                            typ_info = bike_shop.get_any_info(info_name="typ", info_id=choice,
                                                              table_name="order_history")
                            speed_info = bike_shop.get_any_info(info_name="speed", info_id=choice,
                                                                table_name="order_history")
                            piece_info = bike_shop.get_any_info(info_name="piece", info_id=choice,
                                                                table_name="order_history")
                            bike_id = bike_shop.get_any_info(info_name="bike_id", info_id=choice,
                                                             table_name="order_history")

                            total_price = bike_shop.get_any_info(info_name="total_price", info_id=choice,
                                                                 table_name="order_history")
                            # It can be full price like 7999 or hourly or daily rate

                            stock_info = bike_shop.get_any_info(info_name="stock", info_id=bike_id,
                                                                table_name="products")

                            # Return purchased bikes
                            if choice4 == "1" and order_info == "Purchase":
                                # In this section, we only want the products purchased to be returned.

                                print(f"Do you want to return back to {piece_info} bikes called {name_info} ?")
                                print(f"You will be paid {price_info:,.2f} TRY in total")
                                print("Would you like to pay it now ?")
                                yes_no = input("Enter your answer( Yes/No ): ")
                                if yes_no.lower().capitalize() == "Yes":
                                    # return the bike
                                    bike_shop.update_any_info(info_type="integer", info_name="stock", info_id=bike_id,
                                                              table_name="products",
                                                              new_value=(stock_info + piece_info))
                                    database.cursor.execute(f"DELETE FROM order_history WHERE id = {choice}")
                                    database.connect.commit()
                                    print(f"\033[1;32mYou have successfully returned your product!\033[m")

                                break

                            # Bring back rented bikes
                            elif choice4 == "2" and order_info != "Purchase":
                                now = datetime.datetime.now()
                                # Getting order time
                                order_time_info = bike_shop.get_any_info(info_name="order_time", info_id=choice,
                                                                         table_name="order_history")

                                d1 = datetime.datetime.strptime(order_time_info, "%d/%m/%Y %H:%M:%S")
                                delta = now - d1
                                hours = int(delta.seconds / (60 * 60))
                                # For example 2 hours
                                minutes = int(delta.seconds / 60)
                                # For example 163 minutes

                                minutes_2 = minutes % 60
                                # I don't want to print it like 2 hours 163 minutes, so I wrote it.
                                # It divides minutes by sixty and prints the remainder in minutes

                                # If you want to see how total_price is calculated go to line 508
                                total_rent_cost = total_price * (minutes / 60)
                                total_rent_cost_yellow = f"\033[93m{total_rent_cost}\033[m"
                                print(
                                    f"{piece_info} {name_info} cost {total_rent_cost_yellow} {money_machine.CURRENCY} for {hours} hours {minutes_2} minutes")
                                print("Would you like to pay it now ?")
                                yes_no = input("Enter your answer( Yes/No ): ")
                                if yes_no.lower().capitalize() == "Yes":
                                    sufficient_money = money_machine.make_payment(total_rent_cost)
                                    if sufficient_money:
                                        # We are updating stocks
                                        bike_shop.update_any_info(info_type="integer", info_name="stock",
                                                                  info_id=bike_id,
                                                                  table_name="products",
                                                                  new_value=(stock_info + piece_info))
                                        database.cursor.execute(f"DELETE FROM order_history WHERE id = {choice}")
                                        database.connect.commit()

                                        print(
                                            "\033[32mDone! I hope you enjoyed! We would love to see you again !\033[m")
                                    break
                                break
                            elif choice4 == "3":
                                print("You've returned back to the menu.")
                                break
                            else:
                                print("\033[31mYou entered invalid value. Please enter one of the options.\033[m")
                                continue


                    except ValueError:
                        print("\033[31mYou entered invalid value. Please enter integer number\033[m")

            case "Exit":
                print("\033[1;32mYou've successfully exited from the program.\033[m")
                break
            case _:
                print("\033[31mYou entered invalid value. Please enter one of the options.\033[m")
                continue

    break
