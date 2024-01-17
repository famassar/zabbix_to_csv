This simple script extracts hosts from Zabbix and create a csv file.

**Required**

requests, csv and configparser python3 modules

**Usage**
1) Insert in Zabbix a tag "Skip" (as written !) in the hosts you dont' wanto to export;
2) Edit hte config.ini file with your Zabbix APi URl and the API token;

You can find the two output files in the same directory af the script. "merged_output.csv" contains the host data, "zabbix_inventory_data.csv" contains the inventory data
