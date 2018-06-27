import pyedflib
import numpy as np
from scipy import signal as sg
import argparse

class Notch_filter():
    Q = 0 
    f0 = 0 
    def __init__(self,f0=60,Q=50):
        self.f0=f0
        self.Q=Q

    def argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--archivo',help='Ingrese el nombre del archivo .edf a utilizar',type = str)
        parser.add_argument('-is','--in_sec',help='Segundo inicial del segmento',type = float)
        parser.add_argument('-fs','--fi_sec',help='Segundo final del segmento. Nota: in_sec debe ser menor que fi_sec',type = float)
        parser.add_argument('-fo','--fo',help='Frecuencia que se desea filtrar. Por defecto fo = 60',type = float)
        parser.add_argument('-Q','--Q',help='Factor de calidad del filtro. Por defecto Q = 50',type = int)
        parser.add_argument('-e','--edf',help='Nombre y dirección del archivo .edf de salida',type = str)
        parsedargs = parser.parse_args()
        arc = parsedargs.archivo
        ini_sec = parsedargs.in_sec
        final_sec = parsedargs.fi_sec
        output = parsedargs.edf
        if (parsedargs.fo != None):
            if (parsedargs.fo> 0):
                self.f0 = parsedargs.fo
        if (parsedargs.Q != None):
            if (parsedargs.Q>0):
                self.Q = parsedargs.Q
        return arc,ini_sec,final_sec,output

    def read_edf(self,nameEdf):
        '''
        Descripción: Se encarga de leer el archivo .edf
        Entradas: - nameEdf: nombre del archivo .edf
        Salidas: - in_signal: Matriz de Canales X Tiempo
                 - fs: Frecuencia de muestro
                 - headers: Etiquetas del archivo .edf 
        '''   
        edf = pyedflib.EdfReader(nameEdf) 
        headers = edf.getSignalHeaders() 
        nch  = edf.signals_in_file
        nsig = edf.getNSamples()[0]
        fs = edf.getSampleFrequency(0)
        in_signal = np.zeros((nch,nsig))
        for x in range(nch):
            in_signal[x,:] = edf.readSignal(x)
        edf._close()
        del edf
        return  in_signal,fs,headers
    
    def segmentation(self,in_signal,fs,ini_sec,final_sec):
        '''
        Descripción: Se encarga de segmentar los datos del EEG
        Entradas: - ini_sec: segundo inicial del segmento 
                  - final_sec: segundo final del segmento
                  - in_signal: Matriz de Canales X Tiempo
                  - fs: Frecuencia de muestro
        Salidas: - segment: Segmento (Matriz de CanalesXTiempo)
        ''' 
        n_ini = int(fs*ini_sec)
        n_final = int(fs*final_sec)
        n = n_final-n_ini
        segment = np.zeros([len(in_signal),n])
        for i in range (0,len(in_signal)):
            segment[i] = in_signal[i][n_ini:n_final]
        return segment

    def filt(self,in_signal,fs):
        '''
        Descripción: Se encarga de filtrar los datos del EEG
        Entradas: - in_signal: Matriz de Canales X Tiempo
                  - fs: Frecuencia de muestro
        Salidas: - out_signal: EEG filtrado (Matriz de CanalesXTiempo)
        ''' 
        w0 = self.f0/(fs/2)  
        num,den = sg.iirnotch(w0,self.Q)
        out_signal = np.zeros((len(in_signal),len(in_signal[0])))
        for i in range(0,len(in_signal)):
            out_signal[i]=sg.filtfilt(num,den,in_signal[i])
        return out_signal

    def write_edf(self,in_signal,headers,nameEdf):
        '''
        Descripción: Se encarga de escribir los datos del nuevo EEG
        Entradas: - headers: etiquetas del .edf 
                  - in_signal: Matriz de Canales X Tiempo
                  - nameEdf : Nombre con el que se desea guardar el nuevo .edf
        ''' 
        edf = pyedflib.EdfWriter(nameEdf,len(in_signal),file_type=pyedflib.FILETYPE_EDFPLUS)
        edf_info = []
        edf_signal = []
        for i in range (len(in_signal)):
            channel_info={'label':headers[i]['label'],'dimension':headers[i]['dimension'],'sample_rate':headers[i]['sample_rate'],'physical_max':headers[i]['physical_max'] , 'physical_min': headers[i]['physical_min'], 'digital_max': headers[i]['digital_max'], 'digital_min': headers[i]['digital_min'], 'transducer':headers[i]['transducer'] , 'prefilter':headers[i]['prefilter']+',notch '+str(self.f0)+'Hz'}
            edf_info.append(channel_info)
            edf_signal.append(in_signal[i])
        edf.setSignalHeaders(edf_info)
        edf.writeSamples(edf_signal)
        edf.close()
        del edf


if __name__ == '__main__':
    notch1 = Notch_filter()
    arc,ini_sec,final_sec,output = notch1.argparse()
    signal , fs ,headers= notch1.read_edf(arc)
    segment = notch1.segmentation(signal,fs,ini_sec,final_sec)
    filtered_segment = notch1.filt(segment,fs)
    notch1.write_edf(filtered_segment,headers,output)


 
