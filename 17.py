# Product and Book classes with inheritance
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.price} USD, {self.quantity} items'


class Book(Product):
    def __init__(self, name, price, quantity, author):
        super().__init__(name, price, quantity)
        self.author = author

    def read(self):
        return f'{self.name} by {self.author}, {self.price} USD,\
 {self.quantity} items'


def test_book():
    The_Martian_Chronicles = Book('The Martian Chronicles', 8.99, 12,
                                  'Ray Bradbury')

    res = The_Martian_Chronicles.author
    assert res == 'Ray Bradbury'

    res = The_Martian_Chronicles.read()
    assert res == 'The Martian Chronicles by Ray Bradbury, 8.99 USD, 12 items'

    res = str(The_Martian_Chronicles)
    assert res == 'The Martian Chronicles, 8.99 USD, 12 items'


test_book()


# Restaurant and FastFood classes with menu management
class Restorant:
    def __init__(self, name, cuisine, menu: dict):
        self.name = name
        self.cuisine = cuisine
        self.menu = menu


class FastFood(Restorant):
    def __init__(self, name, cuisine, menu: dict, drive_thru: bool):
        super().__init__(name, cuisine, menu)
        self.drive_thru = drive_thru

    def order(self, dish_name, requested_quantity):
        if dish_name not in self.menu:
            raise ValueError(f"{str(dish_name).capitalize()} isn't on the\
 menu.")
        elif self.menu[dish_name]['quantity'] == 0:
            raise ValueError(f"{str(dish_name).capitalize()} isn't available.")
        elif self.menu[dish_name]['quantity'] < requested_quantity:
            raise ValueError(f"The requested quantity isn't available, there\
 are {self.menu[dish_name]['quantity']} units.")
        else:
            self.menu[dish_name]['quantity'] -= requested_quantity
            return requested_quantity * self.menu[dish_name]['price']


def test_menu_management():
    menu = {
        'burger': {'price': 5, 'quantity': 10},
        'pizza': {'price': 10, 'quantity': 20},
        'drink': {'price': 1, 'quantity': 15}
    }

    mc = FastFood('McDonalds', 'Fast Food', menu, True)

    res = mc.order('burger', 5)
    assert res == 25

    try:
        res = mc.order('burger', 15)
    except ValueError as e:
        res = e.args[0]
    assert res == "The requested quantity isn't available, there are 5 units."

    res = mc.order('burger', 5)
    assert res == 25

    try:
        res = mc.order('burger', 5)
    except ValueError as e:
        res = e.args[0]
    assert res == "Burger isn't available."

    try:
        res = mc.order('soup', 5)
    except ValueError as e:
        res = e.args[0]
    assert res == "Soup isn't on the menu."


test_menu_management()


# A Bank
class Account:
    def __init__(self, balance, account_number):
        self._balance = balance
        self._account_number = account_number

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError('Amount must be positive')

    def withdraw(self, amount):
        if amount > 0:
            self._balance -= amount
        else:
            raise ValueError('Amount must be positive')

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f'Account number: {self._account_number},\
 balance: {self._balance}'


class SavingsAccount(Account):
    def __init__(self, balance, account_number, interest: int):
        super().__init__(balance, account_number)
        self._interest = interest

    def add_interest(self):
        self._balance += self._balance * self._interest / 100


class CurrentAccount(Account):
    def __init__(self, balance, account_number, overdraft_limit):
        super().__init__(balance, account_number)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self._balance - amount) >= self._overdraft_limit:
            self._balance -= amount
        else:
            raise ValueError('Withdrawal amount exceeds available balance and\
 overdraft limit')


class Bank:
    def __init__(self, accounts: list[Account]):
        self._accounts = accounts

    def update(self):
        for a in self._accounts:
            if isinstance(a, SavingsAccount):
                a.add_interest()
            elif isinstance(a, CurrentAccount) and a.get_balance() < 0:
                print(f"{a.get_account_number()} in overdraft")

    def open_account(self, a):
        self._accounts.append(a)

    def close_account(self, a):
        self._accounts.remove(a)

    def pay_dividend(self, dividend):
        for a in self._accounts:
            a.deposit(dividend)


def test_bank():
    account_1 = Account(2000, 'UA85 399622 0000 0002 6001 2335 661')
    account_2 = Account(2200, 'NL91 ABNA 0417 1643 00')
    account_s_1 = SavingsAccount(1200, 'GB29 NWBK 6016 1331 9268 19', 2)
    account_s_2 = SavingsAccount(1500, 'FI21 1234 5600 0007 85', 2.5)
    account_c_1 = CurrentAccount(1050, 'DE89 3704 0044 0532 0130 00', -200)
    account_c_2 = CurrentAccount(1400, 'SE45 5000 0000 0583 9825 7466', -100)

    bank = Bank([account_1, account_2, account_s_1, account_s_2, account_c_1,
                account_c_2])
    bank.update()

    res = str(account_s_1)
    assert res == "Account number: GB29 NWBK 6016 1331 9268 19,\
 balance: 1224.0"

    account_c_2.withdraw(1450)
    res = str(account_c_2)
    assert res == "Account number: SE45 5000 0000 0583 9825 7466, balance: -50"

    new_account = Account(3000, 'US34 1234 5678 9012')
    bank.open_account(new_account)

    res = str(new_account)
    assert res == "Account number: US34 1234 5678 9012, balance: 3000"

    bank.pay_dividend(50)

    res = str(account_s_1)
    assert res == "Account number: GB29 NWBK 6016 1331 9268 19,\
 balance: 1274.0"

    res = str(account_c_2)
    assert res == "Account number: SE45 5000 0000 0583 9825 7466, balance: 0"

    res = str(new_account)
    assert res == "Account number: US34 1234 5678 9012, balance: 3050"


test_bank()
