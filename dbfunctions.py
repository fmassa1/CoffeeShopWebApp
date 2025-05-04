import psycopg2
from datetime import datetime

user = "postgres"
password = "fred1234"

connection = {
    'dbname' : 'coffeeshop',
    'user' : user,
    'host' : '127.0.0.1',
    'password' : password,
    'port' : 5432
}
conn = psycopg2.connect(**connection)
cur = conn.cursor()

def login(email, password):
    try:
        cur.execute("SELECT ssn FROM Employees WHERE email = %s", (email,))
        employee = cur.fetchone()
        if not employee:
            return "Email not found", "error"

        ssn = employee[0]

        cur.execute("SELECT 1 FROM Barista WHERE ssn = %s", (ssn,))
        is_barista = cur.fetchone() is not None

        cur.execute("SELECT 1 FROM Manager WHERE ssn = %s", (ssn,))
        is_manager = cur.fetchone() is not None

        if is_barista and is_manager:
            role = "both"
        elif is_manager:
            role = "manager"
        elif is_barista:
            role = "barista"
        else:
            role = "error"

        cur.execute("SELECT password FROM Accounts WHERE ssn = %s", (ssn,))
        account = cur.fetchone()

        if account:
            spassword = account[0]
            if spassword == password:
                return "Successful", role
            else:
                return "Incorrect password", "error"
        
        else:
            cur.execute("INSERT INTO Accounts (ssn, email, password) VALUES (%s, %s, %s)", (ssn, email, password))
            conn.commit()
            return "Account created", role

    except Exception as e:
        conn.rollback()
        print("An error occurred:", e)
        return "Error occurred"

def getEmployees():
    try:
        cur.execute("SELECT * FROM Employees")
        rows = cur.fetchall()
        return rows
        
    except Exception as e:
        conn.rollback()
        print("Error:", e)


def addEmployee(type, ssn, name, email, salary, percent=None):
    try:
        cur.execute( "INSERT INTO Employees (name, ssn, email, salary) VALUES (%s, %s, %s, %s);",(name, ssn, email, salary))

        if type == "manager" or type == "both":
            cur.execute("INSERT INTO Manager (ssn, ownership_percentage) VALUES (%s, %s);",(ssn, percent))
        if type == "barista" or type == "both":
            cur.execute("INSERT INTO Barista (ssn) VALUES (%s);", (ssn,))
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def removeEmployee(ssn, type):
    try:
        cur.execute("DELETE FROM Accounts WHERE ssn = %s;", (ssn,))
        cur.execute("DELETE FROM Work_Schedule WHERE ssn = %s;", (ssn,))
        cur.execute("DELETE FROM Barista WHERE ssn = %s;", (ssn,))
        cur.execute("DELETE FROM Manager WHERE ssn = %s;", (ssn,))
        cur.execute("DELETE FROM Employees WHERE ssn = %s;", (ssn,))
        
        rows_deleted = cur.rowcount
        print(f"Deleted from Employees: {rows_deleted}")
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

def updateInfo(ssn, column, new_val):
    try:
        # checks if ssn exists
        cur.execute("SELECT 1 FROM Employees WHERE ssn = %s;", (ssn,))
        if cur.fetchone() is None:
            print(f"Error: Employee with SSN {ssn} does not exist.")
            return

        query = f"UPDATE Employees SET {column} = %s WHERE ssn = %s;"
        cur.execute(query, (new_val, ssn))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

def getAccounting():
    try:
        cur.execute("SELECT * FROM Accounting")
        rows = cur.fetchall()
        return rows
        
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return "error"

def addNewInventory(name, init_quantity, unit, ppu):
    try:
        cur.execute("INSERT INTO Inventory (name, stock_quantity, unit, price_per_unit) VALUES (%s, %s, %s, %s);",(name, 0, unit, ppu))
        add = manageInventory(name, init_quantity)
        if (add == "0"):
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error:", e)


