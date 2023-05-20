# importando os módulos necessários
import pandas as pd
import os

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
        #df.columns = df.columns.str.lower()
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
    pass

def update(dataframe):
    col = list(dataframe.columns.str.lower())
    idx = list(dataframe.index)
    pass

def findOnDate(dataframe):
    # retorna um dataframe a partir das datas passadas
    pass

def indexToDatetime():
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
        return (lower_limit,upper_limit)
    except:
        pass
    pass

def calculateDeDearLimits(temperature_column):
    # retorna uma tupla com o limite superior e inferior
    cons = 0.26
    up_add = 21.25
    low_add = 12.25
    up_name = 'de dear: upper limit'
    low_name = 'de dear: lower limit'

    try:
    	# calculating the limits
    	upper_limits = temperature_column * cons + up_add
    	lower_limits = temperature_column * cons + low_add

    	# renaming dataframe
    	upper_limits = upper_limits.rename(up_name)
    	lower_limits = lower_limits.rename(low_name)

    	# return new columns
    	return (lower_limits,upper_limits)
    except:
        pass

def isBelow(zone_temperature, limit_temperature):
    # parametros: temperaturas, temperatura limite
    # retorna coluna com dados boleanos para as ocorrências acima
    return zone_temperature.lt(limit_temperature)

def isAbove(zone_temperature, limit_temperature):
    # parametros: temperaturas, temperatura limite
    # retorna coluna com dados boleanos para as ocorrências abaixo
    return zone_temperature.gt(limit_temperature)

def isBetween(zone_temperature, lower_limit, upper_limit):
    # parametros: temperaturas, temperatura limite
    # retorna coluna com dados boleanos para as ocorrências entre os limites
    return zone_temperature.between(lower_limit,upper_limit)
    
def adequacyOfTemperatureLimits(temperature_column, limit_column, upper=False, lower=False):
    # testa se as colunas são mesmo colunas válidas do pandas
    if type(temperature_column) == pd.Series and type(limit_column) == pd.Series:
        if upper == True:
            # is upper?
            adequacy = temperature_column >= limit_colum
        elif lower == True:
            # is lower?
            adequacy = temperature_column <= limit_colum
        else:
            return False

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

