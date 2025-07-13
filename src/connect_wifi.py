import network
import machine
import time


def connect_wifi(wifi_networks=tuple(), ap_ssid='ESP32', ap_password=None, verbose=True):
    wlan = network.WLAN()  # Create station interface
    wlan.active(True)      # Activate the interface
    # If already connected, return
    if wlan.isconnected():
        if verbose:
            print("Already connected to WiFi")
            print('Network config:', wlan.ipconfig('addr4'))
        return wlan.ipconfig('addr4')
    if verbose:
        print("Scanning for known networks...")
    # Try each network in the list
    for ssid, password in wifi_networks:
        if verbose:
            print(f"Attempting to connect to {ssid}...")
        # Set to only try once (don't retry indefinitely)
        wlan.config(reconnects=0)
        # Attempt to connect
        wlan.connect(ssid, password)
        # Wait for connection with timeout
        max_wait = 10  # seconds
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > max_wait:
                if verbose:
                    print(f"Could not connect to {ssid}, trying next network...")
                break
            machine.idle()  # Save power while waiting
        # If connected, print details and exit loop
        if wlan.isconnected():
            if verbose:
                print(f"Successfully connected to {ssid}")
                print('Network config:', wlan.ipconfig('addr4'))
            return wlan.ipconfig('addr4')
    # If we get here, no connection was established
    # Start access point mode
    if verbose:
        print("Could not connect to any known WiFi network")
        print("Starting access point mode...")
    wlan.active(False)  # Deactivate station mode
    wlan = network.WLAN(network.AP_IF)  # Create access point interface
    wlan.active(True)  # Activate access point
    wlan.config(essid=ap_ssid)
    if ap_password:
        wlan.config(password=ap_password)
    if verbose:
        print(f"Access point '{ap_ssid}' started with password '{ap_password}'")
        print('Network config:', wlan.ifconfig())
    return None
