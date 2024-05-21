import slurpit  # Import the slurpit library.
import pytest
from slurpit.models.vault import Vault
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)  

@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture

def test_get_vaults():
  # Retrieve and print all vaults using the API.
  vaults = api.vault.get_vaults()
  assert all(isinstance(item, Vault) for item in vaults)

def test_save_csv():
  # Retrieve all vaults save to csv
  vaults_csvdata = api.vault.get_vaults(export_csv=True)
  result = api.vault.save_csv_bytes(vaults_csvdata, "csv/vaults.csv")
  assert result == True, "Failed to save csv file"

def test_create_vault(shared_data):
  # Data for creating a new vault.
  new_data = {
    "username": "new",
    "password": "new",
    "default": 0,
    "device_os": "arista_eos",
    "comment": "string"
  }

  # Create a vault with the specified data and print the result if creation is successful.
  created_vault = api.vault.create_vault(new_data)
  assert isinstance(created_vault, Vault)
  shared_data.update(vars(created_vault))

def test_update_vault(shared_data):
  # Data for updating a vault (vault ID 1).
  update_data = {
    "username": "test",
    "password": "test",
    "default": 0,
    "device_os": "cisco_ios",
    "comment": "string"
  }
  # Update the specified vault and print the result if update is successful.
  updated_vault = api.vault.update_vault(shared_data['id'], update_data)
  assert isinstance(updated_vault, Vault)

def test_get_vault(shared_data):
  # Retrieve and display a specific vault by ID (ID 1 in this case).
  vault = api.vault.get_vault(shared_data['id'])
  assert isinstance(vault, Vault)

# def test_delete_vault(shared_data):
#   # Delete a vault (vault ID 1) and print its details if the deletion is successful.
#   deleted_vault = api.vault.delete_vault(shared_data['id'])
#   assert isinstance(deleted_vault, Vault)
