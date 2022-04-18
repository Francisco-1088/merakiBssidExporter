import meraki
import pandas as pd
import config

api_key = config.api_key

# Create Dashboard API Client
dashboard = meraki.DashboardAPI(api_key)

# Fetch organizations API Key has access to
orgs = dashboard.organizations.getOrganizations()

# Display menu
for i in range(len(orgs)):
    print(f"{i} - {orgs[i]['name']}")

# Find org ID
selection = int(input("Enter the number corresponding to the Organization you want to obtain BSSID information for: "))
org_id = orgs[selection]["id"]

# Get all MR APs in the org
aps = dashboard.organizations.getOrganizationDevices(org_id, productTypes=['wireless'])
# Get all Networks in the org
nets = dashboard.organizations.getOrganizationNetworks(org_id)

# Build BSSID List
emergency_locations = []
for ap in aps:
  bssids = dashboard.wireless.getDeviceWirelessStatus(ap['serial'])
  for bssid in bssids['basicServiceSets']:
    if 'Unconfigured' not in bssid["ssidName"]:
      location = {
          "bssid":bssid["bssid"],
          "ssid_name":bssid["ssidName"],
          "ssid_band":bssid["band"],
          "ssid_number":bssid["ssidNumber"],
          "ap_name":ap['name'],
          "ap_serial":ap['serial'],
          "ap_mac":ap['mac'],
          "ap_ip":ap["lanIp"],
          "ap_net_id": ap['networkId'],
          "ap_model": ap['model'],
          "ap_address": ap["address"],
          "ap_latitude": ap["lat"],
          "ap_longitude": ap["lng"],
          "ap_model": ap["model"],
          "ap_url": ap["url"]
      }
      emergency_locations.append(location)

# Add Network Name
for net in nets:
    for location in emergency_locations:
        if net['id'] == location['ap_net_id']:
            location['ap_net_name'] = net['name']

# Export to CSV file
bssid_df = pd.DataFrame(emergency_locations)
bssid_df.to_csv('./bssids.csv')