import slurpit  # Import the slurpit library, which is assumed to contain API client functionalities.
import pytest
# Configuration setup: update these values to your actual API connection settings.
host = "http://portal_test"  # Specify the API host address.
api_key = "1234567890abcdefghijklmnopqrstuvwxqz"  # Provide the API key.

# Initialize an API client instance with the configured host and API key.
api = slurpit.api(host, api_key)  

# Retrieve scraped data for a specific batch ID and print it.
def test_scraper():
    scraped_data = api.scraper.scrape(1)
    assert isinstance(scraped_data, dict)
    assert isinstance(scraped_data['data'], list) 

# Retrieve scraped data and save to csv file
def test_save_csv():
    scraped_csvdata = api.scraper.scrape(1, export_csv=True)
    result = api.scraper.save_csv_bytes(scraped_csvdata, "csv/scraper.csv")
    assert result == True, "Failed to save csv file"

# Retrieve scraped planning data for a specific planning ID and print it.
def test_scrape_planning():
    scraped_data = api.scraper.scrape_planning(4)
    assert isinstance(scraped_data, dict)
    assert isinstance(scraped_data['data'], list) 

# Retrieve IP addresses related to a specific planning ID and date, and print them.
def test_scrape_planning_ips():
    scraped_planning_ips = api.scraper.scrape_planning_ips(3,'2023-04-03')
    assert isinstance(scraped_planning_ips, list), "Failed to scrape ips"


# Retrieve IP addresses related to a specific planning ID and date, and print them.
def test_scrape_planning_ipams():
    scraped_planning_ipams = api.scraper.scrape_planning_ipam(3,'2023-04-03')
    assert isinstance(scraped_planning_ipams, list), "Failed to scrape ipams"

# Retrieve scraped planning data for a specific planning ID, hostname, and print it.
def test_scrape_planning_by_hostname():
    scraped_planning2 = api.scraper.scrape_planning_by_hostname(3, "cisco_ios", 0, 100)
    assert isinstance(scraped_planning2, dict)
    assert isinstance(scraped_planning2['data'], list) 

# Retrieve scraped data for a specific device hostname, and print it.
def test_scrape_device():
    scraped_data = api.scraper.scrape_device("cisco_ios", 0, 100)
    assert isinstance(scraped_data, dict)
    assert isinstance(scraped_data['data'], list) 

# Retrieve the latest scraped batches and print them.
def test_scrape_batches_latest():
    scraped_data = api.scraper.scrape_batches_latest()
    assert isinstance(scraped_data, dict)

# Retrieve scraped batches for a specific planning ID and hostname, and print them.
def test_scrape_batches():
    scraped_data = api.scraper.scrape_batches(3,'arista_eos')
    assert isinstance(scraped_data, dict)

# Start the scraper with provided information and print the result.
def test_start_scraper():
    scraper_info = {
        "hostnames": [
            "cisco_ios"
        ],
        "planning_id": 3
    }
    started_result = api.scraper.start_scraper(scraper_info)
    assert isinstance(started_result, dict)


# Clean logs based on the provided datetime and print the result.
def test_clean_logs():
    cleaned_result = api.scraper.clean_logs("2023-12-31 22:30")
    assert isinstance(cleaned_result, dict)

# Retrieve the status of the scraper and print it.
def test_get_status():
    scraper_status = api.scraper.get_status()
    assert isinstance(scraper_status, dict)

# Gives a list of currently queued tasks
def test_queue_list():
    queue_list = api.scraper.get_queue_list()
    assert isinstance(queue_list, list)

# Clears all queued tasks
def test_clear_queue():
    clear_result = api.scraper.clear_queue()
    assert isinstance(clear_result, dict)