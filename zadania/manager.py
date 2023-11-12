import os

class Manager:
    def __init__(self):
        self.actions = {}
        self.balance = 0
        self.history = []
        self.warehouse = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self)

    def save_money(self):
        file_path = "balance.txt"
        with open(file_path, "w") as file:
            file.write(f"{self.balance}")

    def get_money(self):
        file_path = "balance.txt"
        if not os.path.exists(file_path):
            self.balance = 0
        else:
            with open(file_path) as file:
                self.balance = float(file.read())
        return self.balance

    def save_storage(self):
        file_path = "warehouse.txt"
        with open(file_path, "w") as file:
            for item, data in self.warehouse.items():
                price = data["price"]
                amount = data["amount"]
                file.write(f"{item}: {price}, {amount}\n")

    def get_storage(self):
        file_path = "warehouse.txt"
        self.warehouse = {}
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass
        else:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(": ")
                    item = parts[0]
                    data_parts = parts[1].split(", ")
                    price = data_parts[0]
                    amount = data_parts[1]
                    self.warehouse[item] = {"price": price, "amount": amount}

    def save_history(self):
        file_path = "history.txt"
        with open(file_path, "w") as file:
            for line in self.history:
                file.write(f"{line}\n")

    def get_history(self):
        self.history = []
        file_path = "history.txt"
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass
        else:
            with open(file_path, 'r') as file:
                for line in file.readlines():
                    self.history.append(line.strip())


manager = Manager()
manager.get_money()
manager.get_storage()
manager.get_history()

@manager.assign("1")
def balance(manager):
    print("1. Wplata pieniedzy")
    print("2. Wyplata pieniedzy")
    print("3. Powrot do menu")
    number_in = input()
    if not number_in:
        print("Blad")
        return
    if number_in == "1":
        change_balance = int(input("Ile chcesz wplacic?: "))
        manager.balance += change_balance
        manager.history.append(f"Do konta dodano {change_balance}")
    elif number_in == "2":
        change_balance = int(input("Ile chcesz wyplacic?: "))
        if manager.balance - change_balance < 0:
            print("Saldo nie moze byc ujemne!")
        else:
            manager.balance -= change_balance
            manager.history.append(f"Z konta zabrano {change_balance}")
    elif number_in == "3":
        return
    else:
        print("Niewlasciwy numer!")
        return


@manager.assign("2")
def sell(manager):
    item = input("Podaj nazwe produktu: ")
    if item in manager.warehouse:
        price = float(input("Podaj cenę produktu: "))
        amount = int(input("Podaj liczbe sztuk: "))
        if manager.warehouse[item]["amount"] > amount:
            manager.warehouse[item]["amount"] -= amount
            manager.balance += price * amount
            manager.history.append(f"Sprzedaz: {item} sztuk {amount} za {price}")
        elif manager.warehouse[item]["amount"] == amount:
            del manager.warehouse[item]
            manager.balance += price * amount
            manager.history.append(f"Sprzedaz: {item} sztuk {amount} za {price}")
        else:
            print("Za malo w magazynie")
    else:
        print("Brak w magazynie")


@manager.assign("3")
def buy(manager):
    item = input("Podaj nazwe produktu?: ")
    price = float(input("Podaj cene produktu?: "))
    amount = int(input("Podaj liczbe sztuk: "))
    if manager.balance - (price * amount) >= 0:
        if item in manager.warehouse:
            manager.warehouse[item]["amount"] += amount
        else:
            manager.warehouse[item] = {"price": price, "amount": amount}
        manager.balance -= price * amount
        manager.history.append(f"Kupiono {item} za {price} w ilosci {amount}")


@manager.assign("4")
def account(manager):
    print(f"Stan konta to {manager.balance}")


@manager.assign("5")
def item_list(manager):
    if manager.warehouse:
        for item, data in manager.warehouse.items():
            price = data["price"]
            amount = data["amount"]
            print(f"{item}: cena: {price} zł, ilość: {amount} sztuk")
    else:
        print("Magazyn jest pusty")


@manager.assign("6")
def storage(manager):
    item = input("Czego szukasz?: ")
    if item in manager.warehouse:
        amount_in = manager.warehouse[item]["amount"]
        print(f"W magazynie jest {amount_in} sztuk.")
    else:
        print("Brak w magazynie")


@manager.assign("7")
def catalog(manager):
    print(f"Przeprowadzono {len(manager.history)} operacji. Wybierz zakres.")
    start = input("Od: ")
    end = input("Do: ")
    if not start:
        start = 0
    else:
        try:
            start = int(start)
        except ValueError:
            print("Bledna wartosc")
            return

    if not end:
        end = len(manager.history)
    else:
        try:
            end = int(end)
        except ValueError:
            print("Bledna wartosc")
            return

    if start < 0 or end > len(manager.history) or start >= end:
        print("Błędny zakres operacji.")
    elif start > 0:
        for i in range(start - 1, end):
            print(manager.history[i])
    else:
        for i in range(start, end):
            print(manager.history[i])


@manager.assign("8")
def end(manager):
    manager.save_storage()
    manager.save_money()
    manager.save_history()
    exit()


while True:
    print("Wybierz numer")
    print("1. Saldo")
    print("2. Sprzedaz")
    print("3. Zakup")
    print("4. Konto")
    print("5. Lista")
    print("6. Magazyn")
    print("7. Przeglad")
    print("8. Koniec")
    number = input("Wybierz numer: ")
    manager.execute(number)
