import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(layout="wide")

URL = "http://127.0.0.1:5000"

# Helper Fetch Functions
def get_error_lists(e_map_str):
    e_map = json.loads(e_map_str)
    e_list = []
    for e in e_map['globalErrors']:
        e_list.append(e)
    for f in list(e_map['fieldErrors'].keys()):
        for e in e_map['fieldErrors'][f]:
            e_list.append(e)
    for e in e_list:
        st.error(e)


def fetch_branch_location_ids():
    url = URL + "/branchLocation"
    response = requests.get(url)
    if response.status_code == 200:
        locations = response.json()["branchLocations"]
        return {location["id"]: location["name"] + ", " + location["company"]["name"] for location in locations}
    else:
        st.error(f"Failed to fetch branch locations. Status code: {response.status_code}")
        return []

def fetch_item_ids():
    url = URL + "/item"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json()["items"]
        return {item["id"]: item["name"] + ", " + item["batchNumber"] for item in items}
    else:
        st.error(f"Failed to fetch items. Status code: {response.status_code}")
        return []

def fetch_company_ids():
    url = URL + "/company"
    response = requests.get(url)
    if response.status_code == 200:
        companies = response.json()["companies"]
        return {company["id"]: company["name"] for company in companies}
    else:
        st.error(f"Failed to fetch company data. Status code: {response.status_code}")
        return []

def fetch_address_ids():
    url = URL + "/address"
    response = requests.get(url)
    if response.status_code == 200:
        addresses = response.json()["addresses"]
        return {address["addrId"]: address["addressLine1"] + ", " + str(address["addressLine2"]) + ", " + address["city"] + ", " + address["state"] + ", " + address["country"] + " - " + address["pincode"] for address in addresses}
    else:
        st.error(f"Failed to fetch address data. Status code: {response.status_code}")
        return []
    
def fetch_unit_codes():
    url = URL + "/unit"
    response = requests.get(url)
    if response.status_code == 200:
        units = response.json()["units"]
        return {unit["unitCode"]: unit["name"] for unit in units}
    else:
        st.error(f"Failed to fetch unit data. Status code: {response.status_code}")
        return []

# View Functions

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
        for vehicle in data["vehicles"]:
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
        for customer in data["customers"]:
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
        for Address in data["Addresses"]:
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
        for hotels in data["hotels"]:
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
    
def form_address():
    st.title("Address Form")

    address_line_1 = st.text_input("Address Line 1", "")
    address_line_2 = st.text_input("Address Line 2", "")
    city = st.text_input("City", "")
    state = st.text_input("State", "")
    country = st.text_input("Country", "")
    pincode = st.text_input("Pincode", "")

    if st.button("Submit"):
        data = {
            "addressLine1": address_line_1,
            "addressLine2": address_line_2,
            "city": city,
            "state": state,
            "country": country,
            "pincode": pincode
        }
        st.table(data)
        response = requests.post(URL + '/address', json=data)
        if response.status_code == 200:
            st.success('Data submitted successfully!')
        else:
            get_error_lists(response.text)

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

def form_company():
    st.title("Company Form")

    addresses = fetch_address_ids()
    address_ids = list(addresses.keys())

    name = st.text_input("Company Name", "")
    headquarter_address_id = st.selectbox("Headquarter Address ID", address_ids, format_func=lambda x: addresses[x])
    gstin = st.text_input("GSTIN", "")

    if st.button("Submit"):
        company_data = {
            "name": name,
            "headquarterAddress": {
                "addrId": headquarter_address_id
            },
            "gstin": gstin
        }
        st.table(company_data)

        response = requests.post(URL + "/company", json=company_data)
        if response.status_code == 200:
            st.success("Data submitted successfully!")
        else:
            get_error_lists(response.text)

