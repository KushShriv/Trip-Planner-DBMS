from flask import Flask, request, jsonify, abort
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    # user="harshita",
    # password="#Har123har",
    user="root",
    password="21sept",
    database="trip_planner"
)

cursor = db.cursor()

'''
tables = { 
    table_name:(
        column slice - how many of the columns of the table are being auto-incremented,
        columns - in a tuple
        foreign key constraints {
            column: (referenced_table, referenced_column)
        }
    ),
    ...........
}
'''
tables = {
    "customer": (
        1,
        ("Customer ID", "Customer Name", "Phone Number", "Email", "Password"),
        {}
    ),
    "address": (
        1,
        ("Address ID", "District", "City", "Pin Code", "State", "Country"),
        {}
    ),
    "hotel": (
        1,
        ("Hotel ID", "Hotel Name", "Check-in Date", "Check-out Date", "Room Class", "Room Capacity", "Cost Per Night", "Address ID"),
        {
            "Address ID": ("address", "Address ID")
        }
    ),
    "transport": (
        1,
        ("Transport ID", "Transport Type", "Departure Date", "Arrival Date", "Start Address ID", "Destination Address ID", "Travel Time", "Price Per Seat"),
        {
            "Start Address ID": ("address", "Address ID"),
            "Destination Address ID": ("address", "Address ID")
        }
    ),
    "travel": (
        1,
        ("Travel ID", "Transport ID To Destination", "Transport ID From Destination", "Number of Seats To Destination", "Number of Seats From Destination", "Total Cost"),
        {
            "Transport ID To Destination": ("transport", "Transport ID"),
            "Transport ID From Destination": ("transport", "Transport ID")
        }
    ),
    "trip": (
        1,
        ("Trip ID", "Customer ID", "Hotel ID", "Travel ID", "Total Cost"),
        {
            "Customer ID": ("customer", "Customer ID"),
            "Hotel ID": ("hotel", "Hotel ID"),
            "Travel ID": ("travel", "Travel ID")
        }
    )
}

def check_foreign_keys(value, table_name, column_name):
    query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    if result is None:
        abort(400, description=f"{column_name}={value} not found in {table_name}")

def post(data, table_name):
    column_slice, columns, foreign_keys = tables[table_name]
    # if foreign_keys:
    #     for column, (referenced_table, referenced_column) in foreign_keys.items():
    #         check_foreign_keys(data[column], referenced_table, referenced_column)
    query = f"INSERT INTO `{table_name}` (`{'`, `'.join(columns[column_slice:])}`) VALUES ({', '.join(['%s'] * (len(columns) - column_slice))})"
    values = tuple(data[column] for column in columns[column_slice:])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': f'{table_name.capitalize()} added successfully'}), 201

def get_all_records(table_name):
    _, columns, __ = tables[table_name]
    query = f"SELECT `{'`, `'.join(columns)}` FROM `{table_name}`"
    cursor.execute(query)
    records = cursor.fetchall()
    result = []
    for record in records:
        record_dict = dict(zip(columns, record))
        result.append(record_dict)
    return jsonify({table_name: result})

def delete(table_name, ID):
    query = f"DELETE FROM `{table_name}` WHERE `{table_name.capitalize()} ID` = {ID}"
    cursor.execute(query)
    db.commit()
    return jsonify({"message": f"{table_name.capitalize()} deleted successfully"}), 200

def get_records_by_ID(table_name, ID):
    _, columns, __ = tables[table_name]
    query = f"SELECT `{'`, `'.join(columns)}` FROM `{table_name}` WHERE `{table_name.capitalize()} ID` = {ID}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = []
    for record in records:
        record_dict = dict(zip(columns, record))
        result.append(record_dict)
    return jsonify({table_name: result})

# Post
@app.route('/address', methods=['POST'])
def add_address():
    return post(request.json, "address")

@app.route('/customer', methods=['POST'])
def add_customer():
    return post(request.json, 'customer')

@app.route('/hotel', methods=['POST'])
def add_hotel():
    return post(request.json, 'hotel')

