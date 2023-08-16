import requests
import json
import asyncio
# Set your Naver API credentials
def calculate_distance(address,start):
    client_id = 'hvid9avxqf'
    client_secret = 'yVe8kRQLMISDknnJAY6zhdOL6NbMbFL6rb1OESqq'

    # Define the starting and destination addresses
    start_address = start
    destination_address = address

    # Get the coordinates (latitude and longitude) of the starting point using Geocoding API
    start_url = f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={start_address}'
    proxies = {
    "http": None,
    "https": None
    }

    headers = {
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret
    }

    start_response = requests.get(start_url, headers=headers, proxies=proxies).json()

    try:
        # Extract coordinates if available
        if 'addresses' in start_response and len(start_response['addresses']) > 0:
            start_coords = start_response['addresses'][0]['x'], start_response['addresses'][0]['y']
            # print(f"The coordinates of the starting point ({start_address}) are latitude: {start_coords[0]}, longitude: {start_coords[1]}.")
        else:
            print("No coordinates found for the starting point.")
    except KeyError as e:
        print("An error occurred while parsing the response:", e)

    # Get the coordinates (latitude and longitude) of the destination using Geocoding API
    destination_url = f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={destination_address}'

    destination_response = requests.get(destination_url, headers=headers).json()

    try:
        # Extract coordinates if available
        if 'addresses' in destination_response and len(destination_response['addresses']) > 0:
            destination_coords = destination_response['addresses'][0]['x'], destination_response['addresses'][0]['y']
            # print(f"The coordinates of the destination ({destination_address}) are latitude: {destination_coords[0]}, longitude: {destination_coords[1]}.")
        else:
            print("No coordinates found for the destination.")
    except KeyError as e:
        print("An error occurred while parsing the response:", e)

    # Calculate walking distance using the Directions API
    try:
        directions_url = f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={start_coords[0]},{start_coords[1]}&goal={destination_coords[0]},{destination_coords[1]}'
    except:
        return -4

    directions_response = requests.get(directions_url, headers=headers).json()
    duration  = int(directions_response["route"]["traoptimal"][0]["summary"]["duration"])

    duration = duration / 1000 / 60 
    return int(duration)
import googlemaps
from googlemaps.exceptions import ApiError

# def calculate_distance(address,start):
#     # Replace 'YOUR_API_KEY' with your actual API key
#     api_key = 'AIzaSyC4A770PO5RfcOQQsAJ-_HmJQVVzn3YaC8'
#     gmaps = googlemaps.Client(key=api_key)

#     origin = start
#     destination = address
#     try:

#         directions_result = gmaps.directions(origin, destination, mode="driving")

#         if directions_result:
#             duration = directions_result[0]['legs'][0]['duration']['text']

#             duration = int(duration)
#             duration = duration / 1000 / 60 
#             return int(duration)
#         else:
#             print("No directions found.")
#             return -4
#     except ApiError as e:
#         print("An API error occurred:")
#         print(e)






