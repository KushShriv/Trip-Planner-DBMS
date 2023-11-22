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

@app.route('/Address', methods=['POST'])
def add_address():
    data = request.json
    # Insert data into the 'address' table
    query = "INSERT INTO Address (Address_id, location_name, pincode, country, house_no, street_no, locality, landmark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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

    return jsonify({'Addresses': result})

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

# Route for 'buses' table
@app.route('/buses', methods=['POST'])
def add_bus():
    data = request.json
    # Check if the provided vehicle_id exists in the 'vehicle' table
    check_foreign_keys(data['vehicle_id'], 'vehicle', 'vehicle_id')

    query = "INSERT INTO buses (vehicle_number, description, duration_mins, seat_class, travel_agency, number_seats, price_per_seat, vehicle_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data['vehicle_number'], data['description'], data['duration_mins'], data['seat_class'], data['travel_agency'], data['number_seats'], data['price_per_seat'], data['vehicle_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Bus added successfully'}), 201

@app.route('/buses', methods=['GET'])
def get_all_buses():
    query = "SELECT * FROM buses"
    cursor.execute(query)
    buses = cursor.fetchall()
    result = []
    for bus in buses:
        bus_dict = {
            "vehicle_number": bus[0],
            "description": bus[1],
            "duration_mins": bus[2],
            "seat_class": bus[3],
            "travel_agency": bus[4],
            "number_seats": bus[5],
            "price_per_seat": bus[6],
            "vehicle_id": bus[7]
            # Add more fields as needed
        }
        result.append(bus_dict)

    return jsonify({'buses': result})

@app.route('/buses/<int:bus_id>', methods=['DELETE'])
def delete_bus(bus_id):
    query = "DELETE FROM buses WHERE vehicle_number = %s"
    cursor.execute(query, (bus_id,))
    db.commit()
    return jsonify({'message': 'Bus deleted successfully'}), 200

# Route for 'cust_phone' table
@app.route('/cust_phone', methods=['POST'])
def add_cust_phone():
    data = request.json
    # Check if the provided customer_id exists in the 'customer' table
    check_foreign_keys(data['customer_id'], 'customer', 'customer_id')

    query = "INSERT INTO cust_phone (phno, customer_id) VALUES (%s, %s)"
    values = (data['phno'], data['customer_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Customer phone added successfully'}), 201

@app.route('/cust_phone', methods=['GET'])
def get_all_cust_phones():
    query = "SELECT * FROM cust_phone"
    cursor.execute(query)
    cust_phones = cursor.fetchall()
    result = []
    for phone_record in cust_phones:
        phone_dict = {
            "phno": phone_record[0],
            "customer_id": phone_record[1]
        }
        result.append(phone_dict)

    return jsonify({'customer_phones': result})

@app.route('/cust_phone/<string:phone_number>', methods=['DELETE'])
def delete_cust_phone(phone_number):
    query = "DELETE FROM cust_phone WHERE phno = %s"
    cursor.execute(query, (phone_number,))
    db.commit()
    return jsonify({'message': 'Customer phone deleted successfully'}), 200

# Route for 'customer' table
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    query = "INSERT INTO customer (customer_id, customer_name, password, email) VALUES (%s, %s, %s, %s)"
    values = (data['customer_id'], data['customer_name'], data['password'], data['email'])
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
            "customer_id": customer[0],
            "customer_name": customer[1],
            "password": customer[2],
            "email": customer[3],
        }
        result.append(customer_dict)

    return jsonify({'customers': result})

@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    query = "DELETE FROM customer WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    db.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Route for 'flights' table
@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.json
    # Check if the provided vehicle_id exists in the 'vehicle' table
    check_foreign_keys(data['vehicle_id'], 'vehicle', 'vehicle_id')

    query = "INSERT INTO flights (flight_number, price_per_seat, number_seats, airline, description, seat_class, duration_mins, vehicle_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data['flight_number'], data['price_per_seat'], data['number_seats'], data['airline'], data['description'], data['seat_class'], data['duration_mins'], data['vehicle_id'])
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Flight added successfully'}), 201

@app.route('/flights', methods=['GET'])
def get_all_flights():
    query = "SELECT * FROM flights"
    cursor.execute(query)
    flights = cursor.fetchall()
    result = []
    for flight in flights:
        flight_dict = {
            "flight_number": flight[0],
            "price_per_seat": flight[1],
            "number_seats": flight[2],
            "airline": flight[3],
            "description": flight[4],
            "seat_class": flight[5],
            "duration_mins": flight[6],
            "vehicle_id": flight[7]
        }
        result.append(flight_dict)

    return jsonify({'flights': result})

@app.route('/flights/<int:flight_number>', methods=['DELETE'])
def delete_flight(flight_number):
    query = "DELETE FROM flights WHERE flight_number = %s"
    cursor.execute(query, (flight_number,))
    db.commit()
    return jsonify({'message': 'Flight deleted successfully'}), 200

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

    return jsonify({'hotels': result})

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

    return jsonify({'vehicles': result})

@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    query = "DELETE FROM vehicle WHERE vehicle_id = %s"
    cursor.execute(query, (vehicle_id,))
    db.commit()
    return jsonify({'message': 'Vehicle deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

