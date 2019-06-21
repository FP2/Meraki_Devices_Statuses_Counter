from meraki import meraki
import csv
from datetime import datetime

# API Key.
KEY = '<API KEY>'

org_ids = []  # all org_ids
org_names = []  # all org names
online_counter_lst = []  # all orgs online devices
offline_counter_lst = []  # all orgs offline devices

# getting all organizations
orgs = meraki.myorgaccess(KEY)

# creating 2 lists containing the ids and names of all orgs
for org in orgs:
    org_ids.append(org.get('id'))
    org_names.append(org.get('name'))

# Creating dictionary
org_names_ids = {names: ids for names, ids in zip(org_names, org_ids)}

# Excluding unnecessary org for this project
org_names_ids.pop('CNB - Camera')

#Getting all devices statuses
for name, org_id in org_names_ids.items():
    status = meraki.get_device_statuses(KEY, org_id)
    online_counter = 0
    offline_counter = 0

    # Counting the quantity of online and offline devices for each org
    for item in status:
        if item.get('status') == 'online':
            online_counter += 1
        elif item.get('status') == 'offline':
            offline_counter += 1
    online_counter_lst.append(online_counter)
    offline_counter_lst.append(offline_counter)

# Creating Dicts with results
org_device_online = {name: status for name, status in zip(org_names_ids.keys(), online_counter_lst)}
org_device_offline = {name: status for name, status in zip(org_names_ids.keys(), offline_counter_lst)}

# Setting up date and time
date_raw = str(datetime.utcnow())
date_no_milli = date_raw[:20]
date_T = date_no_milli.replace(" ", "T")
date_T_Z = date_T.replace(".", "Z")

# Showing results to user
print("Online Devices:")
print(org_device_online)
print("\n")
print("Offline Devices:")
print(org_device_offline)

# Adding last column 'tempo' with the date and time in UTC
org_device_online['tempo'] = date_T_Z
org_device_offline['tempo'] = date_T_Z

# Creating .txt for the online devices (keys = columns, values = rows)
with open('Online Devices.txt', mode='w') as online_devices_file:
    writer = csv.DictWriter(online_devices_file, fieldnames=org_device_online.keys())
    writer.writeheader()
    writer.writerow(org_device_online)

# Creating .txt for the offline devices (keys = columns, values = rows)
with open('Offline Devices.txt', mode='w') as offline_devices_file:
    writer = csv.DictWriter(offline_devices_file, fieldnames=org_device_offline.keys())
    writer.writeheader()
    writer.writerow(org_device_offline)
