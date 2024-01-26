import phonenumbers
from phonenumbers import geocoder, carrier
import folium
import requests

number = "+27748598367"
BING_MAPS_API_KEY = "Au8v-vsubpU1ULMpcH3UqDiFX1dCq4r4mLavOToU2AkqeP__f8_QsleuSsGUstFC"

if len(number) <= phonenumbers.phonenumberutil._MAX_INPUT_STRING_LENGTH:
    try:
        check_number = phonenumbers.parse(number)
        # Continue processing with the parsed phone number
    except phonenumbers.NumberFormatException as e:
        print(f"Error parsing phone number: {e}")
else:
    print("Invalid phone number: Input string length exceeds maximum allowed.")

check_number = phonenumbers.parse(number)
number_location = geocoder.description_for_number(check_number, "en")
print(number_location)

service_provider = phonenumbers.parse(number)
print(carrier.name_for_number(service_provider, "en"))

bing_maps_api_url = f'https://dev.virtualearth.net/REST/v1/Locations?q={number_location}&key={BING_MAPS_API_KEY}'
response = requests.get(bing_maps_api_url)
data = response.json()

if 'resourceSets' in data and data['resourceSets']:
    coordinates = data['resourceSets'][0]['resources'][0]['point']['coordinates']
    lat, lng = coordinates
    print(lat, lng)

    map_location = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=number_location).add_to(map_location)
    map_location.save("mylocation.html")
else:
    print("Error retrieving location information from Bing Maps API.")
