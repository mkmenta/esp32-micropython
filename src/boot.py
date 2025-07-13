import webrepl
from wifi_config import WIFI_NETWORKS
from connect_wifi import connect_wifi

# Connect to WiFi using the provided networks
IFCONFIG = connect_wifi(WIFI_NETWORKS)

# Start the WebREPL server
webrepl.start()