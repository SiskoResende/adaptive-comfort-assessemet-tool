# separando o código por função, uma função faz só uma coisa

print('LibConfort foi importado')

# importando os módulos necessários
import pandas as pd
import os

# criando log
log = ''

# listando arquivos da pasta
def listCsvOfFolder(folder):
    files = os.listdir(folder)
    csv_file_path = []
    csv_file_name = []
    for item in files:
        if item[-3:] == 'csv':
            if item.lower().find('table') < 0:
                newItem = os.path.join(folder, item)
                csv_file_path.append(newItem)
    return csv_file_path
            

# ler arquivo csv
def readCSV(file, index_column = 0):
    # lê arquivo em CSV e converte em DataFrame
    try:
        # criando dataframe
        df = pd.read_csv(file,index_col = index_column)
        # uniformizando os nomes das colunas
        df.columns = df.columns.str.lower()
        return df
    except:
        print(f'Não foi possível ler o arquivo {file}')

# converter csvs em dataframes
def createDataFrames(files):
    mydf=[]
    try:
        mydf = [readCSV(f) for f in files]
        return mydf
    except:
        pass

# list unique column's name
def getColumnName(dataframes):
    if type(dataframes)==list:
        column_names = []
        for df in dataframes:
            for name in df.columns:
                column_names.append(name)
    
    elif type(dataframes)==dict:
        column_names = []
        for data in dataframes.keys():
            for name in dataframes[data].columns:
                column_names.append(name)        
    else:
        try:
            dataframes = list(dataframes)
            column_names = []
            for df in dataframes:
                for name in df.columns:
                    column_names.append(name)
            return set(column_names) 
        except:
            print('Não foi possível converter em lista')
            return False
    
    return set(column_names)  

def showColumn(column):
    # não sei o que fazer com ela
    pass

def showDates():
	pass

def searchColumnWith(words):
    # retorna um DataFrame onde tenha colunas com as seguintes palavras 

    '''
    def colunas_com(self,*palavras,onde=[]):
        self.log += f'\n\tBuscando colunas com {palavras}...\n'
        self.atualizar()
        if onde == []:
            onde = self.col
        palavras = [item.lower() for item in palavras]
        palavras = palavras[:3]
        colunas_validas = {}

        for palavra in palavras:
            palavra = palavra.lower()
            colunas_validas[palavra]=[]
            for candidato in onde:
                if candidato.find(palavra) >= 0:
                    colunas_validas[palavra].append(candidato)
        if len(palavras) == 2:
            resultado = list(set(colunas_validas[palavras[0]]) & set(colunas_validas[palavras[1]]))
        elif len(palavras) == 3:
            resultado = list(set(colunas_validas[palavras[0]]) & set(colunas_validas[palavras[1]]) & set(colunas_validas[palavras[2]]))
        else:
            resultado = list(set(colunas_validas[palavras[0]]))
        self.log += f'\n\tEncotramos as colunas: {resultado}'
        return resultado

    def buscar_colunas_com(self,*palavras,onde=[]):
        self.atualizar()
        self.log += f'\n\tBuscando colunas com: {palavras}'
        colunas_validas = []
        if onde == []:
            onde = self.col

        for nome in palavras:
            nome.lower()
            for coluna in onde:
                if coluna.find(nome)>-1:
                    colunas_validas.append(coluna)
        if len(colunas_validas) > 0:
            self.log += f'\n\tForam entregadas as colunas: {colunas_validas}'
            return colunas_validas
        self.log += f'\n\tNão encontrada coluna com {nome.upper()}'
        print(self.log.splitlines()[-1])

    def colunas_com(self,*palavras,onde=[]):
        self.log += f'\n\tBuscando colunas com {palavras}...\n'
        self.atualizar()
        if onde == []:
            onde = self.col
        palavras = [item.lower() for item in palavras]
        palavras = palavras[:3]
        colunas_validas = {}

        for palavra in palavras:
            palavra = palavra.lower()
            colunas_validas[palavra]=[]
            for candidato in onde:
                if candidato.find(palavra) >= 0:
                    colunas_validas[palavra].append(candidato)
        if len(palavras) == 2:
            resultado = list(set(colunas_validas[palavras[0]]) & set(colunas_validas[palavras[1]]))
        elif len(palavras) == 3:
            resultado = list(set(colunas_validas[palavras[0]]) & set(colunas_validas[palavras[1]]) & set(colunas_validas[palavras[2]]))
        else:
            resultado = list(set(colunas_validas[palavras[0]]))
        self.log += f'\n\tEncotramos as colunas: {resultado}'
        return resultado

    '''
    pass

def update(dataframe):
    col = list(dataframe.columns.str.lower())
    idx = list(dataframe.index)
    pass

