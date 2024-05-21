import slurpit  # Import the slurpit library, which provides API interaction capabilities
import pytest
from slurpit.models.platform import Platform 
## Setup config.
# Update the host and api key with your actual values to configure the API connection.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

## Create slurpit instance
# Initialize an API client instance with the specified host and API key.
api = slurpit.api(host, api_key)  # Creates an instance of the API client configured with the host and API key

# Ping to platform
def test_ping():
    platform = api.platform.ping()
    assert platform is not None
    assert isinstance(platform, Platform)
    assert platform.status == 'up', "Expected 'up' status, got not"
