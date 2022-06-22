import logging
import serial
import serial.tools.list_ports
#import prometheus_client

VENDOR_ID = '0403'
PRODUCT_ID = '6001'

keys_and_units = {
        "ISOUSC": ("amperes","Intensité souscrite (A)"),
        "BASE": ("watt_hours","Index option Base (Wh)"),
        "HCHC": ("watt_hours","Index option Heures Creuses (Wh) Heures Creuses"),
        "HCHP": ("watt_hours","Index option Heures Creuses (Wh) Heures Pleines"),
        "EJPHN": ("watt_hours","Index option EJP (Wh) Heures Normales"),
        "EJPHPM": ("watt_hours","Index option EJP (Wh) Heures de Pointe Mobile"),
        "BBRHCJB": ("watt_hours","Index option Tempo (Wh) Heures Creuses Jours Bleus"),
        "BBRHPJB": ("watt_hours","Index option Tempo (Wh) Heures Pleines Jours Bleus"),
        "BBRHCJW": ("watt_hours","Index option Tempo (Wh) Heures Creuses Jours Blancs"),
        "BBRHPJW": ("watt_hours","Index option Tempo (Wh) Heures Pleines Jours Blancs"),
        "BBRHCJR": ("watt_hours","Index option Tempo (Wh) Heures Creuses Jours Rouges"),
        "BBRHPJR": ("watt_hours","Index option Tempo (Wh) Heures Pleines Jours Rouges"),
        "IINST": ("amperes","Intensité Instantanée (A)"),
        "ADPS": ("amperes","Avertissement de Dépassement de Puissance Souscrite (A)"),
        "IMAX": ("amperes","Intensité maximale (A)"),
        "PAPP": ("volt_amperes", "Puissance apparente (VA)")
## currently not managed
# "ADCO" 12 caractères Adresse d’identification du compteur
# "OPTARIF" 4 car. Option tarifaire choisie
# "PEJP " 2 car. 30mn avant période EJP
# "PTEC " 4 car. Période Tarifaire en cours
# DEMAIN Couleur du lendemain
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

