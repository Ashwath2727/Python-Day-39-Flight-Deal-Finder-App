#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import time
import datetime as dt
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
# flight_data = FlightData()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)

print(f"sheet_data: \n{sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()


tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_month_from_today = dt.datetime.now() + dt.timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}.....")

    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination["city"]}: £{cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")

        stop_over_flights = flight_search.check_flights(
            origin_city_code=ORIGIN_CITY_IATA,
            destination_city_code=destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False,
        )

        cheapest_flight = find_cheapest_flight(stop_over_flights)
        print(f"Cheapest indirect flight price is £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")

        message_body = f"Low price alert! Only £{cheapest_flight.price} to fly "
        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."

        notification_manager.send_notification(message_body)
