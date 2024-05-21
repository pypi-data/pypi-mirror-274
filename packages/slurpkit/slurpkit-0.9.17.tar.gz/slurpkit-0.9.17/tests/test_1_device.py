import slurpit  # Import the slurpit library, which is assumed to contain API client functionalities.
import pytest
from slurpit.models.device import Device, Vendor
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)  

@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture

# Retrieve devices
def test_get_devices():
  devices = api.device.get_devices()
  assert all(isinstance(device, Device) for device in devices)

def test_save_csv():
  devices_csvdata = api.device.get_devices(export_csv=True)
  result = api.device.save_csv_bytes(devices_csvdata, "csv/devices.csv")
  assert result == True, "Failed to save csv file"

# Creating a new device with specified details.
def test_create_device(shared_data):
  new_data = {
    "hostname": "test_device1",
    "fqdn": "192.168.1.1",
    "port": 22,
    "device_os": "linux",
    "device_type": "linux_1004",
    "disabled": 0
  }
  new_device = api.device.create_device(new_data)
  shared_data.update(vars(new_device))
  assert isinstance(new_device, Device)

# Updating a device's details.
def test_update_device(shared_data):
  update_data = {
    "hostname": "test_device2",
    "fqdn": "192.168.1.1",
    "port": 22,
    "device_os": "linux",
    "device_type": "linux_1004",
    "disabled": 0
  }
  updated_device = api.device.update_device(shared_data['id'], update_data)
  shared_data.update(vars(updated_device))
  assert isinstance(updated_device, Device)

# Fetching a specific device by its ID.
def test_get_device(shared_data):
  device = api.device.get_device(shared_data['id'])
  assert isinstance(device, Device)

# Syncing device data.
def test_sync_device(shared_data):
  sync_data = {
    "hostname": 'cisco_ios',
    "fqdn": "cisco_ios",
    "port": 22,
    "device_os": "cisco_ios",
    "device_type": "IOSv",
    "disabled": 0
  }

  synced_device = api.device.sync_device(sync_data)
  assert isinstance(synced_device, Device)

# Deleting a device by its ID.
def test_delete_device(shared_data):
  deleted_device = api.device.delete_device(shared_data['id'])
  assert isinstance(deleted_device, Device)

# Retrieving all vendors.
def test_get_vendors():
  vendors = api.device.get_vendors()
  assert all(isinstance(item, Vendor) for item in vendors)
  

# Retrieving all device types.
def test_get_types():
  types = api.device.get_types()
  assert isinstance(types, list)
  

# Retrieving snapshots for a specific hostname.
def test_get_snapshots():
  snap_shots = api.device.get_snapshots()
  assert isinstance(snap_shots, dict)
  

# Retrieving a specific snapshot for a device.
def test_get_snapshots():
  snap_shot = api.device.get_snapshot(hostname="cisco_ios", planning_id=3)
  assert isinstance(snap_shot, dict)
  
# Testing SSH connectivity.
def test_test_ssh():
  ssh_data = {
    "username": "test",
    "password": "test",
    "ip": "cisco_ios_test",
    "port": 22,
    "device_os": "cisco_ios"
  }
  
  ssh_response = api.device.test_ssh(ssh_data)
  assert ssh_response == True
