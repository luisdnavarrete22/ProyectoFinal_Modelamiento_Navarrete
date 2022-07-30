import matplotlib
from matplotlib import colors
matplotlib.use('Agg')
import random
import io
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

class Simulacion:

    def modeloInventario(self):
        D = 12000.00
        Co = 25.00
        Ch = 0.50
        P = 2.50
        Tespera = 5
        DiasAno = 250

        Q = round(sqrt(((2*Co*D)/Ch)),2)
        N = round(D / Q,2)
        R = round((D / DiasAno) * Tespera,2)
        T = round(DiasAno / N,2)
        CoT = N * Co
        ChT = round(Q / 2 * Ch,2)
        MOQ = round(CoT + ChT,2)
        CTT = round(P * D + MOQ,2)

        data = {'datos':
            {
                'Q':Q,
                'CoT':CoT,
                'ChT':ChT,
                'MOQ':MOQ,
                'CTT': CTT,
                'N': N,
                'R':R,
                'T':T
            }
        }
        
        indice = ['Q','Inversion_maxima','Inversion_minima','Inversion_total','Diferencia_Inversion_total']
        periodo = np.arange(1,19)
        Lista = self.generarLista(Q)
        Lista.sort()
        dfQ = pd.DataFrame(index=periodo, columns=indice).fillna(0)
        dfQ['Q'] = Lista
        for period in periodo:
            dfQ['Inversion_maxima'][period] = D * Co / dfQ['Q'][period]
            dfQ['Inversion_minima'][period] = dfQ['Q'][period] * Ch / 2
            dfQ['Inversion_total'][period] = dfQ['Inversion_maxima'][period] + dfQ['Inversion_minima'][period]
            dfQ['Diferencia_Inversion_total'][period] = dfQ['Inversion_total'][period] - MOQ
        data ['df'] = dfQ
        dfG = dfQ.loc[:,'Inversion_maxima':'Inversion_total']
        
        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.grid()
        plt.plot(dfG, color='brown')
        plt.legend(('Inversion_maxima','Inversion_minima','Inversion_total'), loc="center")
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()

        data['img_url'] = img_url

        return data
        
    def generarLista(self, Q):
        n=18
        Q_Lista = []
        i=1
        Qi = Q
        Q_Lista.append(Qi)
        for i in range(1,9):
            Qi = Qi - 60
            Q_Lista.append(Qi)
        
        Qi = Q
        for i in range(9, n):
            Qi = Qi + 60
            Q_Lista.append(Qi)
        
        return Q_Lista

    def banco(self):
        landa = 1.3333
        nu = 4.0 
        #La probabilidad de hallar el sistema ocupado o utilización del sistema:
        p=landa/nu
        #La probabilidad de que no haya unidades en el sistema este vacía u ocioso : 
        Po = 1.0 - (landa/nu)
        #Longitud esperada en cola, promedio de unidades en la línea de espera:
        Lq = landa*landa / (nu * (nu - landa))
        #/ (nu * (nu - landa))
        # Número esperado de clientes en el sistema(cola y servicio) : 
        L = landa /(nu - landa)
        #El tiempo promedio que una unidad pasa en el sistema:
        W = 1 / (nu - landa)
        #Tiempo de espera en cola:
        Wq = W - (1.0 / nu)
        #La probabilidad de que haya n unidades en el sistema: 
        n= 1
        Pn = (landa/nu)*n*Po

        i = 0
        # Landa y nu ya definidos
        # Atributos del DataFrame
        """
        ALL # ALEATORIO DE INVERSORES
        ASE # ALEATORIO DE SERVICIO
        TILL TIEMPO ENTRE LLEGADA
        TISE TIEMPO DE SERVICIO
        TIRLL TIEMPO REAL DE LLEGADA
        TIISE TIEMPO DE INICIO DE SERVICIO
        TIFSE TIEMPO FINAL DE SERVICIO
        TIESP TIEMPO DE ESPERA
        TIESA TIEMPO DE SALIDA
        numClientes NUMERO DE INVERSORES
        dfLE DATAFRAME DE LA LINEA DE ESPERA
        """
        numClientes=100
        i = 0
        indice = ['ALL','ASE','TILL','TISE','TIRLL','TIISE','TIFSE','TIESP','TIESA']

        Clientes = np.arange(numClientes)
        dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
        np.random.seed(100)
        for i in Clientes:
            if i == 0:
                dfLE['ALL'][i] = round(random.random(),2)
                dfLE['ASE'][i] = round(random.random(),2)
                dfLE['TILL'][i] = round(-1/landa*np.log(dfLE['ALL'][i]),2)
                dfLE['TISE'][i] = round(-1/nu*np.log(dfLE['ASE'][i]),2)
                dfLE['TIRLL'][i] = round(dfLE['TILL'][i],2)
                dfLE['TIISE'][i] = round(dfLE['TIRLL'][i],2)
                dfLE['TIFSE'][i] = round(dfLE['TIISE'][i] + dfLE['TISE'][i],2)
                dfLE['TIESA'][i] = round(dfLE['TIESP'][i] + dfLE['TISE'][i],2)
            else:
                dfLE['ALL'][i] = round(random.random(),2)
                dfLE['ASE'][i] = round(random.random(),2)
                dfLE['TILL'][i] = round(-1/landa*np.log(dfLE['ALL'][i]),2)
                dfLE['TISE'][i] = round(-1/nu*np.log(dfLE['ASE'][i]),2)
                dfLE['TIRLL'][i] = round(dfLE['TILL'][i] + dfLE['TIRLL'][i-1],2)
                dfLE['TIISE'][i] = round(max(dfLE['TIRLL'][i],dfLE['TIFSE'][i-1]),2) 
                dfLE['TIFSE'][i] = round(dfLE['TIISE'][i] + dfLE['TISE'][i],2)
                dfLE['TIESP'][i] = round(dfLE['TIISE'][i] - dfLE['TIRLL'][i],2)
                dfLE['TIESA'][i] = round(dfLE['TIESP'][i] + dfLE['TISE'][i],2)
        columnas = ["A_LLEGADA","A_SERVICIO","TIE_LLEGADA","TIE_SERVICIO",
            "TIE_EXACTO_LLEGADA","TIE_INI_SERVICIO","TIE_FIN_SERVICIO","TIE_ESPERA","TIE_SALIDA"]
        nuevas_columnas = pd.core.indexes.base.Index(columnas)
        dfLE.columns = nuevas_columnas
        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.grid()
        for i in columnas:
            plt.plot(dfLE.loc[:,i], color='brown')
        plt.legend(columnas, loc="upper left")
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()

        return {'img_url': img_url, 'df': dfLE}
        
s = Simulacion()