@app.route('/transport', methods=['POST'])
def add_transport():
    return post(request.json, 'transport')

@app.route('/travel', methods=['POST'])
def add_travel():
    return post(request.json, 'travel')
# @app.route('/travel', methods=['POST'])
# def add_travel():
#     data = request.json
#     query = "INSERT INTO travel (`Transport ID To Destination`, `Transport ID From Destination`, `Number of Seats To Destination`, `Number of Seats From Destination`, `Total Cost`) VALUES (%s, %s, %s, %s, %s)"
#     values = (data['Transport ID To Destination'], data['Transport ID From Destination'], data['Number of Seats To Destination'], data['Number of Seats From Destination'], data['Total Cost'])
#     cursor.execute(query, values)
#     db.commit()
#     return jsonify({'message': 'Travel added successfully'}), 201

@app.route('/trip', methods=['POST'])
def add_trip():
    return post(request.json, 'trip')
# @app.route('/trip', methods=['POST'])
# def add_trip():
#     data = request.json
#     # Check if the provided Hotel_Id, customer_id, and travel_id exist in their respective tables
#     check_foreign_keys(data['Hotel_Id'], 'hotels', 'Hotel_id')
#     check_foreign_keys(data['customer_id'], 'customer', 'customer_id')
#     check_foreign_keys(data['travel_id'], 'Travel', 'travel_id')
#
#     query = "INSERT INTO trip (No_of_rooms, Total_cost, Hotel_Id, customer_id, travel_id) VALUES (%s, %s, %s, %s, %s)"
#     values = (data['No_of_rooms'], data['Total_cost'], data['Hotel_Id'], data['customer_id'], data['travel_id'])
#     cursor.execute(query, values)
#     db.commit()
#     return jsonify({'message': 'trip added successfully'}), 201

# GET All
@app.route('/address', methods=['GET'])
def get_all_addresses():
    return get_all_records("address")

@app.route('/customer', methods=['GET'])
def get_all_customers():
    return get_all_records('customer')

@app.route('/hotel', methods=['GET'])
def get_all_hotels():
    return get_all_records('hotel')

@app.route('/transport', methods=['GET'])
def get_all_transports():
    return get_all_records('transport')

@app.route('/travel', methods=['GET'])
def get_all_travels():
    return get_all_records('travel')

@app.route('/trip', methods=['GET'])
def get_all_trips():
    return get_all_records('trip')

# Delete By ID
@app.route('/address/<int:ID>', methods=['DELETE'])
def delete_address(ID):
    return delete("address", ID)

@app.route('/customer/<int:ID>', methods=['DELETE'])
def delete_customer(ID):
    return delete('customer', ID)

@app.route('/hotel/<int:ID>', methods=['DELETE'])
def delete_hotel(ID):
    return delete('hotel', ID)

@app.route('/transport/<int:ID>', methods=['DELETE'])
def delete_transport(ID):
    return delete('transport', ID)

@app.route('/travel/<int:ID>', methods=['DELETE'])
def delete_travel(ID):
    return delete('travel', ID)

@app.route('/trip/<int:ID>', methods=['DELETE'])
def delete_trip(ID):
    return delete('trip', ID)

# GET By ID
@app.route('/address/<int:ID>', methods=['GET'])
def get_address_by_id(ID):
    return get_records_by_ID('address', ID)

@app.route('/customer/<int:ID>', methods=['GET'])
def get_customer_by_id(ID):
    return get_records_by_ID('customer', ID)

@app.route('/hotel/<int:ID>', methods=['GET'])
def get_hotel_by_id(ID):
    return get_records_by_ID('hotel', ID)

@app.route('/transport/<int:ID>', methods=['GET'])
def get_transport_by_id(ID):
    return get_records_by_ID('transport', ID)

@app.route('/travel/<int:ID>', methods=['GET'])
def get_travel_by_id(ID):
    return get_records_by_ID('travel', ID)

@app.route('/trip/<int:ID>', methods=['GET'])
def get_trip_by_id(ID):
    return get_records_by_ID('trip', ID)

if __name__ == '__main__':
    app.run(debug=True)

