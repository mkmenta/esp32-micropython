from wifi_config import WIFI_NETWORKS
from connect_wifi import connect_wifi
from simple_web_server import SimpleWebServer, extract_json_from_request
import machine
import json

# Connect to WiFi using the provided networks
IFCONFIG = connect_wifi(WIFI_NETWORKS)

# Start the REST API
sws = SimpleWebServer(IFCONFIG[0])

integrated_led = machine.Pin(2, machine.Pin.OUT)
# Initialize the LED state
integrated_led.value(0)
IS_ACTIVE = False

def toggle_onoff(query, request):
    if not query:
        query = extract_json_from_request(request)
    if 'state' in query and query['state'] == 'on':
        integrated_led.value(1)
        global IS_ACTIVE
        IS_ACTIVE = True
        return json.dumps({"is_active": IS_ACTIVE})
    if 'state' in query and query['state'] == 'off':
        integrated_led.off()
        global IS_ACTIVE
        IS_ACTIVE = False
        return json.dumps({"is_active": IS_ACTIVE})
    raise Exception

def turn_on(query, request):
    return toggle_onoff({'state': 'on'}, request)

def turn_off(query, request):
    return toggle_onoff({'state': 'off'}, request)

def active_status(query, request):
    """Example handler to get the light status."""
    return json.dumps({"is_active": IS_ACTIVE})

sws.add_handler('POST', '/toggle_onoff', toggle_onoff, content_type='application/json')
sws.add_handler('GET', '/toggle_onoff', active_status, content_type='application/json')
sws.add_handler('GET', '/turn_on', turn_on, content_type='application/json')
sws.add_handler('GET', '/turn_off', turn_off, content_type='application/json')

# Start the web server
# sws.start()