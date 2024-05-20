import unittest
from bvg_python.bvg import BVGApi
from unittest.mock import patch

class TestBVGApi(unittest.TestCase):
    @patch('bvg_python.bvg.requests.get')
    def test_get_journeys(self, mock_get):
        print("Testing get_journeys")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'journeys': 'dummy_data'}
        
        result = api.get_journeys('Berlin', 'Potsdam')
        self.assertEqual(result, {'journeys': 'dummy_data'})
    
    @patch('bvg_python.bvg.requests.get')
    def test_get_stop(self, mock_get):
        print("Testing get_stop")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'stop': 'dummy_data'}
        
        result = api.get_stop('900000100001')
        self.assertEqual(result, {'stop': 'dummy_data'})
    
    @patch('bvg_python.bvg.requests.get')
    def test_get_departures(self, mock_get):
        print("Testing get_departures")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'departures': 'dummy_data'}
        
        result = api.get_departures('900000100001')
        self.assertEqual(result, {'departures': 'dummy_data'})
    
    @patch('bvg_python.bvg.requests.get')
    def test_get_arrivals(self, mock_get):
        print("Testing get_arrivals")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'arrivals': 'dummy_data'}
        
        result = api.get_arrivals('900000100001')
        self.assertEqual(result, {'arrivals': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_locations(self, mock_get):
        print("Testing get_locations")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'locations': 'dummy_data'}
        
        result = api.get_locations('Alexanderplatz')
        self.assertEqual(result, {'locations': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_nearby_locations(self, mock_get):
        print("Testing get_nearby_locations")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'nearby': 'dummy_data'}
        
        result = api.get_nearby_locations(52.52725, 13.4123)
        self.assertEqual(result, {'nearby': 'dummy_data'})
    
    @patch('bvg_python.bvg.requests.get')
    def test_get_reachable_stops(self, mock_get):
        print("Testing get_reachable_stops")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'reachable': 'dummy_data'}
        
        result = api.get_reachable_stops(52.52446, 13.40812, '10178 Berlin-Mitte, Münzstr. 12')
        self.assertEqual(result, {'reachable': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_trip(self, mock_get):
        print("Testing get_trip")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'trip': 'dummy_data'}
        
        result = api.get_trip('trip_id')
        self.assertEqual(result, {'trip': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_trips(self, mock_get):
        print("Testing get_trips")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'trips': 'dummy_data'}
        
        result = api.get_trips('query')
        self.assertEqual(result, {'trips': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_radar(self, mock_get):
        print("Testing get_radar") 
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'radar': 'dummy_data'}
        
        result = api.get_radar(52.52411, 13.41002, 52.51942, 13.41709)
        self.assertEqual(result, {'radar': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_get_stops(self, mock_get):
        print("Testing get_stops") 
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'stops': 'dummy_data'}
        
        result = api.get_stops()
        self.assertEqual(result, {'stops': 'dummy_data'})

    @patch('bvg_python.bvg.requests.get')
    def test_refresh_journey(self, mock_get):
        print("Testing refresh_journey")
        api = BVGApi()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'refresh': 'dummy_data'}
        
        result = api.refresh_journey('ref')
        self.assertEqual(result, {'refresh': 'dummy_data'})

if __name__ == '__main__':
    unittest.main()
