# Meraki_Devices_Statuses_Counter
A simple Python script developed to run in a Debian based server that will interact with Cisco Meraki's dashboard(via API) and count the quantity of online and offline devices in each organization.

This script will generate two csv files, the first containing all the organizations names as columns and the quantity of online devices for each org as a row. The second csv is for the offline devices. The last column 'tempo' in both of the txts contains the date and time in UTC which the script has been ran.

