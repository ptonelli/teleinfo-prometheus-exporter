import logging
import serial
import serial.tools.list_ports
#import prometheus_client

VENDOR_ID = '0403'
PRODUCT_ID = '6015'

keys_and_units = {
        "EAST": ("Wh","Energie active soutirée Totale, index 02 (Wh)"),
        "EASF01": ("Wh","Energie active soutirée Fournisseur, index 01 (Wh)"),
        "EASF02": ("Wh","Energie active soutirée Fournisseur, index 02 (Wh)"),
        "EASF03": ("Wh","Energie active soutirée Fournisseur, index 03 (Wh)"),
        "EASF04": ("Wh","Energie active soutirée Fournisseur, index 04 (Wh)"),
        "EASD01": ("Wh","Energie active soutirée Distributeur, index 01 (Wh)"),
        "EASD02": ("Wh","Energie active soutirée Distributeur, index 02 (Wh)"),
        "EASD03": ("Wh","Energie active soutirée Distributeur, index 03 (Wh)"),
        "EASD04": ("Wh","Energie active soutirée Distributeur, index 04 (Wh)"),
}

#stty -F /dev/ttyUSB0 9600 -parodd cs7 -cstopb
def initialize():
    device = next(serial.tools.list_ports.grep('%s:%s' % (VENDOR_ID, PRODUCT_ID))).device
    return serial.Serial(device, 
                         baudrate=9600, 
                         parity=serial.PARITY_ODD, 
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
        line = serial_port.readline().strip().decode('utf-8').rsplit('\t', 2)
        current_key = line[0]
        logging.debug('got %s' % str(line))
        for key in keys_and_units:
            if key == line[0]:
                frame[current_key] = (int(line[1]), *keys_and_units[current_key])
                logging.debug('added %s' % key)
                break
    return frame 


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    serial_port = initialize()
    logging.info('initialized')
    values = get_metrics(serial_port)
    logging.info(values)

