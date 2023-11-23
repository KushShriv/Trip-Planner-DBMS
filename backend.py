from flask import Flask, request, jsonify
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

# Function to check foreign key constraints
def check_foreign_keys(value, table_name, column_name):
    query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    if result is None:
        abort(400, description=f"{column_name}={value} not found in {table_name}")

@app.route('/address', methods=['POST'])
def add_address():
    data = request.json
    # Insert data into the 'address' table
    query = "INSERT INTO address (Address_id, location_name, pincode, country, house_no, street_no, locality, landmark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data['Address_id'], data['location_name'], data['pincode'], data['country'], data['house_no'], data['street_no'], data['locality'], data['landmark'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Address added successfully'}), 201

@app.route('/Address', methods=['GET'])
def get_all_addresses():
    # Retrieve all addresses from the 'address' table
    query = "SELECT * FROM Address"
    cursor.execute(query)
    addresses = cursor.fetchall()
    result = []
    for address in addresses:
        address_dict = {
            "Address_id": address[0],
            "location_name": address[1],
            "pincode": address[2],
            "country": address[3],
            "house_no": address[4],
            "street_no": address[5],
            "locality": address[6],
            "landmark": address[7]
        }
        result.append(address_dict)

    return jsonify({'Address': result})

@app.route('/Address/<int:Address_id>', methods=['DELETE'])
def delete_address(address_id):
    # Delete an address from the 'address' table
    query = "DELETE FROM Address WHERE Address_id = %s"
    cursor.execute(query, (Address_id,))
    db.commit()
    return jsonify({'message': 'Address deleted successfully'}), 200

# Route for 'booking' table
@app.route('/booking', methods=['POST'])
def add_booking():
    data = request.json
    # Check if the provided Hotel_Id, customer_id, and travel_id exist in their respective tables
    check_foreign_keys(data['Hotel_Id'], 'Hotels', 'Hotel_id')
    check_foreign_keys(data['customer_id'], 'customer', 'customer_id')
    check_foreign_keys(data['travel_id'], 'Travel', 'travel_id')

    query = "INSERT INTO booking (No_of_rooms, Total_cost, Hotel_Id, customer_id, travel_id) VALUES (%s, %s, %s, %s, %s)"
    values = (data['No_of_rooms'], data['Total_cost'], data['Hotel_Id'], data['customer_id'], data['travel_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Booking added successfully'}), 201

@app.route('/booking', methods=['GET'])
def get_all_bookings():
    query = "SELECT * FROM booking"
    cursor.execute(query)
    bookings = cursor.fetchall()
    result = []
    for booking in bookings:
        booking_dict = {
            "No_of_rooms": booking[0],
            "Total_cost": booking[1],
            "Hotel_Id": booking[2],
            "customer_id": booking[3],
            "travel_id": booking[4]
        }
        result.append(booking_dict)

    return jsonify({'booking': result})

