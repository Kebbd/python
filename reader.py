import os
import csv
import sys



def read(file_path, data):
    possible_delimiters = [',', ';', '\t']  

    if os.path.exists(file_path):
        with open(file_path, newline='') as file:
            for delimiter in possible_delimiters:
                try:
                    reader = csv.reader(file, delimiter=delimiter)
                    for row in reader:
                        data.append(row)
                    break
                except csv.Error:
                    file.seek(0)
                    data.clear()
    return data

def edit(items, data):
    for arg in items:
        item = arg.split(",")
        x = int(item[0])
        y = int(item[1])
        value = item[2]
        data[y].pop(x)
        data[y].insert(x, value)
    return data

def show(data):
    for row in data:
        print(row)
            
def write(file_path, data):
    with open(file_path, "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerows(data)

data = []

file_in = sys.argv[1]
file_out = sys.argv[2]
changes = sys.argv[3:]

read(file_in, data)
edit(changes, data)
show(data)
write(file_out, data)