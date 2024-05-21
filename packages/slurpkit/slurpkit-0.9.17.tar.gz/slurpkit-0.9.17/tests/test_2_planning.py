import slurpit  # Import the slurpit library, which is assumed to contain API client functionalities.
import pytest
from slurpit.models.planning import Planning
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)  

@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture

def test_get_plannings():
  # Retrieve plannings
  plannings = api.planning.get_plannings()
  assert all(isinstance(item, Planning) for item in plannings)

def test_save_csv():
  # Retrieve plannings
  plannings_csvdata = api.planning.get_plannings(export_csv=True)
  result = api.device.save_csv_bytes(plannings_csvdata, "csv/plannings.csv")
  assert result == True, "Failed to save csv file"

# Search data configuration
def test_search_plannings():
  search_data = {
    "planning_id": 3,  # ID of the planning entry to search
    "hostnames": ["device1"],  # List of hostnames to include in the search
    "device_os": ["cisco_ios"],  # List of operating systems to include in the search
    "search": "cisco",  # Search keyword
    "unique_results": False,  # Flag to determine whether to return unique results only
    "start_date": "2023-12-01 00:30",  # Start date for the search interval
    "end_date": "2023-12-31 22:30",  # End date for the search interval
    "offset": 0,  # Offset for pagination
    "limit": 1000  # Maximum number of results to return
  }
      
  search_result = api.planning.search_plannings(search_data)
  assert isinstance(search_result, dict)

# Data for planning regeneration
def test_regenerate_unique():
  updated_info = api.planning.regenerate_unique(3)
  assert isinstance(updated_info, dict)
