import time
import math
import asyncio
import machine
import network
import ntptime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import data


# create galactic object and graphics surface for drawing
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# create the rtc object
rtc = machine.RTC()

# constants for controlling the background colour throughout the day
MIDDAY_HUE = 1.1
MIDNIGHT_HUE = 0.8
HUE_OFFSET = -0.1

MIDDAY_SATURATION = 1.0
MIDNIGHT_SATURATION = 1.0

MIDDAY_VALUE = 0.8
MIDNIGHT_VALUE = 0.3

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

# set up some pens to use later
WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)

show_str = ""


@micropython.native  # noqa: F821
def from_hsv(h, s, v):
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)


# function for drawing a gradient background
def gradient_background(start_hue, start_sat, start_val, end_hue, end_sat, end_val):
    half_width = width // 2
    for x in range(0, half_width):
        hue = ((end_hue - start_hue) * (x / half_width)) + start_hue
        sat = ((end_sat - start_sat) * (x / half_width)) + start_sat
        val = ((end_val - start_val) * (x / half_width)) + start_val
        colour = from_hsv(hue, sat, val)
        graphics.set_pen(graphics.create_pen(int(colour[0]), int(colour[1]), int(colour[2])))
        for y in range(0, height):
            graphics.pixel(x, y)
            graphics.pixel(width - x - 1, y)

    colour = from_hsv(end_hue, end_sat, end_val)
    graphics.set_pen(graphics.create_pen(int(colour[0]), int(colour[1]), int(colour[2])))
    for y in range(0, height):
        graphics.pixel(half_width, y)


# function for drawing outlined text
def outline_text(text, x, y):
    graphics.set_pen(BLACK)
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(WHITE)
    graphics.text(text, x, y, -1, 1)

# Check whether the RTC time has changed and if so redraw the display
def redraw_display_if_reqd():
    global show_str
    
    data.year, data.month, data.day, data.wd, data.hour, data.minute, data.second, _ = rtc.datetime()
    # print('second: ', data.second, data.last_second)
    if data.second != data.last_second:
        data.hour = (data.hour + data.utc_offset) % 24
        time_through_day = (((data.hour * 60) + data.minute) * 60) + data.second
        percent_through_day = time_through_day / 86400
        percent_to_midday = 1.0 - ((math.cos(percent_through_day * math.pi * 2) + 1) / 2)
        print(percent_to_midday)

        hue = ((MIDDAY_HUE - MIDNIGHT_HUE) * percent_to_midday) + MIDNIGHT_HUE
        sat = ((MIDDAY_SATURATION - MIDNIGHT_SATURATION) * percent_to_midday) + MIDNIGHT_SATURATION
        val = ((MIDDAY_VALUE - MIDNIGHT_VALUE) * percent_to_midday) + MIDNIGHT_VALUE

        gradient_background(hue, sat, val,
                            hue + HUE_OFFSET, sat, val)

        #clock = "{:02}:{:02}:{:02}".format(data.hour, data.minute, data.second)

        # calculate text position so that it is centred
        w = graphics.measure_text(show_str, 1)
        x = int(width / 2 - w / 2 + 1)
        y = 2

        outline_text(show_str, x, y)

        data.last_second = data.second


async def create_text():
    global show_str
    text_state=0
    feed_indx = 0
    
    while (True):
        if text_state == 0:
            show_str = "{:02}:{:02}:{:02}".format(data.hour, data.minute, data.second)
            text_state = 1
            await asyncio.sleep_ms(5000)
        elif text_state == 1:
            subs = data.mqtt_subs[feed_indx]
            if subs['updated']:
                show_str = "{0} {1}".format(subs['label'], subs['value'])
                print(show_str)
                await asyncio.sleep_ms(10000)
            else:
                await asyncio.sleep_ms(100)
            feed_indx = feed_indx + 1
            if feed_indx >= len(data.mqtt_subs):
                feed_indx = 0
            text_state = 0
    

async def update_display_task():


    # set the font
    graphics.set_font("bitmap8")
    gu.set_brightness(0.5)
    
    while(True):
        # print('Show: redraw', data.second, data.last_second)
            
        redraw_display_if_reqd()

        # update the display
        gu.update(graphics)
        # print('Show: wait')
        await asyncio.sleep_ms(1000)


async def check_btns():
    while(True):
        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            gu.adjust_brightness(+0.01)
            data.last_second = None

        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            gu.adjust_brightness(-0.01)
            data.last_second = None

        if gu.is_pressed(GalacticUnicorn.SWITCH_A):
            sync_time()
        await asyncio.sleep_ms(50)


    