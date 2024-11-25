import asyncio
from umqtt.simple import MQTTClient
import config
import data
from data import mqtt_subs
from time import sleep

'''
mqtt_subs = [
    {'feed':'infrapale/feeds/villaastrid.ruuvi-e6', 'label':'MH1','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-ea', 'label':'K','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-ed', 'label':'Parvi','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-f2', 'label':'KHH','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/lillaastrid.studio-temp', 'label':'Studio','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.astrid-mode', 'label':'VA Mode','value': 0.0, 'updated': False},
    {'feed': 'infrapale/feeds/demofeed',               'label':'Set Temp','value': 0.0, 'updated': False}, 
    ]
'''



def subscribe(client, topic):
    client.subscribe(topic)
    print('Subscribe to topic:', topic)
    
# Callback function that runs when you receive a message on subscribed topic
def my_callback(topic, message):
    # Perform desired actions based on the subscribed topic and response
    print('Received message on topic:', topic)
    print('Response:', message)
    topic_str = topic.decode()
    msg_str = message.decode()
    for subs in mqtt_subs:
        if subs['feed'] == topic_str:
            print("Feed: ",topic_str, " = ", msg_str)
            subs['value'] = float(msg_str)
            subs['updated'] = True
            print(subs)
            break
    
    
 

async def mqtt_task():
    mqtt_state = 0
    MQTT_SERVER = config.mqtt_broker_address
    MQTT_PORT = 8883
    MQTT_USER = config.mqtt_broker_username
    MQTT_PASSWORD = config.mqtt_broker_password
    MQTT_CLIENT_ID = b'raspberrypi_picow'
    MQTT_KEEPALIVE = 7200
    MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
    MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}
        
    print(mqtt_subs)
    
    
    while True:
        if mqtt_state == 0:
            print('MQTT state: ',mqtt_state, data.wifi_is_ready)
            if data.wifi_is_ready:
                mqtt_state = 10
            await asyncio.sleep_ms(1000)
        elif mqtt_state == 10:
            print('MQTT state: ',mqtt_state)
            try:
                client = MQTTClient(client_id=MQTT_CLIENT_ID,
                                    server=MQTT_SERVER,
                                    port=MQTT_PORT,
                                    user=MQTT_USER,
                                    password=MQTT_PASSWORD,
                                    keepalive=MQTT_KEEPALIVE,
                                    ssl=MQTT_SSL)
                client.connect()
                mqtt_state = 20
            except Exception as e:
                print('Error connecting to MQTT:', e)
                mqtt_state = 100
            await asyncio.sleep_ms(1000)

        elif mqtt_state == 20:
            print('MQTT state: ',mqtt_state)

            try:
                client.set_callback(my_callback)
            except Exception as e:
                print('Error defining callback:', e)
                mqtt_state = 100
            else:
                mqtt_state = 30
            await asyncio.sleep_ms(1000)

        elif mqtt_state == 30:
            print('MQTT state: ',mqtt_state)
            try:
                for subs in mqtt_subs:
                    print (subs['label'])
                    subscribe(client, subs['feed'])
            except Exception as e:
                print('Error adding subscriptions:', e)
                mqtt_state = 100
            else:    
                mqtt_state = 40
                    
            await asyncio.sleep_ms(1000)
        elif mqtt_state == 40:
            print('MQTT state: ',mqtt_state)
            await asyncio.sleep_ms(5000)
            try:
                client.check_msg()
            except Exception as e:
                print('Error checking feeds:', e)
                mqtt_state = 100
    
            # mqtt_state = 50
        elif mqtt_state == 50:
            print('MQTT state: ',mqtt_state)
            mqtt_state = 100
            await asyncio.sleep_ms(1000)
            
        elif mqtt_state == 100:
            print('MQTT state: ',mqtt_state)
            mqtt_state = 0
            await asyncio.sleep_ms(1000)

