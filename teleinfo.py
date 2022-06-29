import logging
import serial
import serial.tools.list_ports
#import prometheus_client

VENDOR_ID = '0403'
PRODUCT_ID = '6015'

keys_and_units = { #format EDF_NAME:  unit, comment
        "EAST": ("Wh","Energie active soutiree Totale"),
        "EASF01": ("Wh","Energie active soutiree Fournisseur index 01"),
        "EASF02": ("Wh","Energie active soutiree Fournisseur index 02"),
        "EASF03": ("Wh","Energie active soutiree Fournisseur index 03"),
        "EASF04": ("Wh","Energie active soutiree Fournisseur index 04"),
        "EASD01": ("Wh","Energie active soutiree Distributeur index 01"),
        "EASD02": ("Wh","Energie active soutiree Distributeur index 02"),
        "EASD03": ("Wh","Energie active soutiree Distributeur index 03"),
        "EASD04": ("Wh","Energie active soutiree Distributeur index 04"),
        "SINSTS": ("VA","Puissance apparente Instantanee soutiree"),
        "SINSTS1": ("VA","Puissance apparente Instantanee soutiree phase 1"),
        "SINSTS2": ("VA","Puissance apparente Instantanee soutiree phase 2"),
        "SINSTS3": ("VA","Puissance apparente Instantanee soutiree phase 3"),
}

#stty -F /dev/ttyUSB0 9600 -parodd cs7 -cstopb
def get_device():
    return next(serial.tools.list_ports.grep('%s:%s' % (VENDOR_ID, PRODUCT_ID))).device

def get_metrics():
    with serial.Serial(get_device(),
                         baudrate=9600, 
                         parity=serial.PARITY_ODD, 
                         stopbits=serial.STOPBITS_ONE, 
                         bytesize=serial.SEVENBITS, 
                         timeout=1) as serial_port:
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
    values = get_metrics()
    logging.info(values)

