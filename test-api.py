import pynetbox
import urllib3

NETBOX_SERVER = "192.168.1.20"
NETBOX_API_KEY = "b26141e2f8e529817fa9644c4cf013ed56b02be7"

nb_conn = pynetbox.api(url=f"https://{NETBOX_SERVER}", token=NETBOX_API_KEY)
nb_conn.http_session.verify=False
urllib3.disable_warnings()

devices = nb_conn.dcim.devices.all()

for device in devices:
    print(f"DEVICE NAME: {device.name:^10} DEVICE IP: {device.primary_ip4}")