def updateInventory(item, amount):
    try:

        cur.execute("SELECT 1 FROM Inventory WHERE name = %s;", (item,))
        if cur.fetchone() is None:
            print(f"Error: Inventory item '{item}' does not exist.")
            return

        cur.execute(
            "UPDATE Inventory SET stock_quantity = stock_quantity + %s WHERE name = %s;",
            (amount, item)
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

def manageInventory(item_name, quantity_adding):
    try:
        if quantity_adding <= 0:
            print("Error: Quantity to add must be positive.")
            return "Error: Quantity to add must be positive."

        cur.execute("SELECT price_per_unit FROM Inventory WHERE name = %s;", (item_name,))
        result = cur.fetchone()
        if result is None:
            print(f"Error: {item_name} is not in the inventory.")
            return 'Error: {item_name} is not in the inventory.'
        
        ppu = result[0]
        total_cost = ppu * quantity_adding

        cur.execute("SELECT balance FROM Accounting ORDER BY timestamp DESC LIMIT 1;")
        current_balance = cur.fetchone()
        if current_balance is None:
            print("Error: No account balance found.")
            return "Error: No account balance found."

        current_balance = current_balance[0]

        if current_balance < total_cost:
            print(f"Error: Not enough balance to buy {quantity_adding} units of {item_name}. Needed: {total_cost}, Available: {current_balance}")
            return f"Error: Not enough balance to buy {quantity_adding} units of {item_name}. Needed: {total_cost}, Available: {current_balance}"

        cur.execute(
            "UPDATE Inventory SET stock_quantity = stock_quantity + %s WHERE name = %s;",
            (quantity_adding, item_name)
        )
        new_balance = current_balance - total_cost
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO Accounting (timestamp, balance, transaction_type) VALUES (%s, %s, %s);", (timestamp, new_balance, f"adding {item_name} inventory stock"))

        conn.commit()
        print(f"Successfully added {quantity_adding} units to {item_name}. New balance: {new_balance}")
        return "0"

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    except Exception as e:
        conn.rollback()
        print("Error:", e)

def createOrderItem(item, quantity, timestamp):
    cur.execute("SELECT name, quantity FROM Ingredients WHERE recipe = %s", (item,))
    ingredients = cur.fetchall()

    for ingredient, required_quantity in ingredients:
        cur.execute("SELECT stock_quantity FROM Inventory WHERE name = %s", (ingredient,))
        result = cur.fetchone()
        if not result:
            raise ValueError(f"Ingredient {ingredient} not found in inventory.")
        available_quantity = result[0]
        if available_quantity < required_quantity * quantity:
            raise ValueError(f"Not enough {ingredient} in stock for {item}. Needed: {required_quantity * quantity}, Available: {available_quantity}")

    for ingredient, required_quantity in ingredients:
        cur.execute("UPDATE Inventory SET stock_quantity = stock_quantity - %s WHERE name = %s", (required_quantity * quantity, ingredient))

    cur.execute("SELECT quantity FROM Order_Items WHERE timestamp = %s AND item = %s", (timestamp, item))
    existing = cur.fetchone()
    if existing:
        new_quantity = existing[0] + quantity
        cur.execute("UPDATE Order_Items SET quantity = %s WHERE timestamp = %s AND item = %s", (new_quantity, timestamp, item))
    else:
        cur.execute("INSERT INTO Order_Items (timestamp, item, quantity) VALUES (%s, %s, %s)", (timestamp, item, quantity))

    cur.execute("SELECT price FROM Menu WHERE name = %s;", (item,))
    result = cur.fetchone()
    item_price = float(result[0])
    return item_price * quantity

def createOrder(payment_method, order_items):
    conn.rollback()
    order_cost = 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("BEGIN")

    for item, quantity in order_items:
        try:
            order_cost += createOrderItem(item, quantity, timestamp)
        except ValueError as e:
            conn.rollback()
            print(f"Order failed: {e}")
            return False, str(e)

    cur.execute("INSERT INTO Orders (timestamp, payment_method) VALUES (%s, %s)", (timestamp, payment_method))

    cur.execute("SELECT balance FROM Accounting ORDER BY timestamp DESC LIMIT 1;")
    current_balance = cur.fetchone()
    new_balance = float(current_balance[0]) + order_cost

    order_details = "Order " + ', '.join([f"{item} x{quantity}" for item, quantity in order_items])

    cur.execute(
        "INSERT INTO Accounting (timestamp, balance, transaction_type) VALUES (%s, %s, %s)",
        (timestamp, new_balance, order_details)
    )

    conn.commit()
    return True, None


def getInventoryItems():
    try:
        cur.execute("SELECT name FROM Inventory;")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return []
    
def getInventory():
    try:
        cur.execute("SELECT name, stock_quantity, unit, price_per_unit FROM Inventory;")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return []
    
def getMenuItems():
    try:
        cur.execute("SELECT name, price FROM Menu;")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return []
    
def getWorkSchedules():
    try:
        cur.execute("""
            SELECT w.ssn, e.name, w.day_of_week, w.start_time, w.end_time
            FROM Work_Schedule w
            JOIN Employees e ON w.ssn = e.ssn
            ORDER BY w.ssn, 
                     CASE 
                        WHEN w.day_of_week = 'Monday' THEN 1
                        WHEN w.day_of_week = 'Tuesday' THEN 2
                        WHEN w.day_of_week = 'Wednesday' THEN 3
                        WHEN w.day_of_week = 'Thursday' THEN 4
                        WHEN w.day_of_week = 'Friday' THEN 5
                        WHEN w.day_of_week = 'Saturday' THEN 6
                        WHEN w.day_of_week = 'Sunday' THEN 7
                     END,
                     w.start_time;
        """)
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return []
    
