import slurpit
import pytest
from slurpit.models.user import User
## Setup config.
# Update the host and api key with your actual values to configure the API connection.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

## Create slurpit instance
# Initialize an API client instance with the specified host and API key.
api = slurpit.api(host, api_key)


@pytest.fixture(scope='module')
def shared_data():
  data = {} # Initialize an empty dictionary to store data
  yield data  # This will be passed to each test function that requests this fixture


## Get all users
def test_get_users():
  # Retrieve all users from the API and print them.
  users = api.users.get_users()
  assert all(isinstance(item, User) for item in users)

def test_get_users():
  # Retrieve all users from the API and save to csv file
  users_csvdata = api.users.get_users(export_csv=True)
  result = api.users.save_csv_bytes(users_csvdata, "csv/users.csv")
  assert result == True

def test_create_user(shared_data):
  # Define data for a new user.
  new_userdata = {
    "first_name": "test",
    "last_name": "test",
    "email": "john.doe@example.com",
    "password": "test$2#@#33",
    "language": "en",
    "dark_mode": 0
  }
  # Create a new user with the specified data and print the new user's details if creation is successful.
  new_user = api.users.create_user(new_userdata)
  shared_data.update(vars(new_user))
  assert isinstance(new_user, User)


def test_update_user(shared_data):
  # Define new data to update for the user with ID 1.
  update_data = {
    "first_name": "admin",
    "last_name": "super",
    "language": "en",
    "dark_mode": 1
  }
  # Update the user and print the updated user details if successful.
  updated_user = api.users.update_user(shared_data['id'], update_data)
  assert isinstance(updated_user, User)

def test_get_user(shared_data):
  # Fetch a specific user by their user ID (in this case, user ID 1) and display the user's details if found.
  user = api.users.get_user(shared_data['id'])
  assert isinstance(user, User)


def test_get_user(shared_data):
  # Attempt to delete a user by their user ID (in this case, user ID 2) and display the deleted user's details if deletion is successful.
  deleted_user = api.users.delete_user(shared_data['id'])
  assert isinstance(deleted_user, User)

