import requests

class BVGApi:
    def __init__(self):
        self.base_url = 'https://v6.bvg.transport.rest/'
        print("BVGApi initialized")

    def get_journeys(self, from_place, to_place, timeout=10):
        print("Called get_journeys")
        url = f"{self.base_url}journeys"
        params = {'from': from_place, 'to': to_place}
        return self._make_request(url, params, timeout)

    def get_stop(self, stop_id, timeout=10):
        print("Called get_stop")
        url = f"{self.base_url}stops/{stop_id}"
        return self._make_request(url, timeout=timeout)

    def get_departures(self, stop_id, duration=10, timeout=10):
        print("Called get_departures")
        url = f"{self.base_url}stops/{stop_id}/departures"
        params = {'duration': duration}
        return self._make_request(url, params, timeout)

    def get_arrivals(self, stop_id, duration=10, timeout=10):
        print("Called get_arrivals")
        url = f"{self.base_url}stops/{stop_id}/arrivals"
        params = {'duration': duration}
        return self._make_request(url, params, timeout)

    def get_locations(self, query, results=10, timeout=10):
        print("Called get_locations")
        url = f"{self.base_url}locations"
        params = {'query': query, 'results': results}
        return self._make_request(url, params, timeout)

    def get_nearby_locations(self, latitude, longitude, results=8, timeout=10):
        print("Called get_nearby_locations")
        url = f"{self.base_url}locations/nearby"
        params = {'latitude': latitude, 'longitude': longitude, 'results': results}
        return self._make_request(url, params, timeout)

    def get_reachable_stops(self, latitude, longitude, address, when=None, max_transfers=5, max_duration=None, timeout=10):
        print("Called get_reachable_stops")
        url = f"{self.base_url}stops/reachable-from"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'address': address,
            'when': when,
            'maxTransfers': max_transfers,
            'maxDuration': max_duration
        }
        return self._make_request(url, params, timeout)

    def get_trip(self, trip_id, timeout=10):
        print("Called get_trip")
        url = f"{self.base_url}trips/{trip_id}"
        return self._make_request(url, timeout=timeout)

    def get_radar(self, north, west, south, east, results=256, duration=30, timeout=10):
        print("Called get_radar")
        url = f"{self.base_url}radar"
        params = {
            'north': north,
            'west': west,
            'south': south,
            'east': east,
            'results': results,
            'duration': duration
        }
        return self._make_request(url, params, timeout)

    def get_stops(self, query=None, results=5, fuzzy=False, completion=True, timeout=10):
        print("Called get_stops")
        url = f"{self.base_url}stops"
        params = {'query': query, 'results': results, 'fuzzy': fuzzy, 'completion': completion}
        return self._make_request(url, params, timeout)

    def refresh_journey(self, ref, stopovers=False, tickets=False, polylines=False, subStops=True, entrances=True, remarks=True, scheduledDays=False, language='en', pretty=True, timeout=10):
        print("Called refresh_journey")
        url = f"{self.base_url}journeys/{ref}"
        params = {
            'stopovers': stopovers,
            'tickets': tickets,
            'polylines': polylines,
            'subStops': subStops,
            'entrances': entrances,
            'remarks': remarks,
            'scheduledDays': scheduledDays,
            'language': language,
            'pretty': pretty
        }
        return self._make_request(url, params, timeout)

    def get_trips(self, query=None, when=None, fromWhen=None, untilWhen=None, onlyCurrentlyRunning=True, currentlyStoppingAt=None, lineName=None, operatorNames=None, stopovers=True, remarks=True, subStops=True, entrances=True, language='en', pretty=True, timeout=10):
        print("Called get_trips")
        url = f"{self.base_url}trips"
        params = {
            'query': query,
            'when': when,
            'fromWhen': fromWhen,
            'untilWhen': untilWhen,
            'onlyCurrentlyRunning': onlyCurrentlyRunning,
            'currentlyStoppingAt': currentlyStoppingAt,
            'lineName': lineName,
            'operatorNames': operatorNames,
            'stopovers': stopovers,
            'remarks': remarks,
            'subStops': subStops,
            'entrances': entrances,
            'language': language,
            'pretty': pretty
        }
        return self._make_request(url, params, timeout)

    def _make_request(self, url, params=None, timeout=10):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("The request timed out")
            return None
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
