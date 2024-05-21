import slurpit  # Import the slurpit library, which is assumed to contain API client functionalities.
from slurpit.models.device import Device, Vendor
from slurpit.models.vault import Vault
import pytest
import time
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)  


@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture

# Deleting cisco ios device after creating it
def test_sync_device(shared_data):
  sync_data = {
    "hostname": 'cisco_ios',
    "fqdn": "2",
    "port": 22,
    "device_os": "cisco_ios",
    "device_type": "IOSv",
    "disabled": 0
  }

  synced_device = api.device.sync_device(sync_data)
  assert isinstance(synced_device, Device)  

  deleted_device = api.device.delete_device(synced_device.id)
  assert isinstance(deleted_device, Device)

# Delete created vault
def test_delete_vaults():
  vaults = api.vault.get_vaults()
  assert all(isinstance(item, Vault) for item in vaults)

  for vault in vaults:
    time.sleep(5)
    deleted_vault = api.vault.delete_vault(vault.id)
    assert isinstance(deleted_vault, Vault)

