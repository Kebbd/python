import os
import csv
import sys


def read(data):
    possible_delimiters = [",", ";", "\t"]
    if len(sys.argv) < 2:
        print("Brak argumentu wiersza poleceń. Podaj ścieżkę do pliku wejściowego.")
        return data

    file_path = sys.argv[1]
    if os.path.exists(file_path):
        with open(file_path, newline="") as file:
            for delimiter in possible_delimiters:
                try:
                    reader = csv.reader(file, delimiter=delimiter)
                    for row in reader:
                        data.append(row)
                    break
                except csv.Error:
                    file.seek(0)
                    data.clear()
    else:
        print("Plik wejściowy nie istnieje")
    return data


def edit(data):
    if len(sys.argv) < 4:
        print("Brak argumentów edycji. Podaj indeksy i wartości do edycji.")
        return data

    items = sys.argv[3:]
    for arg in items:
        item = arg.split(",")
        if len(item) != 3:
            print("Nieprawidłowy format argumentu edycji:", arg)
            continue
        try:
            x = int(item[0])
            y = int(item[1])
            value = item[2]
            if y < len(data) and x < len(data[y]):
                data[y][x] = value
            else:
                print("Nieprawidłowe indeksy edycji:", x, y)
        except ValueError:
            print("Nieprawidłowy format indeksów edycji:", arg)
    return data


def show(data):
    for row in data:
        print(row)


def write(data):
    if len(sys.argv) < 3:
        print("Podaj ścieżkę do pliku wyjściowego.")
        return

    file_path = sys.argv[2]
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == "__main__":
    data = []

    read(data)
    edit(data)
    show(data)
    write(data)