@app.route('/booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    query = "DELETE FROM booking WHERE No_of_rooms = %s"
    cursor.execute(query, (booking_id,))
    db.commit()
    return jsonify({'message': 'Booking deleted successfully'}), 200

# Route for 'customer' table
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    query = "INSERT INTO customer (`Customer Name`, `Phone Number`, `Email`, `Password`) VALUES (%s, %s, %s, %s)"
    values = (data['Customer Name'], data['Phone Number'], data['Email'], data['Password'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@app.route('/customer', methods=['GET'])
def get_all_customers():
    query = "SELECT * FROM customer"
    cursor.execute(query)
    customers = cursor.fetchall()
    result = []
    for customer in customers:
        customer_dict = {
            "Customer ID": customer[0],
            "Customer Name": customer[1],
            "Phone Number": customer[2],
            "Email": customer[3],
            "Password": customer[4]
        }
        result.append(customer_dict)

    return jsonify({'customer': result})

@app.route('/customer/<int:Customer ID>', methods=['DELETE'])
def delete_customer(customer_id):
    query = "DELETE FROM customer WHERE `Customer ID` = %s"
    cursor.execute(query, (customer_id,))
    db.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Route for 'Hotels' table
@app.route('/Hotels', methods=['POST'])
def add_hotel():
    data = request.json
    # Check if the provided Address_id exists in the 'address' table
    check_foreign_keys(data['Address_id'], 'Address', 'Address_id')

    query = "INSERT INTO Hotels (Hotel_id, room_id, hotel_name, check_in_date, check_out_date, room_capacity, room_class, cost_per_night, Address_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data['Hotel_id'], data['room_id'], data['hotel_name'], data['check_in_date'], data['check_out_date'], data['room_capacity'], data['room_class'], data['cost_per_night'], data['Address_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Hotel added successfully'}), 201

@app.route('/Hotels', methods=['GET'])
def get_all_hotels():
    query = "SELECT * FROM Hotels"
    cursor.execute(query)
    hotels = cursor.fetchall()
    result = []
    for hotel in hotels:
        hotel_dict = {
            "Hotel_id": hotel[0],
            "room_id": hotel[1],
            "hotel_name": hotel[2],
            "check_in_date": hotel[3],
            "check_out_date": hotel[4],
            "room_capacity": hotel[5],
            "room_class": hotel[6],
            "cost_per_night": hotel[7],
            "Address_id": hotel[8]
            # Add more fields as needed
        }
        result.append(hotel_dict)

    return jsonify({'Hotels': result})

@app.route('/Hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    query = "DELETE FROM Hotels WHERE Hotel_id = %s"
    cursor.execute(query, (hotel_id,))
    db.commit()
    return jsonify({'message': 'Hotel deleted successfully'}), 200

# Route for 'travel' table
@app.route('/Travel', methods=['POST'])
def add_travel():
    data = request.json
    query = "INSERT INTO Travel (travel_id, vehicle_id_to, vehicle_id_from, vehicle_quantity_from, vehicle_quantity_to, Total_cost) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data['travel_id'], data['vehicle_id_to'], data['vehicle_id_from'], data['vehicle_quantity_from'], data['vehicle_quantity_to'], data['Total_cost'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Travel added successfully'}), 201

@app.route('/Travel', methods=['GET'])
def get_all_travels():
    query = "SELECT * FROM Travel"
    cursor.execute(query)
    travel = cursor.fetchall()
    result = []
    for travel_record in travel:
        travel_dict = {
            "travel_id": travel_record[0],
            "vehicle_id_to": travel_record[1],
            "vehicle_id_from": travel_record[2],
            "vehicle_quantity_from": travel_record[3],
            "vehicle_quantity_to": travel_record[4],
            "Total_cost": travel_record[5]
        }
        result.append(travel_dict)

    return jsonify({'Travel': result})

@app.route('/Travel/<int:travel_id>', methods=['DELETE'])
def delete_travel(travel_id):
    query = "DELETE FROM Travel WHERE travel_id = %s"
    cursor.execute(query, (travel_id,))
    db.commit()
    return jsonify({'message': 'Travel deleted successfully'}), 200

# Route for 'vehicle' table
@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    # Check if the provided Address_id exists in the 'address' table
    check_foreign_keys(data['Address_id'], 'Address', 'Address_id')

    query = "INSERT INTO vehicle (vehicle_id, arriving_date, vehicle_type, leaving_date, start_address_id, dest_address_id, Address_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (data['vehicle_id'], data['arriving_date'], data['vehicle_type'], data['leaving_date'], data['start_address_id'], data['dest_address_id'], data['Address_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Vehicle added successfully'}), 201

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    query = "SELECT * FROM vehicle"
    cursor.execute(query)
    vehicles = cursor.fetchall()
    result = []
    for vehicle in vehicles:
        vehicle_dict = {
            "vehicle_id": vehicle[0],
            "arriving_date": vehicle[1],
            "vehicle_type": vehicle[2],
            "leaving_date": vehicle[3],
            "start_address_id": vehicle[4],
            "dest_address_id": vehicle[5],
            "Address_id": vehicle[6]
        }
        result.append(vehicle_dict)

    return jsonify({'vehicle': result})

@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    query = "DELETE FROM vehicle WHERE vehicle_id = %s"
    cursor.execute(query, (vehicle_id,))
    db.commit()
    return jsonify({'message': 'Vehicle deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

