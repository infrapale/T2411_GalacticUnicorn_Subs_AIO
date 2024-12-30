# data module
from micropython import const
import time


wifi_is_ready = False
utc_offset = 2
year = 0
month =0
day = 0
wd = 0
hour = 0
minute = 0
second = 0
last_second = 0



mqtt_subs = [
    {'feed':'infrapale/feeds/villaastrid.ruuvi-e6', 'label':'MH1','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-ea', 'label':'K','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-ed', 'label':'Parv','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.ruuvi-f2', 'label':'KHH','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/lillaastrid.studio-temp', 'label':'LA2','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.astrid-mode', 'label':'Mode','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.dock-ldr1', 'label':'(Lux)','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.dock-temp-bmp180', 'label':'Dock1','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.dock-temp-dht22', 'label':'Dock2','value': 0.0, 'updated': False},
    {'feed':'infrapale/feeds/villaastrid.dock-temp-water', 'label':'Water','value': 0.0, 'updated': False},    
    {'feed':'infrapale/feeds/test.scd30-temperature', 'label':'Temp','value': 0.0, 'updated': False},    
    {'feed':'infrapale/feeds/test.scd30-humidity', 'label':'Hum','value': 0.0, 'updated': False},    
    {'feed':'infrapale/feeds/test.scd30-c02', 'label':'CO2','value': 0.0, 'updated': False},
    ]

    # {'feed': 'infrapale/feeds/demofeed',               'label':'Temp','value': 0.0, 'updated': False}, 
