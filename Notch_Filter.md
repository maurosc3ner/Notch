
# Filtro Notch

Script para el uso de un filtro tipo notch de un EEG (archivo '.edf')

## Resumen
En este script se realiza un proceso de filtrado (Con un filtro tipo Notch), para posteriormente crear un archivo '.edf' con los datos obtenidos tras realizar dicho proceso, utilizando la librería "pyedflib"

## Entradas
Utilizando argparse, se definen las siguientes entradas de usuario.

1) -i o --archivo: Nombre del archivo .edf que se desea cargar, es de tipo str

2) -fo o --f0: Frecuencia que se desea filtrar con el filtro notch, es de tipo float, ejemplo: -fo 60. Por defecto fo = 60 Hz.

3) -Q 0 --Q: Factor de calidad del filtro, es de tipo int, ejemplo: -Q 50. Por defecto Q = 50 Hz

4) -e o --edf: Nombre del archivo y dirección donde se desea guardar el nuevo archivo .edf, es de tipo str, ejemplo: -e desktop/prueba.edf


## Salidas
1) edf : Archivo .edf con la señal original filtrada.

## Código
En el script principal (notch.py), se importan las librerías necesarias para implementar este código, definiendo una clase (Notch_filter) con sus respectivos métodos.
El código se implementa creando un objeto y haciendo uso de sus métodos.


```python
from notch import Notch_filter
notch1 = Notch_filter()
arc,output = notch1.argparse()
signal , fs ,headers= notch1.read_edf(arc)
filtered_signal = notch1.filt(signal,fs)
notch1.write_edf(filtered_signal,headers,output)

#python notch.py -i sujeto_base.edf -is 1000 -fs 1001.5 -e prueba.edf
```

## Librerias utilizadas
[1] Pyedflib http://pyedflib.readthedocs.io/en/latest/

[2] Numpy http://www.numpy.org/

[3] Scipy http://www.scipy.org

[4] Argparse  https://docs.python.org/3/library/argparse.html
