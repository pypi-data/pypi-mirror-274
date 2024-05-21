import slurpit  # Import the slurpit library, which is assumed to contain API client functionalities.
import time
import pytest
from slurpit.models.scanner import Node
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)

def test_get_nodes():    
    # Fetch a list of nodes for a specified batch ID, in this case, batch_id is 1.
    nodes = api.scanner.get_nodes(1)
    assert isinstance(nodes, dict)

def test_save_csv():    
    # Fetch a list of nodes for a specified batch ID, and save it to csv file.
    nodes_csvdata = api.scanner.get_nodes(1, export_csv=True)
    result = api.scanner.save_csv_bytes(nodes_csvdata, "csv/scanner.csv")
    assert result == True, "Failed to save csv file"

def test_get_finders():    
    # Fetch a list of all configured finders in the scanning system.
    finders_data = api.scanner.get_finders()
    assert isinstance(finders_data, list)

def test_get_crawlers():    
    # Fetch a list of all configured crawlers in the scanning system.
    crawlers_data = api.scanner.get_crawlers()
    assert isinstance(crawlers_data, list)

def test_scanner_run():    
    scanner_data = {
        "target": "192.168.70.0/24",
        "version": "snmpv2c",
        "batch_id": 68,
        "snmpv2c_key": "public"
    }
    result = api.scanner.start_scanner(scanner_data)
    assert isinstance(result, dict)
    assert result['active'] == True

def test_clean_logging():
    cleaned_result = api.scanner.clean_logging("2023-12-31 23:00")
    assert isinstance(cleaned_result, dict)

def test_get_status():
    status = api.scanner.get_status()
    assert isinstance(status, dict)
    assert status['active'] == True

# Prepare data for an SNMP test on a specific IP address.
def test_scanner_snmp():    
    test_ip = {
        "ip": "192.168.1.2",
        "version": "snmpv2c",
        "snmpv2c_key": "test",
        "snmpv3_username": "test", 
        "snmpv3_authkey": "test",
        "snmpv3_authtype": [
            "none", "md5", "sha", "sha224", "sha256", "sha384", "sha512"
        ],
        "snmpv3_privkey": "string",
        "snmpv3_privtype": [
            "none", "des", "3des", "aes128", "aes192", "aes256", "aesblumenthal192", "aesblumenthal256"
        ]
    }
    test_result = api.scanner.test_snmp(test_ip)  # Conduct an SNMP test with the provided data.
    assert isinstance(test_result, dict)


def test_queue_list():    
    # Gives a list of currently queued tasks
    queue_list = api.scanner.get_queue_list()
    assert isinstance(queue_list, list)

def test_clear_queue():    
    # Clears all queued tasks
    clear_result = api.scanner.clear_queue()
    assert isinstance(clear_result, dict)

