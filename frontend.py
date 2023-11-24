import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(layout="wide")

URL = "http://127.0.0.1:5000"

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
    st.title(f"{table.capitalize()}")
    result = fetch_table_attribute(table, attribute_list)
    if result == "Error retrieving data":
        st.error(result)
    else:
        df = pd.DataFrame(result)
        st.table(df)
    return None

def add_customer():
    st.title("Register Customer")

    customer_name = st.text_input("Full Name")
    customer_phone_no = st.text_input("Phone Number")
    customer_email = st.text_input("Email ID")
    customer_password = st.text_input("Password")
    if st.button("Register"):
        data = {
            "Customer Name": customer_name,
            "Phone Number": customer_phone_no,
            "Email": customer_email,
            "Password": customer_password
        }
        customer_detail = data
        response = requests.post(URL + '/customer', json=data)
        if response.status_code == 201:
            st.success('Data submitted successfully!')
        else:
            st.error(f"Unable to Register")
# '''
# def book_trip():
#     address_data = fetch_table_attribute("Address")
#     bus_data = fetch_table_attribute("buses")
#     st.write("Buses")
#     st.table(bus_data)
#     flight_data = fetch_table_attribute("flights")
#     st.write("Flights")
#     st.table(flight_data)
#     vehicle_data = fetch_table_attribute("vehicle")
#     customer_data = fetch_table_attribute("customer")
#     st.table(customer_data)
#     st.write("Hotels")
#     hotel_data = fetch_table_attribute("Hotels")
#     st.table(hotel_data)
#
#     customer_ids = []
#     for i in customer_data:
#         customer_ids.append(i["customer_id"])
#     customer_id = st.selectbox("Customer_ID", customer_ids)
#     hotel_ids = []
#     for i in hotel_data:
#         hotel_ids.append(i["Hotel_id"])
#     hotel_id = st.selectbox("Hotel_ID", hotel_ids)
#     rooms = st.number_input("Select Number of Rooms Required")
#     bus_ids = []
#     vehicle_ids = []
#     for i in bus_data:
#         bus_ids.append(i["vehicle_id"])
#         vehicle_ids.append(i["vehicle_id"])
#     flight_ids = []
#     for i in flight_data:
#         flight_ids.append(i["vehicle_id"])
#         vehicle_ids.append(i["vehicle_id"])
#     selection1 = st.selectbox("Select Transport to Destination", vehicle_ids)
#     q1 = st.number_input("number of seats to")
#     selection2 = st.selectbox("Select Transport from Destination", vehicle_ids)
#     q2 = st.number_input("number of seats from")
#
#     if st.button("Book Trip"):
#         data1 = {
#             "travel_id": 5,
#             "vehicle_id_to": selection1,
#             "vehicle_id_from": selection2,
#             "vehicle_quantity_from": q1,
#             "vehicle_quantity_to": q2,
#             "Total_cost": 60000
#         }
#         response = requests.post(URL + "/Travel", json=data1)
#         if response.status_code == 201:
#             st.success("Data1 submitted successfully!")
#             data2 = {
#                 "No_of_rooms": rooms,
#                 "Total_cost": 90000,
#                 "Hotel_Id": hotel_id,
#                 "customer_id": customer_id,
#                 "travel_id": 5
#             }
#             response2 = requests.post(URL + "/booking", json= data2)
#             if response2.status_code == 201:
#                 st.success("Data2 submitted successfully!")
#             else:
#                 st.error("Data 2 not submitted")
#         else:
#             st.error("Data 1 not submitted")
#     # selection1 = st.selectbox("Select Transport Type", vehicle_ids)
#     # for i in vehicle_ids:
#     #     if selection1 == i:
#     #         st.selectbox("Select Flight to destination", vehicle_ids["flights"])
#     #     else:
#     #         st.selectbox("Select Bus to destination", vehicle_ids["buses"])
#
#     # st.write(address_data, bus_data, flight_data, vehicle_data, customer_data, hotel_data)
# '''

