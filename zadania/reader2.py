import os
import sys
import json
import csv
import pickle

class FileReader:
    def __init__(self, file_in, file_out, data):
        self.file_in = file_in
        self.file_out = file_out
        self.data = data

    def edit(self):
        if len(sys.argv) < 4:
            print("Arguments missing")
            return self.data

        items = sys.argv[3:]
        for arg in items:
            item = arg.split(",")
            if len(item) != 3:
                print("Edit argument format is invalid:", arg)
                continue
            try:
                x = int(item[0])
                y = int(item[1])
                value = item[2]
                if y < len(self.data) and x < len(self.data[y]):
                    self.data[y][x] = value
                else:
                    print("Invalid argumenst:", x, y)
            except ValueError:
                print("Edit argument format is invalid:", arg)
        return self.data

    def read(self):
        pass

    def write(self):
        pass

class CsvReader(FileReader):
    def read(self):
        with open(self.file_in, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.data.append(row)


    def write(self):
        with open(self.file_out, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.data)

class JsonReader(FileReader):
    def read(self):
        with open(self.file_in) as file:
            self.data = json.load(file)

    def write(self):
        with open(self.file_out, 'w') as file:
            json.dump(self.data, file)

class PickleReader(FileReader):
    def read(self):
        with open(self.file_in, 'rb') as file:
            self.data = pickle.load(file)

    def write(self):
        with open(self.file_out, 'wb') as file:
            pickle.dump(self.data, file)

class TxtReader(FileReader):
    def read(self):
        with open(self.file_in, "r") as file:
            self.data = [line.strip().split(',') for line in file]

    def write(self):
        with open(self.file_out, "w") as file:
            for row in self.data:
                file.write(','.join(row) + '\n')

def main():
    data = []
    file_in = sys.argv[1]
    file_out = sys.argv[2]

    file_extension = os.path.splitext(file_in)[1]
    file_extension = file_extension.lower()

    reader = None

    if file_extension == ".txt":
        reader = TxtReader(file_in, file_out, data)
    elif file_extension == ".csv":
        reader = CsvReader(file_in, file_out, data)
    elif file_extension == ".pickle":
        reader = PickleReader(file_in, file_out, data)
    elif file_extension == ".json":
        reader = JsonReader(file_in, file_out, data)

    if reader:
        reader.read()
        reader.edit()
        reader.write()
        for line in data:
            print(line)
        print("Data successfully read and written.")
    else:
        print("Unsupported file extension:", file_extension)

if __name__ == "__main__":
    main()
