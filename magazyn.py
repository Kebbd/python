balance = 0
warehouse = []
prices = []
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
        number1 = input()
        
        if number1 == "1":
            change_balance = int(input("Ile chcesz wplacic?: "))
            balance += change_balance
            history.append(f"Do konta dodano {change_balance}")
        elif number1 == "2":
            change_balance = int(input("Ile chcesz wyplacic?: "))
            
            if balance - change_balance < 0:
                print("Saldo nie moze byc ujemne!")
            else:
                balance -= change_balance
                history.append(f"Z konta zabrano {change_balance}")
        
        elif number1 == "3":
            continue
        else:
            print("Niewlasciwy numer!")
            continue
            
    
    elif number == "2": # SPRZEDARZ
        item = input("Co sprzedajesz?: ")
        price = int(input("Za ile?: "))
        amount = int(input("Ile sztuk?: "))

        if warehouse.count(item) > 0:
            for i in range(amount):
                warehouse.remove(item)
                prices.remove(warehouse.index(item))
                balance += price
            history.append(f"Sprzedano {item} za {price} w ilosci {amount}")
        else:
            print("Brak w magazynie")

    
    elif number == "3": # ZAKUP
        item = input("Co kupujesz?: ")
        price = int(input("Za ile?: "))
        amount = int(input("Ile sztuk?: "))
        
        if balance - price < 0:
            print("Za malo srodkow na koncie!")
        else:
            for i in range(amount):
                warehouse.append(item)
                prices.append(price)
                balance -= price
        history.append(f"Kupiono {item} za {price} w ilosci {amount}")

    elif number == "4": # KONTO
        print(f"Stan konta to {balance}")

        
    elif number == "5": # LISTA
        item_list = zip(warehouse, prices)
        print(tuple(item_list))

    elif number == "6": # MAGAZYN
        check = input("Czego szukasz?: ")
        if warehouse.count(check) > 0:
            print(f"W magazynie jest {warehouse.count(check)} sztuk.")
        else:
            print("Brak w magazynie")


    elif number == "7": # PRZEGLAD
        print(f"Przeprowadzono {len(history)} operacji. Wybierz zakres.")
        od = input("Od: ")
        
        if od == "":
            od = None
        else:
            od = int(od)
        do = input("Do: ")
        
        if do == "":
            do = None
        else:
            do = int(do)
        
        if od == None and do != None:
            print(history[od:do])
        elif od != None and do != None:
            print(history[od-1:do])
        elif od != None and do == None:
            print(history[od-1:do])
        else:
            print(history[od:do])


    elif number == "8": # KONIEC
        exit()
    
    
    else: ######
        print("Niewlasciwy wybor")
        continue