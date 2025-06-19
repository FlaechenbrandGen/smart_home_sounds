import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def fetch_ups_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    url = "http://pi3/cgi-bin/nut/upsstats.cgi"
    ups_data = fetch_ups_data(url)
    if ups_data:
        print("UPS Data:")
        print(ups_data)
    else:
        print("Failed to retrieve UPS data.")

if __name__ == "__main__":
    main()