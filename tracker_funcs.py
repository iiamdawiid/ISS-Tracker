import requests
from colorama import Fore, Style
import folium
import time


def get_iss_position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    if response.status_code == 200:
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
        return float(latitude), float(longitude)
    else:
        raise Exception(f"\n{Fore.RED}ERROR: Could not fetch data{Style.RESET_ALL}\n")
    

def update_map(latitude, longitude):
    iss_map = folium.Map(location=[latitude,longitude],zoom_start=3)

    folium.Marker(
        location=[latitude,longitude],
        popup="International Space Station",
        icon=folium.Icon(color="blue",icon="info-sign")
    ).add_to(iss_map)

    return iss_map


def track_iss():
    try:
        while True:
            latitude, longitude = get_iss_position()
            iss_map = update_map(latitude, longitude)
            iss_map.save("iss_position.html")
            print(f"\n{Fore.GREEN}UPDATED ISS POSITION: Latitude:{Style.RESET_ALL} {latitude}, {Fore.GREEN}Longitude:{Style.RESET_ALL} {longitude}\n")
            time.sleep(10)

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}TRACKING STOPPED{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}\n")