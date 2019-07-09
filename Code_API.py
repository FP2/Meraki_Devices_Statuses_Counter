from meraki import meraki
import csv
from datetime import datetime
from collections import OrderedDict
import logging
import requests

logging.basicConfig(filename='Devices_Counter.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

org_ids = []  # all org_ids
org_names = []  # all org names
online_counter_lst = []  # all orgs online devices
offline_counter_lst = []  # all orgs offline devices

try:
    # API Key.
    KEY = <API KEY>
    try:
        # getting all organizations
        orgs = meraki.myorgaccess(KEY)
        # creating 2 lists containing the ids and names of all org
        for org in orgs:
            org_ids.append(org.get('id'))
            org_names.append(org.get('name'))
    except meraki.OrgPermissionError:
        error_text = 'No permission to access organization.'
        logging.error('{}'.format(error_text))
        print('{}'.format(error_text))

    # Creating list of tuples
    org_names_ids = sorted(list(zip(org_names, org_ids)))
    # Excluding unnecessary org for this project
    org_names_ids.__delitem__(4)
    org_names_sorted = sorted(org_names)
    org_names_sorted.__delitem__(4)
   
    # Getting all devices statuses
    for i in org_names_ids:
        status = meraki.get_device_statuses(KEY, i[1])
        print("Scanning {} - {}".format(i[0], i[1]))
        online_counter = 0
        offline_counter = 0
        # Counting online and offline devices for each org
        for item in status:
            if item.get('status') == 'online':
                online_counter += 1
            elif item.get('status') == 'offline':
                offline_counter += 1
        logging.info('Scanned {} successfully'.format(i[0]))
        online_counter_lst.append(online_counter)
        offline_counter_lst.append(offline_counter)

    logging.info('All orgs scanned successfully')

    # Creating Dicts with results
    org_device_online = {name: status for name, status in zip(org_names_sorted, online_counter_lst)}
    org_device_online_sorted = OrderedDict(sorted(org_device_online.items(), key=lambda t: t[0]))
    org_device_offline = {name: status for name, status in zip(org_names_sorted, offline_counter_lst)}
    org_device_offline_sorted = OrderedDict(sorted(org_device_offline.items(), key=lambda t: t[0]))

    # Setting up date and time
    date_raw = str(datetime.utcnow())
    date_no_milli = date_raw[:20]
    date_T = date_no_milli.replace(" ", "T")
    date_T_Z = date_T.replace(".", "Z")

    # Showing results to user
    print("\n")
    print("Online Devices:")
    print(org_device_online_sorted)
    print("\n")
    print("Offline Devices:")
    print(org_device_offline_sorted)

    # Adding last column 'tempo' with the date and time in UTC
    org_device_online_sorted['tempo'] = date_T_Z
    org_device_offline_sorted['tempo'] = date_T_Z

    # Creating .txt for the online devices (keys = columns, values = rows)
    with open('Online Devices.txt', mode='w') as online_devices_file:
        writer = csv.DictWriter(online_devices_file, fieldnames=org_device_online_sorted.keys())
        writer.writeheader()
        writer.writerow(org_device_online_sorted)

    logging.info('Online Devices.txt created successfully')

    # Creating .txt for the offline devices (keys = columns, values = rows)
    with open('Offline Devices.txt', mode='w') as offline_devices_file:
        writer = csv.DictWriter(offline_devices_file, fieldnames=org_device_offline_sorted.keys())
        writer.writeheader()
        writer.writerow(org_device_offline_sorted)

    logging.info('Offline Devices.txt created successfully')

except requests.exceptions.ConnectionError:
    co_error = "Connection error raised."
    logging.error('{}'.format(co_error))
    print('{}'.format(co_error))

except TimeoutError:
    to_error = "Connection timeout error raised."
    logging.error('{}'.format(to_error))
    print('{}'.format(to_error))

except ConnectionError:
    con_error = '"Connection error raised."'
    logging.error('{}'.format(con_error))
    print('{}'.format(con_error))

except Exception as unknown:
    logging.error('{}'.format(unknown))
    tipo = (type(unknown))
    logging.error('{}'.format(tipo))
    print('{}'.format(unknown))
