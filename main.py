import logging
import serial
import serial.tools.list_ports
#import prometheus_client

VENDOR_ID = '0403'
PRODUCT_ID = '6001'

keys_and_units = {
        "ISOUSC": "amperes",
        "BASE": "watt_hours",
        "HCHC": "watt_hours",
        "HCHP": "watt_hours",
        "EJP HN": "watt_hours",
        "EJP HPM": "watt_hours",
        "BBR HC JB": "watt_hours",
        "BBR HP JB": "watt_hours",
        "BBR HC JW": "watt_hours",
        "BBR HP JW": "watt_hours",
        "BBR HC JR": "watt_hours",
        "BBR HP JR": "watt_hours",
        "IINST": "amperes",
        "ADPS": "amperes",
        "IMAX": "amperes",
        "PAPP": "volt_amperes"
## currently not managed
# "ADCO" 12 caractères
# "OPTARIF" 4 car.
# "PEJP " 2 car. 30mn avant période EJP
# "PTEC " 4 car.
# DEMAIN
}

def initialize():
    device = next(serial.tools.list_ports.grep('%s:%s' % (VENDOR_ID, PRODUCT_ID))).device
    return serial.Serial(device, 
                         baudrate=1200, 
                         parity=serial.PARITY_EVEN, 
                         stopbits=serial.STOPBITS_ONE, 
                         bytesize=serial.SEVENBITS, 
                         timeout=1)

def get_metrics(serial_port):
    current_key = ''
    first_key = ''
    frame = {}
    serial_port.readline() #purge buffer to get a complete line next
    while current_key != first_key or not first_key:
        if not first_key:
            first_key = current_key
        line = serial_port.readline().strip().decode('utf-8').rsplit(' ', 2)
        current_key = line[0]
        logging.debug('got %s' % str(line))
        for key in keys_and_units:
            if key == line[0]:
                frame[current_key] = (int(line[1]), keys_and_units[current_key])
                logging.debug('added %s' % key)
                break
    return frame 

def main():
    serial_port = initialize()
    logging.info('initialized')
    values = get_metrics(serial_port)
    print(values)
    logging.info(values)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
