# BVG Python API Wrapper

This is a Python wrapper for the BVG (Berliner Verkehrsbetriebe) public transportation REST API. It provides an easy-to-use interface to interact with the BVG API and fetch transportation data such as journeys, stops, departures, nearby locations, and reachable stops.

## Features

- Fetch journeys between two locations.
- Get information about specific stops.
- Get departures from specific stops.
- Get nearby locations based on latitude and longitude.
- Get reachable stops from a specific location within a certain time frame.

## Installation

You can install the package directly from PyPI:

```sh
pip install bvg-python
```

Alternatively, you can clone the repository and install the dependencies manually:

1. Clone the repository:
    ```sh
    git clone https://github.com/tlieshoff/bvg-python.git
    cd bvg-python
    ```

2. Set up a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Example Script

An example script (`examples/example.py`) is provided to demonstrate the usage of the BVG API wrapper.

```python
from bvg_python.bvg import BVGApi
import requests
import time

def fetch_with_retries(api_call, retries=3, delay=2):
    for i in range(retries):
        try:
            result = api_call()
            if result:
                return result
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(delay)
    return None

def main():
    api = BVGApi()

    # Example 1: Get journeys from Alexanderplatz to Rosa-Luxemburg-Platz
    print("Fetching journey from Alexanderplatz to Rosa-Luxemburg-Platz...")
    journey = fetch_with_retries(lambda: api.get_journeys('S+U Alexanderplatz', 'U Rosa-Luxemburg-Platz'))
    if journey:
        print("Journey Details:", journey)
    else:
        print("No journey details available after retries.")

    # Example 2: Get information about a specific stop (Alexanderplatz)
    print("\nFetching stop information for Alexanderplatz...")
    try:
        stop_info = api.get_stop('900100003')
        if stop_info:
            print("Stop Information:", stop_info)
        else:
            print("No stop information available.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stop information: {e}")

    # Example 3: Get departures from a specific stop (Alexanderplatz)
    print("\nFetching departures from Alexanderplatz...")
    try:
        departures = api.get_departures('900100003')
        if departures:
            print("Departures:", departures)
        else:
            print("No departures available.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching departures: {e}")

    # Example 4: Get nearby locations based on latitude and longitude
    print("\nFetching nearby locations...")
    try:
        nearby_locations = api.get_nearby_locations(52.521508, 13.411267)
        if nearby_locations:
            print("Nearby Locations:", nearby_locations)
        else:
            print("No nearby locations available.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nearby locations: {e}")

    # Example 5: Get reachable stops from a specific location
    print("\nFetching reachable stops from a specific location...")
    try:
        reachable_stops = api.get_reachable_stops(52.521508, 13.411267, 'Alexanderplatz, Berlin')
        if reachable_stops:
            print("Reachable Stops:", reachable_stops)
        else:
            print("No reachable stops available.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reachable stops: {e}")

if __name__ == "__main__":
    main()

```

### More Information

For more detailed information about the BVG API, you can visit the [API documentation](https://v6.bvg.transport.rest).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---