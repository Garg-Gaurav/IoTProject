import paho.mqtt.client as mqtt
from marvelmind import MarvelmindHedge
import sqlite3


# MQTT broker settings
BROKER = "io.adafruit.com"  # Public broker for testing
PORT = 1883
TOPIC = "GauravLNU/feeds/timestamp"          # Replace with your topic
MQTT_USER = 'GauravLNU'  
MQTT_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'     



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker.")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload
    print(f"Received raw bytes: {payload}")
    processed_data = parse_data(payload)
    

def write_data_sqlite(data):
    conn = sqlite3.connect('marvelmind_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO position_data (timestamp, hedge_id, x, y, z)
        VALUES (?, ?, ?, ?, ?)
    ''', (int(data[5]), data[0], data[1], data[2], data[3]))
    conn.commit()



def parse_data(raw_data):
    hedge = MarvelmindHedge(tty=None, adr=None, debug=True)

    hedge.handle_binary_data(raw_data)

    if hedge.positionUpdated:
        write_data_sqlite(hedge.position())
        return hedge.print_position()

    if hedge.distancesUpdated:
        return hedge.print_distances()

    if hedge.rawImuUpdated:
        return hedge.print_raw_imu()

    if hedge.fusionImuUpdated:
        return hedge.print_imu_fusion()

    if (hedge.positionUpdated):
        return hedge.print_position()
                    
    if (hedge.distancesUpdated):
        return hedge.print_distances()
                    
    if (hedge.rawImuUpdated):
        return hedge.print_raw_imu()
                    
    if (hedge.fusionImuUpdated):
        return hedge.print_imu_fusion()
                    
    if (hedge.telemetryUpdated):
        return hedge.print_telemetry()
                    
    if (hedge.qualityUpdated):
        return hedge.print_quality()
                    
    if (hedge.waypointsUpdated):
        return hedge.print_waypoint()
                    
    if (hedge.userDataUpdated):
        return hedge.print_user_data()

client = mqtt.Client()

client.username_pw_set(MQTT_USER, MQTT_KEY)

client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER, PORT, keepalive=60)


client.loop_forever()