def form_pi():
    st.title("Purchase Invoice Form")

    branch_locations = fetch_branch_location_ids()
    bl_ids = list(branch_locations.keys())
    
    addresses = fetch_address_ids()
    address_ids = list(addresses.keys())
    
    items = fetch_item_ids()
    item_ids = list(items.keys())

    invoice_date = st.date_input("Invoice Date", key="invoice_date")
    vendor_name = st.text_input("Vendor Name", key="vendor_name")
    branch_location_id = st.selectbox("Branch Location ID", bl_ids, format_func=lambda x: branch_locations[x], key="branch_location_id")
    billing_address_id = st.selectbox("Billing Address ID", address_ids, format_func=lambda x: addresses[x], key="billing_address_id")
    branch_location_to_send = {"id": branch_location_id}
    billing_address_to_send = {"addrId": billing_address_id}

    item_id = st.selectbox("Item ID", item_ids, format_func=lambda x: items[x], key="item_id")
    quantity = st.number_input("Quantity", min_value=1, step=1, value=1, key="quantity")
    order_items = [{"item": {"id": item_id}, "quantity": quantity}]

    # Create order items    
    # order_items = []
    # st.header("Order Items")
    # add_item_button = st.button("Add Item")
    # if add_item_button:
        # st.write(add_item_button)
        # with st.form(f"item_form {len(order_items)}"):
            # item_id = st.selectbox(f"Item ID {len(order_items)}", item_ids, key = f"item_id_{len(order_items)}")
            # quantity = st.number_input("Quantity", key=f"quantity_{len(order_items)}")
            # item = {"item": {"id": item_id}, "quantity": quantity}
            # test = test + 1
            # if st.form_submit_button("Enter Item"):
            #     order_items.append(item)
            #     st.write(f"Item {len(order_items)} added!")
            #     add_item_button = False

    if st.button("Submit"):
        invoice_data = {
            "invoiceDate": str(invoice_date),
            "branchLocation": branch_location_to_send,
            "billingAddress": billing_address_to_send,
            "vendorName": vendor_name,
            "orderItems": order_items
        }

        # st.subheader("JSON Data")
        # st.json(invoice_data)
        response = requests.post(URL + "/pi", json=invoice_data)
        if response.status_code == 200:
            st.success("Data submitted successfully!")
        else:
            get_error_lists(response.text)

def form_si():
    st.title("Sales Invoice Form")

    branch_locations = fetch_branch_location_ids()
    bl_ids = list(branch_locations.keys())
    
    addresses = fetch_address_ids()
    address_ids = list(addresses.keys())
    
    items = fetch_item_ids()
    item_ids = list(items.keys())

    invoice_date = st.date_input("Invoice Date", key="invoice_date")
    customer_name = st.text_input("Customer Name", key="vendor_name")
    branch_location_id = st.selectbox("Branch Location ID", bl_ids, format_func=lambda x: branch_locations[x], key="branch_location_id")
    billing_address_id = st.selectbox("Billing Address ID", address_ids, format_func=lambda x: addresses[x], key="billing_address_id")
    shipping_address_id = st.selectbox("Shipping Address ID", address_ids, format_func=lambda x: addresses[x], key="shipping_address_id")
    branch_location_to_send = {"id": branch_location_id}
    billing_address_to_send = {"addrId": billing_address_id}
    shipping_address_to_send = {"addrId": shipping_address_id}

    item_id = st.selectbox("Item ID", item_ids, format_func=lambda x: items[x], key="item_id")
    quantity = st.number_input("Quantity", min_value=1, step=1, value=1, key="quantity")
    order_items = [{"item": {"id": item_id}, "quantity": quantity}]

    if st.button("Submit"):
        invoice_data = {
            "invoiceDate": str(invoice_date),
            "branchLocation": branch_location_to_send,
            "billingAddress": billing_address_to_send,
            "shippingAddress": shipping_address_to_send,
            "customerName": customer_name,
            "orderItems": order_items
        }

        # st.subheader("JSON Data")
        # st.json(invoice_data)
        response = requests.post(URL + "/si", json=invoice_data)
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
#elif page == "Add Bookings":
    #form_bookings()
# elif page == "Add Travels":
# elif page == "Add Vehicles":
# elif page == "Add Customer":
# elif page == "Add Address":
# elif page == "Add Hotels":
# elif page == "Add Buses":
# elif page == "Add Flights":

