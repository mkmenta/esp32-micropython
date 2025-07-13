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

def toggle_light(query, request):
    """Example handler to toggle a light."""
    if not query:
        query = extract_json_from_request(request)
    if 'state' in query and query['state'] == 'on':
        integrated_led.value(1)  # Turn on the integrated LED
        return json.dumps({"is_active":True})
    if 'state' in query and query['state'] == 'off':
        integrated_led.off()
        return json.dumps({"is_active":False})
    raise Exception

def turn_on_light(query, request):
    """Example handler to turn on a light."""
    return toggle_light({'state': 'on'}, request)

def turn_off_light(query, request):
    """Example handler to turn off a light."""
    return toggle_light({'state': 'off'}, request)

def full_request_handler(query, request):
    """Example handler that returns the full request as html."""
    return f"<h1>Full Request</h1><pre>{request}</pre>"

def light_status(query, request):
    """Example handler to get the light status."""
    return json.dumps({"is_active": integrated_led.value() == 1})

sws.add_handler('POST', '/toggle_light', toggle_light, content_type='application/json')
sws.add_handler('GET', '/toggle_light', light_status, content_type='application/json')
sws.add_handler('GET', '/turn_on_light', turn_on_light, content_type='application/json')
sws.add_handler('GET', '/turn_off_light', turn_off_light, content_type='application/json')
sws.add_handler('GET', '/full_request', full_request_handler, content_type='text/html')
sws.add_handler('POST', '/full_request', full_request_handler, content_type='text/html')
sws.add_handler('PUT', '/full_request', full_request_handler, content_type='text/html')
sws.add_handler('DELETE', '/full_request', full_request_handler, content_type='text/html')

# Start the web server
# sws.start()