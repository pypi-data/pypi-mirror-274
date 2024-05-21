import slurpit  # Import the slurpit library, which provides API interaction capabilities
from slurpit.models.template import Template
import pytest

## Setup config.
# Configure the API connection by providing the host URL and the API key.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

## Create slurpit instance
# Initialize an API client instance with the specified host and API key.
api = slurpit.api(host, api_key)  # Creates an API client instance configured with the host and API key

@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture

# Fetch and print all templates
def test_get_templates():
  templates = api.templates.get_templates()  # Retrieves all templates from the API
  assert all(isinstance(device, Template) for device in templates)

# Fetch all templates and save to csv file
def test_save_csv():
  templates_csvdata = api.templates.get_templates(export_csv=True)  # Retrieves all templates from the API
  result = api.templates.save_csv_bytes(templates_csvdata, "csv/templates.csv")
  assert result == True, "failed to save csv file"


# Define data for a new template
def test_create_template(shared_data):
  new_data = {
    "device_os": "cisco_ios",
    "name": "test2",
    "command": "string",
    "content": "string"
  }

  # Create a new template and print its details
  new_template = api.templates.create_template(new_data)  # Creates a new template with the provided data
  shared_data.update(vars(new_template))
  assert isinstance(new_template, Template)

def test_update_template(shared_data):
  # Define update data for the newly created template
  update_data = {
    "device_os": "cisco_ios",
    "name": "test1",
    "command": "test",
    "content": "test"
  }

  # Update the template and print the updated information
  updated_template = api.templates.update_template(shared_data['id'], update_data)  # Updates the existing template
  assert isinstance(updated_template, Template)

# Retrieve and print the details of the updated template
def test_get_template(shared_data):
  template = api.templates.get_template(shared_data['id'])  # Fetches the template by ID
  assert isinstance(template, Template)

# Delete the template and print confirmation
def test_delete_template(shared_data):
  deleted_template = api.templates.delete_template(shared_data['id'])  # Deletes the template by ID
  assert isinstance(deleted_template, Template)

def test_search_template():
  # Define search criteria for templates
  search_data = {
    "id": 8,
    "name": "cisco_ios_show_cdp_neighbors.textfsm",
    "device_os": ["cisco_ios"],
    "search": "cisco",
    "command": "show cdp neighbors"
  }

  # Search for templates and print the results
  searched_result = api.templates.search_template(search_data)  # Searches for templates based on provided criteria
  assert isinstance(searched_result, list)

def test_run_template():
  # Define information for running a template
  run_info = {
    "hostname": "cisco_ios",
    "template_id": 162,
    "command": "dir"
  }

  # Run a template and print the result
  run_result = api.templates.run_template(run_info)  # Executes a template with the provided information
  assert isinstance(run_result, dict)

def test_validate_textfsm():
  # Validate TextFSM format
  txtfsm = """
  Value ROUTER (\d+\.\d+\.\d+\.\d+)
  Value PORT ([0-9]0?\/[1-2]\/[0-9]+|lag-[0-9]{1,3})
  Value TAG ([0-9]{1,4}|\d+.?\d+?)

  Start
    ^1\s+${ROUTER}:sap${PORT}:${TAG} -> Record
  """
  validate_result = api.templates.validate_textfsm(txtfsm)  # Validates the TextFSM template format
  assert isinstance(validate_result, dict)
  assert validate_result['valid'] == True


def test_validate_textfsm():
  # Define test data for testing TextFSM
  txtfsm = """
  Value ROUTER (\d+\.\d+\.\d+\.\d+)
  Value PORT ([0-9]0?\/[1-2]\/[0-9]+|lag-[0-9]{1,3})
  Value TAG ([0-9]{1,4}|\d+.?\d+?)

  Start
    ^1\s+${ROUTER}:sap${PORT}:${TAG} -> Record
  """

  test_data = {
    "username": "admin",
    "password": "pass",
    "ip": "192.168.1.2",
    "port": 22,
    "device_type": "cisco_ios",
    "command": "string",
    "textfsm": txtfsm
  }

  # Test TextFSM template and print the result
  test_result = api.templates.test_textfsm(test_data)  # Tests the TextFSM template with the provided data
  assert isinstance(test_result, dict)