def book_trip():
    st.title("Book Trip")
    address_data = fetch_table_attribute('address')
    customer_data = fetch_table_attribute('customer')
    hotel_data = fetch_table_attribute('hotel')
    transport_data = fetch_table_attribute('transport')

    full_address = [f"{address['Address ID']} - {address['District']}, {address['City']}, {address['State']}, {address['Country']}" for address in address_data]
    customer = st.selectbox("Select Customer", [f"{customer['Customer ID']} - {customer['Customer Name']} - {customer['Email']}" for customer in customer_data])
    start_from = st.selectbox("Select Current Address", full_address)
    destination = st.selectbox("Select Destination Address", full_address)
    # st.write(f"{customer}\n{start_from}\n{destination}")
    filtered_transport_to = [f"{transport['Transport ID']} - {transport['Transport Type']} will take {transport['Travel Time']} hours and costs ${transport['Price Per Seat']} per seat" for transport in transport_data if transport["Start Address ID"] == int(start_from.split()[0]) and transport["Destination Address ID"] == int(destination.split()[0])]
    transport_to = st.selectbox("Select Transport to the Destination", filtered_transport_to)
    seats_to = st.number_input("Select Number of seats in the travel to the destination")
    transport_to_price = int(requests.get(f"{URL}/transport/{int(transport_to.split()[0])}").json()['transport'][0]['Price Per Seat'])
    # st.write(transport_to_price)

    filtered_hotels = [f"{hotel['Hotel ID']} - {hotel['Hotel Name']} offering {hotel['Room Class']} with a capacity of {hotel['Room Capacity']} - ${hotel['Cost Per Night']} Per Night" for hotel in hotel_data if hotel['Address ID'] == int(destination.split()[0])]
    hotel = st.selectbox("Select Hotel", filtered_hotels)
    nights = st.number_input("Select Number of Nights you want to stay")
    hotel_price = int(requests.get(f"{URL}/hotel/{int(hotel.split()[0])}").json()['hotel'][0]['Cost Per Night'])

    filtered_transport_from = [f"{transport['Transport ID']} - {transport['Transport Type']} will take {transport['Travel Time']} hours and costs ${transport['Price Per Seat']} per seat" for transport in transport_data if transport["Start Address ID"] == int(destination.split()[0]) and transport["Destination Address ID"] == int(start_from.split()[0])]
    transport_from = st.selectbox("Select Transport from the Destination", filtered_transport_from)
    seats_from = st.number_input("Select Number of seats in the travel from the destination")
    transport_from_price = int(requests.get(f"{URL}/transport/{int(transport_from.split()[0])}").json()['transport'][0]['Price Per Seat'])

    if st.button("Book Trip"):
        st.write(int(transport_to.split()[0]),int(transport_from.split()[0]),int(seats_to),int(seats_from),int(transport_to_price*seats_to + transport_from_price*seats_from))
        travel_data = {
            "Transport ID To Destination": int(transport_to.split()[0]),
            "Transport ID From Destination": int(transport_from.split()[0]),
            "Number of Seats To Destination": int(seats_to),
            "Number of Seats From Destination": int(seats_from),
            "Total Cost": int(transport_to_price*seats_to + transport_from_price*seats_from)
        }
        response = requests.post(f"{URL}/travel", json = travel_data)
        if response.status_code == 201:
            st.success("Travel Table Updated!")
            travel = requests.get(f"{URL}/travel").json()['travel'][-1]
            st.write(travel)
            trip_data = {
                "Customer ID": int(customer.split()[0]),
                "Hotel ID": int(hotel.split()[0]),
                "Travel ID": int(travel['Travel ID']),
                "Total Cost": int(travel['Total Cost']) + hotel_price*nights
            }
            response = requests.post(f"{URL}/trip", json=trip_data)
            if response.status_code == 201:
                st.success("Trip Data Updated!")
            else:
                st.error("Unable to Update Trip Table")
        else:
            st.error("Unable to Update Travel Table")


# Sidebar menu
from streamlit_option_menu import option_menu
with st.sidebar:
    page = option_menu(menu_title=None, options=[
        "View Trips",
        "View Travels",
        "View Transport",
        "View Customers",
        "View Addresses",
        "View Hotels",
        "Add Trips",
        "Add Customers",
    ])
if page == "View Trips":
    directly_display("trip")
elif page == "View Travels":
    directly_display('travel')
elif page == "View Transport":
    directly_display('transport')
elif page == "View Customers":
    directly_display('customer')
elif page == "View Addresses":
    directly_display('address')
elif page == "View Hotels":
    directly_display('hotel')
elif page == "Add Trips":
    book_trip()
elif page == "Add Customers":
    add_customer()