def findOnDate(dataframe):
    '''
    def localizar_data(self,date):
        self.log += f'\n\t[!] A função <LOCALIZAR_DATA> não funciona corretamente'
        print(self.log.splitlines()[-1])
        date = str(date)
        if date[0]==' ':
            pass
        else:
            date = ' '+date
        try:
            return self.df.loc[date]
        except:
            self.log += '\n[!] Formato inadequado, tente usar self.df.loc...'
            print(self.log.splitlines()[-1])
    '''
    pass

def indexToDatetime():
    '''
    def index_para_datetime(self):
        self.log += '\n\tConvertendo as datas...'
        print(self.log.splitlines()[-1])
        novo_index = []
        for data in self.df.index:
            nova_hora = int(data[7:9])-1
            nova_hora = str(nova_hora)
            if len(nova_hora)<2:
                nova_hora = '0'+nova_hora
            else:
                pass
            datetime = data[:7]+nova_hora+data[9:]
            novo_index.append(datetime)
        self.df.index = novo_index
        self.df.index = pd.to_datetime(self.df.index,format='%m/%d  %H:00:00')
        datetime = pd.DataFrame(self.df.index,columns=['month'])
        datetime.index = self.df.index
        datetime['month'] = datetime.index.month
        datetime['day'] = datetime.index.day
        datetime['hour'] = datetime.index.hour
        self.df = pd.concat([datetime,self.df],axis=1)
        self.atualizar()
    '''
    pass

def averagePreviousOccurrences(dataframe,column_name):
    # por enquanto funciona apenas para dados horários
    previus_hours = 15 * 24 # day x hours in a day
    # copia as 360 horas finais do ano
    previus_serie = dataframe[column_name].iloc[-1*previus_hours:]
    # cria uma nova Serie onde duplica as horas finais antes do ano começar
    new_serie = pd.concat([previus_serie,dataframe[column_name]])
    # retira os campos vazios e calcula a media das ultimas 360 horas
    ##new_serie = new_serie[new_serie.notna()]
    new_serie = new_serie.rolling(previus_hours).mean()
    # retorna uma Series com as temperaturas médias
    return new_serie.iloc[previus_hours:]

def calculateAshraeLimits(temperature_column):
    cons = 0.31
    up_add = 21.3
    low_add = 14.3

    try:
        # calculating the limits
        upper_limit = temperature_column * cons + up_add
        lower_limit = temperature_column * cons + low_add

        # renaming dataframe
        upper_limit = upper_limit.rename('ashrae: upper limit')
        lower_limit = lower_limit.rename('ashrae: lower limit')

        # return new columns
        return (upper_limit,lower_limit)
    except:
        pass
    pass

def calculateDeDearLimits(temperature_column):
    '''
    def calcular_limites_dedear(self,coluna):
        coluna = coluna.lower()
        if coluna in self.col:
            self.log += f'\n\tCalculando os limites segundo De Dear para {coluna.split(":")[0].upper()}... '
            print(self.log.splitlines()[-1])
            self.limites['dedear']['upper'] = 'de dear:upper limit [c](daily)'
            self.limites['dedear']['lower'] = 'de dear:lower limit [c](daily)'
            self.df[self.limites['dedear']['upper']] = self.df[coluna] * 0.26 + 21.25
            self.df[self.limites['dedear']['lower']] = self.df[coluna] * 0.26 + 12.25
        else:
            self.log += f'\n[!] Não encontrada a coluna {coluna.upper()}'
            print(self.log.splitlines()[-1])
        self.atualizar()
    '''
    cons = 0.26
    up_add = 21.25
    low_add = 12.25

    try:
    	# calculating the limits
    	upper_limits = temperature_column * cons * up_limits
    	lower_limits = temperature_column * cons * low_limits

    	# renaming dataframe
    	upper_limits = upper_limits.rename('de dear: upper limit')
    	lower_limits = lower_limits.rename('de dear: lower limit')

    	# return new columns
    	return (upper_limits, lower_limits)
    except:
        pass

def adequacyOfTemperatureLimits(temperature_column, limit_column, upper=False, lower=False):
    # testa se as colunas são mesmo colunas válidas do pandas
    if type(temperature_column) == pd.Series and type(limit_column) == pd.Series:
        if upper == True:
            # is upper?
            adequacy = temperature_column >= limit_colum
        elif lower == True:
            # is lower?
            adequacy = temperature_column <= limit_colum
        else: pass

    else: pass
    
    return adequacy

def saveFile(df, path=''):
	df.to_csv(f'{path}{name}.csv', index=True, header=True)
	df.to_excel(f'{path}{name}.xlsx', sheet_name='Calculado', index=False, header=False)

def calculateDegreeHour(df, column):
	# up set point
	tmax = 26
	# low set point
	tmin = 18

	# degree cooling time
	dct = pd.Series(column.apply(lambda x: x - tmax if x >= tmax else 0))
	# degree heating time
	dht = pd.Series(column.apply(lambda x: x - tmin if x <= tmin else 0))

	# renaming the Series
	dct = dct.raname('degree cooling time')
	dht = dht.raname('degree heating time')

	return (dct, dht)

