import requests
import csv
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Set the Zabbix API URL
ZABBIX_API_URL = config['zabbix']['url']

# Set the Zabbix API token
ZABBIX_API_TOKEN = config['zabbix']['token']

# Create a Zabbix API session
zabbix_api_session = requests.Session()
zabbix_api_session.headers = {"Authorization": "Bearer {}".format(ZABBIX_API_TOKEN)}

# Get all hosts from the Zabbix API
zabbix_api_request = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "selectTags": "extend",
        "evaltype": 0,
        "tags": [
            {
                "tag": "Fake",
                "operator": 5
            }
        ]
    },
    "id": 1
}
zabbix_api_response = zabbix_api_session.post(ZABBIX_API_URL, json=zabbix_api_request)

# Check the Zabbix API response status code
if zabbix_api_response.status_code != 200:
    raise Exception("Failed to get all hosts from the Zabbix API: {}".format(zabbix_api_response.content))

# Get the host data from the Zabbix API response
zabbix_host_data = zabbix_api_response.json()["result"]

# Create a CSV file to write the Zabbix host data to
with open("zabbix_host_data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the CSV header row
    csv_writer.writerow(["hostid", "host_name","description","disabled"])

    # Write the Zabbix host data to the CSV file
    for zabbix_host in zabbix_host_data:
        csv_writer.writerow([
            zabbix_host["hostid"],
            zabbix_host["host"],
            zabbix_host["description"] if zabbix_host.get("description") else " ",
            zabbix_host["status"] if zabbix_host.get("status") else "1",
        ])

# Close the CSV file
csv_file.close()

# Get all interfaces from the Zabbix API
zabbix_api_request = {
    "jsonrpc": "2.0",
    "method": "hostinterface.get",
    "params": {
        "output": "extend"
    },
    "id": 1
}
zabbix_api_response = zabbix_api_session.post(ZABBIX_API_URL, json=zabbix_api_request)

# Check the Zabbix API response status code
if zabbix_api_response.status_code != 200:
    raise Exception("Failed to get all hosts from the Zabbix API: {}".format(zabbix_api_response.content))

# Get the host data from the Zabbix API response
zabbix_int_data = zabbix_api_response.json()["result"]

# Create a CSV file to write the Zabbix host data to
with open("zabbix_int_data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the CSV header row
    csv_writer.writerow(["hostid", "interface_type","interface_ip_address","interface_dns","interface_use_ip","interface_port","interface_default"])

    # Write the Zabbix host data to the CSV file
    for zabbix_int in zabbix_int_data:
        csv_writer.writerow([
            zabbix_int["hostid"],
            zabbix_int["type"] if zabbix_int.get("type") else "1",
            zabbix_int["ip"] if zabbix_int.get("ip") else "127.0.0.1",
            zabbix_int["dns"] if zabbix_int.get("dns") else "example.tld",
            zabbix_int["useip"] if zabbix_int.get("useip") else "1",
            zabbix_int["port"] if zabbix_int.get("port") else "10050",
            zabbix_int["main"] if zabbix_int.get("main") else "1",
        ])

# Close the CSV file
csv_file.close()
###
import csv
import os

# Define the input CSV files and output file
file1 = "zabbix_host_data.csv"
file2 = "zabbix_int_data.csv"
output_file = "merged_output.csv"

# Define the key field (the common field to merge on)
key_field = "hostid"  # Change this to the appropriate field name

# Create dictionaries to store the data from both files
data1 = {}
data2 = {}

# Read data from the first CSV file
with open(file1, 'r', newline='') as csv_file1:
    reader = csv.DictReader(csv_file1)
    for row in reader:
        key = row[key_field]
        data1[key] = row

# Read data from the second CSV file
with open(file2, 'r', newline='') as csv_file2:
    reader = csv.DictReader(csv_file2)
    for row in reader:
        key = row[key_field]
        data2[key] = row

# Merge the data based on the key field
merged_data = []
for key, row1 in data1.items():
    if key in data2:
        row2 = data2[key]
        merged_row = {**row1, **row2}
        merged_data.append(merged_row)

# Write the merged data to the output file
with open(output_file, 'w', newline='') as output_csv:
    fieldnames = merged_data[0].keys()  # Assuming all rows have the same keys
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

# Delete the input files
os.remove(file1)
os.remove(file2)

print(f"Merged data written to {output_file}")
print(f"Input files {file1} and {file2} deleted.")



