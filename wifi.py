import asyncio
import network
import data
import ntptime
import config

 

async def wifi_task():
   
    wifi_state = 0
    wifi_timeout = 0
    #wifi_ssid = config.wifi_ssid
    #wifi_pswd  = config.wifi_password
    data.wifi_is_ready = False

    while True:
        if wifi_state == 0:
            print('WiFi state: ',wifi_state)
            wifi_is_connected = False;
            wifi_state = 5
            await asyncio.sleep_ms(1000)
        elif wifi_state == 5:
            try:
                import config
                WIFI_SSID = config.wifi_ssid
                WIFI_PASSWORD = config.wifi_password
                # from secrets import WIFI_SSID, WIFI_PASSWORD
                wifi_state = 10
            except ImportError:
                print("Create secrets.py with your WiFi credentials to get time from NTP")
                wifi_state = 100
        elif wifi_state == 10:
            print('WiFi state: ',wifi_state)
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wifi_state = 20
            await asyncio.sleep_ms(1000)
        elif wifi_state == 20:
            print('WiFi state: ',wifi_state)
            # Connect to the network
            wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            wifi_timeout = 10;
            wifi_state = 30
            await asyncio.sleep_ms(1000)
        elif wifi_state == 30:
            print('WiFi state: ',wifi_state)
            if wlan.status() >= 3:
                wifi_state = 40
                data.wifi_is_ready = True
                print('Connection successful!')
                network_info = wlan.ifconfig()
                print('IP address:', network_info[0])
            elif wifi_timeout == 0:
                wifi_state = 100
            else:
                wifi_timeout = wifi_timeout -1
            await asyncio.sleep_ms(1000)
            
        elif wifi_state == 40:
            print('WiFi state: ',wifi_state)
            if wlan.status() < 3:
                wifi_state = 50
                
            try:
                ntptime.settime()
                print("Time set")
            except OSError:
                print('ntptime failed')

            await asyncio.sleep_ms(5000)

        elif wifi_state == 50:
            print('WiFi state: ',wifi_state)
            wifi_state = 100
            await asyncio.sleep_ms(1000)
            
        elif wifi_state == 100:
            print('WiFi state: ',wifi_state)
            data.wifi_is_ready = False
            wifi_state = 0
            await asyncio.sleep_ms(1000)


    '''
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    # Check if connection is successful
    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True
    '''