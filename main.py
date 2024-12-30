'''
####################################################################################
    GALACTIC AIO / INFRAPALE 2024
####################################################################################
    Read Adafruit IO feed and show values on the Pimoroni GalacticUnicorn LED Display
    Get time from NTP synchronization
####################################################################################
    https://github.com/infrapale/T2411_GalacticUnicorn_Subs_AIO
####################################################################################
Links:
  https://github.com/pimoroni/pimoroni-pico
  https://shop.pimoroni.com/products/space-unicorns?variant=40842033561683
  https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/galactic_unicorn
  https://github.com/pimoroni/pimoroni-pico/releases/download/v1.21.0/pimoroni-galactic_unicorn-v1.21.0-micropython.uf2
  https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/galactic_unicorn#imports-and-objects
  https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics

####################################################################################
####################################################################################
'''

import time
import math
import asyncio
import machine
import data
import wifi
import mqtt
import show


async def main():
    asyncio.create_task(show.check_btns())
    asyncio.create_task(show.create_text())
    asyncio.create_task(show.update_display_task())
    asyncio.create_task(wifi.wifi_task())
    asyncio.create_task(mqtt.mqtt_task())
    while (True):
        await asyncio.sleep_ms(10_000)

asyncio.run(main())    
    


