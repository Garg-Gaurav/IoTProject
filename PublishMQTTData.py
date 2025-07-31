import network
import time
import machine
from umqtt.simple import MQTTClient
import ubinascii
from machine import UART, Pin




WIFI_SSID = 'Xxxxxxxx-XXX'
WIFI_PASS = 'xxxxxxxxxxxxxxx'
MQTT_BROKER = 'io.adafruit.com'   
MQTT_PORT = 1883
MQTT_USER = 'GauravLNU'  
MQTT_KEY = 'aio_uVIg99fo9iG7BMQqMIvU7dgua8cz'        
MQTT_TOPIC = 'GauravLNU/feeds/timestamp'


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected:", wlan.ifconfig())


def connect_mqtt():
    client = MQTTClient("picow_pub", MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_KEY)
    client.connect()
    print("Connected to MQTT broker")
    return client


def publish_csv(client, filename):
    with open(filename) as f:
        for line in f:
            parts = line.strip().split(',')
            #f"{parts[0]},{parts[1]},{parts[2]}"
            payload = f"{1}"
            print("Publishing:", payload)
            client.publish(MQTT_TOPIC, payload)
            time.sleep(3)  


connect_wifi()
mqtt_client = connect_mqtt()
client=mqtt_client
uart = UART(0, baudrate=500000, tx=Pin(0), rx=Pin(1))

try:
    count = 0
    while True:
        if uart.any():
            data = uart.read()
            print('Received:', data)
            time.sleep(0.5)
        #message = f'Hello {0.23}'
            client.publish(MQTT_TOPIC, data)
            #print('Published:', message)
        #count += 1
            time.sleep(3)
except KeyboardInterrupt:
    client.disconnect()
    print('Disconnected')


mqtt_client.disconnect()

