'''
CORSO DI GEOPROCESSIGN IN QGIS PER GEOLOGI
salvataggio di una stringa ad un file di testo
'''

import os
#from esercitazione2 import destinazione
destinazione = r"C:\Users\ferregutie\Downloads"


text_file = open(os.path.join(destinazione, 'mio_file.txt'), 'r')
testo = text_file.read()
text_file.close()

print (testo)