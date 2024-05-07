# This example finds and connects to a Calliope mini act as a peripheral running the
# UART service.
#
# See also the higher-level aioble library which takes
# care of all IRQ handling and connection management.
# https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble

import sys

sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

import random
import struct

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

_MY_CALLIOPE_MINI = b'\xe0\xfb\x7f\x3c\x7e\xf8'

def _decode_data(data):
    #return struct.unpack("<h", data)[0]
    return data.decode('utf-8')

async def find_calliope():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # See if it matches our name and the environmental sensing service.
            #print(result.device.addr)
            if result.device.addr == _MY_CALLIOPE_MINI: 
                return result.device
    return None

async def main():
    
    device = await find_calliope()
    
    if not device:
        print("Calliope mini not found")
        return
    
    try:
        print("Connecting to", device)
        connection = await device.connect()
        
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return
    
    async with connection:
        
        try:
            uart_service = await connection.service(_UART_SERVICE_UUID)
            uart_char = await uart_service.characteristic(_UART_RX_CHAR_UUID)
    
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

        await uart_char.subscribe(indicate=True)

        while True:
            data = await uart_char.indicated()
            temp_value = _decode_data(data)
            print(temp_value)
            
asyncio.run(main())        
