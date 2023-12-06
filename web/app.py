from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class Manager:
    def __init__(self):
        self.balance = 0
        self.warehouse = {}
        self.history = []

    def save_data(self):
        self.save_balance()
        self.save_warehouse()
        self.save_history()

    def save_balance(self):
        with open("balance.txt", "w") as file:
            file.write(str(self.balance))

    def load_balance(self):
        if os.path.exists("balance.txt"):
            with open("balance.txt", "r") as file:
                self.balance = float(file.read())

    def save_warehouse(self):
        with open("warehouse.txt", "w") as file:
            for item, data in self.warehouse.items():
                file.write(f"{item},{data['price']},{data['quantity']}\n")

    def load_warehouse(self):
        self.warehouse = {}
        if os.path.exists("warehouse.txt"):
            with open("warehouse.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        item = parts[0]
                        price = float(parts[1])
                        try:
                            quantity = int(parts[2])
                            self.warehouse[item] = {"price": price, "quantity": quantity}
                        except ValueError:
                            print(f"Invalid quantity for item {item}. Skipping this item.")

    def save_history(self):
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")

    def load_history(self):
        self.history = []
        if os.path.exists("history.txt"):
            with open("history.txt", "r") as file:
                for line in file:
                    self.history.append(line.strip())

manager = Manager()
manager.load_balance()
manager.load_warehouse()
manager.load_history()

@app.route('/')
def index():
    return render_template('index.html', balance=manager.balance, warehouse=manager.warehouse)

@app.route('/purchase', methods=['POST'])
def purchase():
    item = request.form['product_name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    if item and price >= 0 and quantity > 0:
        if item in manager.warehouse:
            manager.warehouse[item]['quantity'] += quantity
        else:
            manager.warehouse[item] = {'price': price, 'quantity': quantity}

        manager.balance -= price * quantity
        manager.history.append(f"Purchased {quantity} units of {item} for {price} each.")
        manager.save_data()

    return redirect(url_for('index'))

@app.route('/sale', methods=['POST'])
def sale():
    item = request.form['product_name']
    quantity = int(request.form['quantity'])

    if item and quantity > 0 and item in manager.warehouse and manager.warehouse[item]['quantity'] >= quantity:
        manager.warehouse[item]['quantity'] -= quantity
        sale_price = manager.warehouse[item]['price']
        manager.balance += sale_price * quantity
        manager.history.append(f"Sold {quantity} units of {item} for {sale_price} each.")
        manager.save_data()

    return redirect(url_for('index'))

@app.route('/balance-change', methods=['POST'])
def balance_change():
    change_value = float(request.form['change_value'])

    if change_value != 0:
        manager.balance += change_value
        manager.history.append(f"Balance changed by {change_value}.")
        manager.save_data()

    return redirect(url_for('index'))

@app.route('/historia/')
@app.route('/historia/<start>/<end>')
def history(start=None, end=None):
    if start is None or end is None:
        return render_template('history.html', history=manager.history)
    else:
        try:
            start = int(start)
            end = int(end)
            if 1 <= start <= len(manager.history) and 1 <= end <= len(manager.history) and start <= end:
                return render_template('history.html', history=manager.history[start - 1:end])
            else:
                available_range = f"Available range: 1-{len(manager.history)}"
                return f"Invalid range. {available_range}"
        except ValueError:
            return "Invalid range. Start and end must be integers."

if __name__ == '__main__':
    app.run(debug=True)
