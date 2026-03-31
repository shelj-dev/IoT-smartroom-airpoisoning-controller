import network
import time
import urequests
from machine import ADC

WIFI_SSID = "CSELABWIFI"
WIFI_PASSWORD = "274998csc"


SERVER_IP_URL = "http://192.168.25.23:8000/"

wifi_status = False


mq2 = ADC(28)


def connect_wifi():
    global wifi_status

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wifi_status = True
        print("WiFi connected:", wlan.ifconfig()[0])
        return

    print("Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 10
    while timeout > 0 and not wlan.isconnected():
        print("Waiting for connection...")
        time.sleep(1)
        timeout -= 1

    wifi_status = wlan.isconnected()

    if wifi_status:
        print("WiFi connected:", wlan.ifconfig()[0])
    else:
        print("WiFi failed")


def sensor_data():
    value = mq2.read_u16()
    voltage = value * 3.3 / 65535

    print("Raw:", value, "Voltage:", round(voltage, 2))

    return value


def send_data(data):

    payload = {
        "value": data
    }

    url = SERVER_IP_URL + "api/get-sensor/"

    r = None

    try:
        
        r = urequests.post(url, json=payload, timeout=5)
        print("Sending to:", url)

    except Exception as e:
        print("Send error:", e)

    finally:
        if r is not None:
            r.close()


def main():
    while True:

        connect_wifi()

        sensor = sensor_data()

        if wifi_status:
            send_data(sensor)

        time.sleep(1)


main()