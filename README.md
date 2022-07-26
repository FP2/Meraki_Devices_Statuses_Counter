# Meraki_Devices_Statuses_Counter
A simple Python script developed to run in a Debian based server that will fetch data from Cisco Meraki's API and count the quantity of online and offline devices in each organization.

This script will create two csv files, the first containing all the organizations names as columns and the quantity of online devices for each org as a row. The second csv is for the offline devices. The last column 'tempo' in both of the files contains the date and time in UTC.

