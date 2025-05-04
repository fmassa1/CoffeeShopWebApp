from decimal import Decimal
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from dbfunctions import *


app = Flask(__name__)
app.secret_key='key'

@app.route('/login', methods=['POST'])
def login_route():
    email = request.form.get('email')
    password = request.form.get('password')
    
    attempt, role = login(email, password)

    if role == "manager" or role == "both":
        session['role'] = role
        return redirect(url_for('manager_menu'))
    elif role == "barista":
        session['role'] = role
        return redirect(url_for('barista_menu')) 
    else:
        return render_template('login.html', message=attempt)
@app.route('/', methods=['GET']) 
def index():
    return render_template('login.html', message=None)

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('index'))


@app.route('/manager', methods=['GET'])
def manager_menu():
    employees = getEmployees()
    accounting = getAccounting()
    inventory_items = getInventoryItems()
    inventory_full = getInventory()
    schedules = getWorkSchedules()
    return render_template('manager_menu.html', employees=employees, accounting=accounting, inventory_items=inventory_items, inventory_full=inventory_full, schedules=schedules)

@app.route('/update_employee', methods=['POST'])
def update_employee():
    ssn = request.form.get('ssn')
    column = request.form.get('column')
    new_val = request.form.get('new_val')

    updateInfo(ssn, column, new_val)
    return redirect(url_for('manager_menu'))

@app.route('/remove_employee', methods=['POST'])
def remove_employee():
    ssn = request.form.get('ssn')
    emp_type = request.form.get('type')  

    removeEmployee(ssn, emp_type)
    return redirect(url_for('manager_menu'))

@app.route('/add_employee', methods=['POST'])
def add_employee():
    ssn = request.form.get('ssn')
    name = request.form.get('name')
    email = request.form.get('email')
    salary = request.form.get('salary')
    emp_type = request.form.get('type')  

    if not ssn.isdigit() or len(ssn) != 9:
        employees = getEmployees()
        return render_template('manager_menu.html', employees=employees, error="SSN must be 9 digits.")
    
    addEmployee(emp_type, ssn, name, email, salary, percent=None)
    return redirect(url_for('manager_menu'))

@app.route('/new_inventory', methods=['POST'])
def add_new_inventory():
    name = request.form['item_name']
    quantity = int(request.form['init_quantity'])
    unit = request.form['unit']
    ppu = int(request.form['ppu'])
    
    try:
        addNewInventory(name, quantity, unit, ppu)
        return redirect(url_for('manager_menu')) 
    except Exception as e:
        print("Error:", e)
        return render_template('manager_menu.html', error="Failed to add inventory item.")

@app.route('/add_stock', methods=['POST'])
def add_stock():
    item_name = request.form.get('item_name')
    quantity_adding = request.form.get('quantity_adding')

    try:
        quantity_adding = Decimal(quantity_adding)
        success = manageInventory(item_name, quantity_adding)
        if success == '0':
            return redirect(url_for('manager_menu'))
        else:
            employees = getEmployees()
            accounting = getAccounting()
            schedules = getWorkSchedules()
            inventory_items = getInventoryItems()
            inventory_full = getInventory()
            return render_template('manager_menu.html', employees=employees, accounting=accounting, stock_error=success,inventory_items=inventory_items, inventory_full=inventory_full, schedules=schedules)

    except Exception as e:
        employees = getEmployees()
        accounting = getAccounting()
        schedules = getWorkSchedules()
        inventory_items = getInventoryItems()
        inventory_full = getInventory()
        error_message = f"Error updating stock: {e}"
        return render_template('manager_menu.html', employees=employees, accounting=accounting, stock_error=error_message, inventory_items=inventory_items, inventory_full=inventory_full, schedules=schedules)
    
@app.route('/barista', methods=['GET'])
def barista_menu():
    menu_items = getMenuItems()
    schedules = getWorkSchedules()

    return render_template('barista_menu.html', menu=menu_items, instructions=None, schedules=schedules)   

@app.route('/submit_order', methods=['POST'])
def submit_order():
    items = request.form.getlist('item[]')
    quantities = request.form.getlist('quantity[]')
    payment_method = request.form.get('payment_method')

    order_items = [[item, int(quantity)] for item, quantity in zip(items, quantities)]

    success, error_message = createOrder(payment_method, order_items)

    instructions = {}
    if success:
        try:
            for item in items:
                cur.execute("SELECT position, name FROM Preperation_Step WHERE recipe = %s ORDER BY position;", (item,))
                steps = cur.fetchall()
                instructions[item] = [step[1] for step in steps]
        except Exception as e:
            print("Error fetching preparation steps:", e)

    menu_items = getMenuItems()
    schedules = getWorkSchedules()

    return render_template(
        'barista_menu.html',
        menu=menu_items,
        instructions=instructions,
        order_summary=order_items,
        error_message=error_message,
        schedules=schedules
    )
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
    #app.run(debug=True)