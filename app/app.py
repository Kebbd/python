from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

class WarehouseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

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
            balance_entry = Balance(amount=self.balance)
            db.session.add(balance_entry)
            db.session.commit()

    def load_balance(self):
        with app.app_context():
            latest_balance_entry = Balance.query.order_by(Balance.id.desc()).first()
            if latest_balance_entry:
                self.balance = latest_balance_entry.amount

    def save_warehouse(self):
        for item, data in self.warehouse.items():
            warehouse_entry = WarehouseItem(
                name=item,
                price=data['price'],
                quantity=data['quantity']
            )
            db.session.add(warehouse_entry)
        db.session.commit()

    def save_history(self):
        for entry in self.history:
            parts = entry.split('units of')
            if len(parts) > 1:
                quantity_str = parts[0].split(' ')[-1].strip()
                quantity = int(quantity_str) if quantity_str else 0
                item_name = parts[1].split('for')[0].strip()
                price = float(parts[1].split('for')[1].split('each')[0].strip())

                transaction_entry = TransactionHistory(
                    transaction_type="Purchase" if "Purchased" in entry else "Sale",
                    item_name=item_name,
                    quantity=quantity,
                    price=price
                )
                db.session.add(transaction_entry)

        db.session.commit()

    def load_warehouse(self):
        with app.app_context():
            warehouse_entries = WarehouseItem.query.all()
            self.warehouse = {entry.name: {'price': entry.price, 'quantity': entry.quantity} for entry in warehouse_entries}


    def load_history(self):
        with app.app_context():
            history_entries = TransactionHistory.query.all()
            self.history = [f"{entry.transaction_type} {entry.quantity} units of {entry.item_name} for {entry.price} each." for entry in history_entries]


    def calculate_total_quantity(self):
        return sum(data['quantity'] for data in self.warehouse.values())

manager = Manager()
manager.load_balance()
manager.load_warehouse()
manager.load_history()

@app.route('/')
def index():
    manager.load_balance()
    total_quantity = manager.calculate_total_quantity()
    return render_template('index.html', balance=manager.balance, total_quantity=total_quantity, warehouse=manager.warehouse)



@app.route('/purchase', methods=['POST'])
def purchase():
    item = request.form['product_name']  # Updated field name to match HTML form
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
    item = request.form['product_name']  # Updated field name to match HTML form
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])


    if item and quantity > 0 and item in manager.warehouse and manager.warehouse[item]['quantity'] >= quantity:
        manager.warehouse[item]['quantity'] -= quantity
        sale_price = manager.warehouse[item]['price']
        manager.balance += sale_price * quantity
        manager.history.append(f"Sold {quantity} units of {item} for {sale_price} each.")
        manager.save_data()

    return redirect(url_for('index'))

@app.route('/balance-change', methods=['POST'])
def balance_change():
    change_value = float(request.form['change_value'])  # Updated field name to match HTML form

    if change_value != 0:
        manager.balance += change_value
        manager.history.append(f"Balance changed by {change_value}.")
        manager.save_data()

    return redirect(url_for('index'))

@app.route('/historia/')
@app.route('/historia/<int:start>/<int:end>')
def history(start=None, end=None):
    if start is None or end is None:
        return render_template('history.html', history=manager.history)
    else:
        try:
            if 1 <= start <= len(manager.history) and 1 <= end <= len(manager.history) and start <= end:
                return render_template('history.html', history=manager.history[start - 1:end])
            else:
                available_range = f"Available range: 1-{len(manager.history)}"
                return render_template('history.html', error=f"Invalid range. {available_range}")
        except ValueError:
            return render_template('history.html', error="Invalid range. Please provide valid start and end values.")
            

if __name__ == '__main__':
    manager = Manager()
    manager.load_balance()
    manager.load_warehouse()
    manager.load_history()

    # Run the Flask app
    app.run(debug=True)

