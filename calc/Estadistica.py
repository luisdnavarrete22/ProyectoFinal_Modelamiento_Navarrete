import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

class Estadistica:

    def __init__(self):
        self.df = pd.read_excel('info/data_living_index.xlsx')
    
    def datosExcel(self):

        return self.df

    def graficoTotalFacturadodecompraventa(self):
        img = io.BytesIO()

        metodo = self.df['País'].unique()
        totalf = []
        for i in metodo:
            suma = self.df.loc[self.df['País'] == i, ['Índice de Precios de Restaurantes']].sum()[0]
            totalf.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(metodo, totalf, color='green')
        plt.title('Índice de precios de restaurantes por país')
        plt.xticks(rotation=10)
        plt.ylabel('Valores')
        plt.xlabel('')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoFrecuenciadelCliente(self):

        img = io.BytesIO()

        cliente = self.df['Índice de Costo de Vida']
        plt.figure(figsize=(10,5))
        plt.hist(cliente, bins=None, color='blue')
        plt.title('Índice de costo de vida')
        plt.xticks(rotation=10)
        plt.ylabel('Valores')
        plt.xlabel('Frecuencia')

        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
        
    def graficodeprecioporproveedor(self):

        img = io.BytesIO()

        proveedor = self.df['Índice de Alquiler'].unique()
        precio = []
        for i in proveedor:
            suma = self.df.loc[self.df['Índice de Costo de Vida'] == i, ['Índice de Alquiler']].sum()[0]
            precio.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(proveedor, precio, color = 'red')
        plt.title('Índice de alquiler')
        plt.xticks(rotation=10)
        plt.ylabel('Rangos (valores)')
        plt.xlabel('Frecuencia')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoFrecuenciadelproducto(self):

        img = io.BytesIO()

        x = self.df['Índice de poder adquisitivo local']
        plt.figure(figsize=(10,5))
        plt.hist(x, bins=None, color='aqua')
        plt.title('Índice de poder adquisitivo local')
        plt.xticks(rotation=10)
        plt.ylabel('Valores')
        plt.xlabel('Frecuencia')

        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
