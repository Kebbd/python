balance = 0
warehouse = {}
history = []

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
    
    
    if number == "1": # SALDO
        print("1. Wplata pieniedzy")
        print("2. Wyplata pieniedzy")
        print("3. Powrot do menu")
        number_in = input()
        if not number_in:
            print("Blad")
            continue
        if number_in == "1":
            change_balance = int(input("Ile chcesz wplacic?: "))
            balance += change_balance
            history.append(f"Do konta dodano {change_balance}")
        elif number_in == "2":
            change_balance = int(input("Ile chcesz wyplacic?: "))
            
            if balance - change_balance < 0:
                print("Saldo nie moze byc ujemne!")
            else:
                balance -= change_balance
                history.append(f"Z konta zabrano {change_balance}")
        elif number_in == "3":
            continue
        else:
            print("Niewlasciwy numer!")
            continue
            
    
    elif number == "2": # SPRZEDARZ
        item = input("Podaj nazwe produktu: ")
        if item in warehouse:
            price = float(input("Podaj cenę produktu: "))
            amount = int(input("Podaj liczbe sztuk: "))
            if warehouse[item]["amount"] > amount:
                warehouse[item]["amount"] -= amount
                balance += price*amount
                history.append(f"Sprzedaz: {item} sztuk {amount} za {price}")
            elif warehouse[item]["amount"] == amount:
                del warehouse[item]
                balance += price*amount
                history.append(f"Sprzedaz: {item} sztuk {amount} za {price}")
            else:
                print("Za malo w magazynie")
        else:
            print("Brak w magazynie")

    
    elif number == "3": # ZAKUP
        item = input("Podaj nazwe produktu?: ")
        price = float(input("Podaj cene produktu?: "))
        amount = int(input("Podaj liczbe sztuk: "))
        
        if balance - (price*amount) >= 0:
            if item in warehouse:
                warehouse[item]["amount"] += amount
            else:
                warehouse[item] = {"price": price, "amount": amount}
            balance -= price*amount
            history.append(f"Kupiono {item} za {price} w ilosci {amount}")

    elif number == "4": # KONTO
        print(f"Stan konta to {balance}")

        
    elif number == "5": # LISTA
        if warehouse:
            for item, data in warehouse.items():
                price = data["price"]
                amount = data["amount"]
                print(f"{item}: cena: {price} zł, ilość: {amount} sztuk")
        else:
            print("Magazyn jest pusty")

    elif number == "6": # MAGAZYN
        item = input("Czego szukasz?: ")
        if item in warehouse:
            amount_in = warehouse[item]["amount"]
            print(f"W magazynie jest {amount_in} sztuk.")
        else:
            print("Brak w magazynie")


    elif number == "7": # PRZEGLAD
        print(f"Przeprowadzono {len(history)} operacji. Wybierz zakres.")
        start = input("Od: ")
        end = input("Do: ")
        
        if not start:
            start = 0
        else:
            try:
                start = int(start)
            except ValueError:
                print("Bledna wartosc")
                continue

        if not end:
            end = len(history)
        else:
            try:
                end = int(end)
            except ValueError:
                print("Bledna wartosc")
                continue

        if start < 0 or end > len(history) or start >= end:
            print("Błędny zakres operacji.")
        elif start > 0:
            for i in range(start-1, end):
                print(history[i])
        else:
            for i in range(start, end):
                print(history[i])

                
    elif number == "8": # KONIEC
        break
    
    
    else: ######
        print("Niewlasciwy wybor")
        continue