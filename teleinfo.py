import logging
import serial
import serial.tools.list_ports
import os
import threading

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

class Teleinfo:
    def __init__(self, vendorId=None, productId=None, devicePath=None):
        if not devicePath and vendorId and productId:
            devicePath = next(serial.tools.list_ports.grep('%s:%s' % (VENDOR_ID, PRODUCT_ID))).device
        if not devicePath:
            raise ValueError('Please define either DEVICE_PATH or VENDOR_ID and PRODUCT_ID')
        self._metrics = {}
        self.thread = threading.Thread(target=self.continuousUpdateState, args=(devicePath,))
        self.thread.start()


    def continuousUpdateState(self, devicePath):
        with serial.Serial(devicePath,
                           baudrate=9600, 
                           parity=serial.PARITY_ODD, 
                           stopbits=serial.STOPBITS_ONE, 
                           bytesize=serial.SEVENBITS, 
                           timeout=1) as device:
            device.readline() #purge buffer to get a complete line next
            while True:
                self.updateMetrics(device)

    def updateMetrics(self, device):
        line = device.readline().strip().decode('utf-8').rsplit('\t', 2)
        current_key = line[0]
        logging.debug('got %s' % str(line))
        if line[0] in keys_and_units:
            try:
                value = int(line[1])
            except ValueError:
                logging.error("could not convert value %s to number with key %s", (line[1],line[0]))
            else:
                self._metrics[current_key] = (value, *keys_and_units[current_key])
                logging.debug('updated %s' % current_key)

    @property
    def metrics(self):
        return self._metrics.copy()


if __name__ == "__main__":
    from time import sleep

    VENDOR_ID = os.getenv('VENDOR_ID')
    PRODUCT_ID = os.getenv('VENDRO_ID')
    DEVICE_PATH = os.getenv('DEVICE_PATH')

    logging.basicConfig(level=logging.DEBUG)
    Teleinfo(VENDOR_ID, PRODUCT_ID, DEVICE_PATH)
