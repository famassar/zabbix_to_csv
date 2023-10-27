# zabbix_to_csv

This simple script extracts hosts from Zabbix and create a csv file.

To use it:
1) Insert in Zabbix a tag "Fake" (as written !) in the hosts you dont' wanto to export;
2) Edit hte config.ini file with your Zabbix APi URl and the API token;

You can find the output file in the same directory af the script, named "merged_output.csv"
