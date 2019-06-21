# Meraki_Devices_Statuses_Counter
Python script that interacts with Cisco Meraki's dashboard(via API) and counts the quantity of online and offline devices in each organization.

This script will generate two .txt files, the first containing all the organizations names as columns and the quantity of online devices for each org as a row. The second .txt is for the offline devices. The last column 'tempo' in both of the .txts contains the date and time in UTC which the script has been ran.

Requirements:
- Python2 or 3 installed
- Meraki module installed (can be installed via PIP)
