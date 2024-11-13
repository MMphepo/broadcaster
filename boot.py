from bluetooth import BLE
import bluetooth
import struct
from micropython import const
import time

# BLE IRQ Event Constants
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

# Simple counter for debugging
connection_count = 0

def bt_irq(event, data):
    global connection_count
    print('Event:', event)  # Print the event type for debugging
    
    if event == _IRQ_CENTRAL_CONNECT:
        conn_handle, addr_type, addr = data
        connection_count += 1
        print('New connection:', conn_handle)
        print(f'Total connections: {connection_count}')
        
    elif event == _IRQ_CENTRAL_DISCONNECT:
        conn_handle, addr_type, addr = data
        connection_count -= 1
        print('Disconnected:', conn_handle)
        print(f'Total connections: {connection_count}')
        # Restart advertising after disconnect
        start_advertising()

def start_advertising():
    print('Starting BLE advertising...')
    
    # Create advertising payload
    payload = bytearray()
    
    # Add device name
    name = '7794dda5-80ef-462e-81de-ba6915e56100'
    payload.extend(struct.pack('BB', len(name) + 1, 0x09))
    payload.extend(name.encode())
    
    # Start advertising
    ble.gap_advertise(100000, adv_data=payload)
    print('Advertising started. Device name:', name)

# Initialize BLE
print('Initializing BLE...')
ble = BLE()
ble.active(True)
ble.irq(bt_irq)

# Start advertising
start_advertising()

print('BLE setup complete. Press Ctrl+C to stop.')
print('Device should now be visible to BLE scanners...')

try:
    while True:
        time.sleep(0.5)  # Short sleep to prevent busy waiting
        print('.', end='')  # Visual indicator that program is running
        
except KeyboardInterrupt:
    print('\nStopping BLE...')
    ble.active(False)
    print('BLE stopped.')

