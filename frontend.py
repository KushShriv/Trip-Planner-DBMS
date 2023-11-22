import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(layout="wide")

URL = "http://127.0.0.1:5000"




def directly_display(table, attribute_list = []):
    st.title(f"{table.capitalize()}s")
    result = fetch_table_attribute(table, attribute_list)
    if result == "Error retrieving data":
        st.error(result)
    else:
        df = pd.DataFrame(result)
        st.table(df)
    return None

def view_bookings():
    directly_display("booking")

def view_travels():
    st.title("Travels")
    table = "Travel"
    result = fetch_table_attribute(table)
    if result == "Error retrieving data":
        st.error(result)
    else:
        df = pd.DataFrame(result)
        st.table(df)

def view_vehicles():
    st.title("Vehicles")
    url = URL + "/vehicle"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for vehicle in data["vehicle"]:
            table_data.append({
                "Vehicle ID": vehicle["vehicle_id"],
                "Arriving date": vehicle["arriving_date"],
                "Vehicle type": vehicle["vehicle_type"],
                "Leaving date": vehicle["leaving_date"],
                "Dest address ID": vehicle["dest_address_id"],
                "Address ID": vehicle["Address_id"]
            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

def view_customer():
    st.title("Customers")
    url = URL + "/customer"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for customer in data["customer"]:
            table_data.append({
                "Customer ID": customer["customer_id"],
                "Customer name": customer["customer_name"],
                "Password": customer["password"],
                "Email": customer["email"]

            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

def view_address():
    st.title("Addresses")
    url = URL + "/Address"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for Address in data["Address"]:
            table_data.append({
                "Address ID": Address["Address_id"],
                "Location name": Address["location_name"],
                "Pincode": Address["pincode"],
                "Country": Address["country"],
                "House no": Address["house_no"],
                "Street no": Address["street_no"],
                "Locality": Address["locality"],
                "Landmark": Address["landmark"]
            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

def view_hotels():
    st.title("Hotels")
    url = URL + "/Hotels"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for hotels in data["Hotels"]:
            table_data.append({
                "Hotel ID": hotels["Hotel_id"],
                "Room ID": hotels["room_id"],
                "Hotel Name": hotels["hotel_name"],
                "Check in date": hotels["check_in_date"],
                "Check out date": hotels["check_out_date"],
                "Room capacity": hotels["room_capacity"],
                "Room class": hotels["room_class"],
                "Cost per night": hotels["cost_per_night"],
                "Address ID": hotels["Address_id"]
            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

def view_buses():
    st.title("Buses")
    url = URL + "/buses"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for buses in data["buses"]:
            table_data.append({
                "Vehicle number": buses["vehicle_number"],
                "Description": buses["description"],
                "Duration mins": buses["duration_mins"],
                "Seat class": buses["seat_class"],
                "Travel agency": buses["travel_agency"],
                "Number seats": buses["number_seats"],
                "Price per seat": buses["price_per_seat"],
                "Vehicle ID": buses["vehicle_id"]

            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

def view_flights():
    st.title("Flights")
    url = URL + "/flights"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_data = []
        for flights in data["flights"]:
            table_data.append({
                "Flight number": flights["flight_number"],
                "Price per seat": flights["price_per_seat"],
                "Number seats": flights["number_seats"],
                "Airline": flights["airline"],
                "Description": flights["description"],
                "Seat class": flights["seat_class"],
                "Duartion mins": flights["duration_mins"],
                "Vehicle ID": flights["vehicle_id"]

            })
        df = pd.DataFrame(table_data)
        st.table(df)
    else:
        st.error("Error retrieving data.")

# Form Functions
def form_unit():
    st.title("Unit Form")
    
    unit_code = st.text_input("Unit code")
    unit_name = st.text_input("Unit name")
    fractional = st.checkbox("Fractional")
    fractional_digits = st.number_input("Fractional digits", value = 0)
    
    submit_button = st.button("Submit")

    if submit_button:
        data = {
            "unitCode": unit_code,
            "name": unit_name,
            "fractionalDigits": fractional_digits,
            "fractional": fractional
            }
        st.table(data)
        response = requests.post(URL + '/unit', json=data)
        if response.status_code == 200:
            st.success('Data submitted successfully!')
        else:
            get_error_lists(response.text)

def form_item():
    st.title("Item Form")

    units = fetch_unit_codes()
    unit_codes = list(units.keys())

    name = st.text_input("Item Name", "")
    batch_number = st.text_input("Batch Number", "")
    unit_code = st.selectbox("Unit", unit_codes, format_func=lambda x: units[x])
    selling_price = st.number_input("Selling Price", min_value=0.0)
    purchase_price = st.number_input("Purchase Price", min_value=0.0)
#    opening_balance_date = st.date_input("Opening Balance Date", value=None)
#    opening_balance_qty = st.number_input("Opening Balance Quantity", min_value=0)
    expiry_date = st.date_input("Expiry Date", value=None)
    
    if st.button("Submit"):
        item_data = {
            "name": name,
            "batchNumber": batch_number,
            "unit": {
                "unitCode": unit_code
            },
            "sellingPrice": selling_price,
            "purchasePrice": purchase_price,
#            "openingBalanceDate": str(opening_balance_date),
#            "openingBalanceQty": opening_balance_qty,
            "expiryDate": str(expiry_date) if expiry_date else ""
        }

        st.table(item_data)

        response = requests.post(URL + "/item", json=item_data)
        if response.status_code == 200:
            st.success("Data submitted successfully!")
        else:
            get_error_lists(response.text)

def fetch_table_attribute(table, attribute_list = []):
    url = f"{URL}/{table}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result_list = []
        for item in data[table]:
            if attribute_list:
                filtered_item = {key: item.get(key) for key in attribute_list}
                result_list.append(filtered_item)
            else:
                result_list.append(item)
        return result_list
    else:
        return "Error retrieving data"

def add_customer():
    st.title("Register Customer")

    customer_name = st.text_input("Full Name")
    customer_phone_no = st.text_input("Phone Number")
    customer_email = st.text_input("Email ID")
    customer_password = st.text_input("Password")
    if st.button("Register"):
        customer_data = {
            "customer_id": 5,
            "customer_name": customer_name,
            "password": customer_password,
            "email": customer_email,
        }
        customer_phone_data = {
            "phno": customer_phone_no,
            "customer_id": 5
        }
        response1 = requests.post(URL + '/customer', json=customer_data)
        response2 = requests.post(URL + '/cust_phone', json = customer_phone_data)
        if response1.status_code == 201:
            st.success('Data1 submitted successfully!')
        if response2.status_code == 201:
            st.success('Data2 submitted successfully!')
        else:
            st.error(f"Unable to Register")

def book_trip():
    address_data = fetch_table_attribute("Address")
    bus_data = fetch_table_attribute("buses")
    st.write("Buses")
    st.table(bus_data)
    flight_data = fetch_table_attribute("flights")
    st.write("Flights")
    st.table(flight_data)
    vehicle_data = fetch_table_attribute("vehicle")
    customer_data = fetch_table_attribute("customer")
    st.table(customer_data)
    st.write("Hotels")
    hotel_data = fetch_table_attribute("Hotels")
    st.table(hotel_data)

    customer_ids = []
    for i in customer_data:
        customer_ids.append(i["customer_id"])
    customer_id = st.selectbox("Customer_ID", customer_ids)
    hotel_ids = []
    for i in hotel_data:
        hotel_ids.append(i["Hotel_id"])
    hotel_id = st.selectbox("Hotel_ID", hotel_ids)
    rooms = st.number_input("Select Number of Rooms Required")
    bus_ids = []
    vehicle_ids = []
    for i in bus_data:
        bus_ids.append(i["vehicle_id"])
        vehicle_ids.append(i["vehicle_id"])
    flight_ids = []
    for i in flight_data:
        flight_ids.append(i["vehicle_id"])
        vehicle_ids.append(i["vehicle_id"])
    selection1 = st.selectbox("Select Transport to Destination", vehicle_ids)
    q1 = st.number_input("number of seats to")
    selection2 = st.selectbox("Select Transport from Destination", vehicle_ids)
    q2 = st.number_input("number of seats from")

    if st.button("Book Trip"):
        data1 = {
            "travel_id": 5,
            "vehicle_id_to": selection1,
            "vehicle_id_from": selection2,
            "vehicle_quantity_from": q1,
            "vehicle_quantity_to": q2,
            "Total_cost": 60000
        }
        response = requests.post(URL + "/Travel", json=data1)
        if response.status_code == 201:
            st.success("Data1 submitted successfully!")
            data2 = {
                "No_of_rooms": rooms,
                "Total_cost": 90000,
                "Hotel_Id": hotel_id,
                "customer_id": customer_id,
                "travel_id": 5
            }
            response2 = requests.post(URL + "/booking", json= data2)
            if response2.status_code == 201:
                st.success("Data2 submitted successfully!")
            else:
                st.error("Data 2 not submitted")
        else:
            st.error("Data 1 not submitted")
    # selection1 = st.selectbox("Select Transport Type", vehicle_ids)
    # for i in vehicle_ids:
    #     if selection1 == i:
    #         st.selectbox("Select Flight to destination", vehicle_ids["flights"])
    #     else:
    #         st.selectbox("Select Bus to destination", vehicle_ids["buses"])

    # st.write(address_data, bus_data, flight_data, vehicle_data, customer_data, hotel_data)
def form_branchLocation():
    st.title("Branch Location Form")

    companies = fetch_company_ids()
    company_ids = list(companies.keys())

    addresses = fetch_address_ids()
    address_ids = list(addresses.keys())

    name = st.text_input("Branch Location Name", "")
    company_id = st.selectbox("Company ID", company_ids, format_func=lambda x: companies[x])
    address_id = st.selectbox("Address ID", address_ids, format_func=lambda x: addresses[x])

    if st.button("Submit"):
        branch_location_data = {
            "name": name,
            "company": {
                "id": company_id
            },
            "address": {
                "addrId": address_id
            }
        }
        st.table(branch_location_data)

        response = requests.post(URL + "/branchLocation", json=branch_location_data)
        if response.status_code == 200:
            st.success("Data submitted successfully!")
        else:
            get_error_lists(response.text)


# Sidebar menu
from streamlit_option_menu import option_menu
with st.sidebar:
    page = option_menu(menu_title=None, options=[
        "View Bookings",
        "View Travels",
        "View Vehicles",
        "View Customer",
        "View Address",
        "View Hotels",
        "View Buses",
        "View Flights",
        "Add Bookings",
        "Add Travels",
        "Add Vehicles",
        "Add Customer",
        "Add Address",
        "Add Hotels",
        "Add Buses",
        "Add Flights",
    ])
# menu = [
#     "View Bookings",
#     "View Travels",
#     "View Vehicles",
#     "View Customer",
#     "View Address",
#     "View Hotels",
#     "View Buses",
#     "View Flights",
#     "Add Bookings",
#     "Add Travels",
#     "Add Vehicles",
#     "Add Customer",
#     "Add Address",
#     "Add Hotels",
#     "Add Buses",
#     "Add Flights",
#
# ]
# page = st.sidebar.selectbox("Menu", menu)

# Render page
if page == "View Bookings":
    view_bookings()
elif page == "View Travels":
    view_travels()
elif page == "View Vehicles":
    view_vehicles()
elif page == "View Customer":
    view_customer()
elif page == "View Address":
    view_address()
elif page == "View Hotels":
    view_hotels()
elif page == "View Buses":
    view_buses()
elif page == "View Flights":
    view_flights()
elif page == "Add Bookings":
    book_trip()
# elif page == "Add Travels":
# elif page == "Add Vehicles":
elif page == "Add Customer":
    add_customer()
# elif page == "Add Address":
# elif page == "Add Hotels":
# elif page == "Add Buses":
# elif page == "Add Flights":

