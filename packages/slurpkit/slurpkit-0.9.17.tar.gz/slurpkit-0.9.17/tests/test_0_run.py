import slurpit
import pytest
import time

host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.
api = slurpit.api(host, api_key)  


@pytest.mark.order(1)
def test_scanner_run():    
    scanner_data = {
        "target": "192.168.70.0/24",
        "version": "snmpv2c",
        "batch_id": 68,
        "snmpv2c_key": "public"
    }
    result = api.scanner.start_scanner(scanner_data)
    assert result is not None, "Failed starting scanner"

    status = api.scanner.get_status()
    assert status is not None, "Failed getting scanner status"
    while status['active']:
        time.sleep(5)
        status = api.scanner.get_status()
        assert status is not None, "Failed getting scanner status"

@pytest.mark.order(2)
def test_scraper_run():  
    vaults = api.vault.get_vaults()
    for vault in vaults:
        api.vault.delete_vault(vault.id)
    vault_data = {
        "username": "root",
        "password": "Welcome01!",
        "default": 1,
        "device_os": "cisco_ios"
    }
    created_vault = api.vault.create_vault(vault_data)
    assert created_vault is not None, "Failed creating vault"

    devices = api.device.get_devices()
    assert devices is not None, "Failed getting devices"
    hostnames = [device.hostname for device in devices]

    plannings = api.planning.get_plannings()
    assert plannings is not None, "Failed getting plannings"

    for planning in plannings:
        scraper_info = {
            "hostnames": hostnames,
            "planning_id": planning.id
        }
        result = api.scraper.start_scraper(scraper_info)
        assert result is not None, "Failed starting scraper"

    status = api.scraper.get_status()
    assert status is not None, "Failed getting scraper status"
    while status['active']:
        time.sleep(5)
        status = api.scraper.get_status()
        assert status is not None, "Failed getting scraper status"



# def test_devices():    
#     devices = api.device.get_devices(offset=0, limit=1000, export_csv=True)
#     api.device.save_csv_bytes(byte_data=devices, filename="csv/devices.csv")