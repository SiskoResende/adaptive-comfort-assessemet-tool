import os
import pandas as pd

__version__ = '1.0.0'

class EPOutputProcess():
    def __init__(self,arquivo_csv,converter_data=True):
        self.df = None
        self.col = None
        self.idx = None
        self.preview = None
        self.colunas_medias = None
        self.limites = {'ashrae' : {}, 'dedear' : {}}
        self.log = ''
        self.nome = 'LOG\n===\n\n'
        self.resumo = [[
            'zona',
            'temperatura maxima [c]',
            'temperatura minima [c]',
            'graus-hora resfriamento [c]',
            'graus-hora aquecimento [c]',
            'graus-hora resfriamento quando ocupado [c]',
            'graus-hora aquecimento quando ocupado [c]',
            'ashrae: desconforto por calor [%]',
            'ashrae: desconforto por frio [%]',
            'ashrae: total em conforto [%]',
            'ashrae: desconforto por calor quando ocupado [%]',
            'ashrae: desconforto por frio quando ocupado [%]',
            'ashrae: total em conforto quando ocupado [%]',
            'de dear: desconforto por calor [%]',
            'de dear: desconforto por frio [%]',
            'de dear: total em conforto [%]',
            'de dear: desconforto por calor quando ocupado [%]',
            'de dear: desconforto por frio quando ocupado [%]',
            'de dear: total em conforto quando ocupado [%]',
            'ashrae: desconforto por calor [h]',
            'ashrae: desconforto por frio [h]',
            'ashrae: desconforto por calor quando ocupado [h]',
            'ashrae: desconforto por frio quando ocupado [h]',
            'de dear: desconforto por calor [h]',
            'de dear: desconforto por frio [h]',            
            'de dear: desconforto por calor quando ocupado [h]',
            'de dear: desconforto por frio quando ocupado [h]',
            'ach: 0_2 [%]',
            'ach: 2_4 [%]',
            'ach: 4_6 [%]',
            'ach: 6_8 [%]',
            'ach: 8_∞ [%]',
            'ach: 0_2 [h]',
            'ach: 2_4 [h]',
            'ach: 4_6 [h]',
            'ach: 6_8 [h]',
            'ach: 8_∞ [h]',
            'ach: 0_2 quando ocupado [%]',
            'ach: 2_4 quando ocupado [%]',
            'ach: 4_6 quando ocupado [%]',
            'ach: 6_8 quando ocupado [%]',
            'ach: 8_∞ quando ocupado [%]',
            'ach: 0_2 quando ocupado [h]',
            'ach: 2_4 quando ocupado [h]',
            'ach: 4_6 quando ocupado [h]',
            'ach: 6_8 quando ocupado [h]',
            'ach: 8_∞ quando ocupado [h]',
            'total de horas [h]',
            'total de horas ocupadas [h]']]
        self.ler_csv(arquivo_csv)
        if converter_data == True:
            self.index_para_datetime()
        else:
            self.df.index = self.df.index = pd.to_datetime(self.df.index)
            self.atualizar()
    
    def atualizar(self):
        self.col = list(self.df.columns.str.lower())
        self.idx = list(self.df.index)

    def ler_csv(self,arquivo_csv,index_col=0):
        '''Carrega o CSV do EnergyPlus, salva como DataFrame e salva os nomes das colunas'''
        try:
            self.log += f'Lendo dados do arquivo {arquivo_csv.upper()}...'
            print(self.log.splitlines()[-1])
            self.df = pd.read_csv(arquivo_csv,index_col=index_col)
            self.df.columns = self.df.columns.str.strip()
            self.df.columns = self.df.columns.str.lower()
            self.df.index = self.df.index.str.strip()
            self.nome = arquivo_csv[:-4]
            self.atualizar()
        except:
            self.log += f'\n[!] Algo deu errado ao ler o arquivo {arquivo_csv.upper()}'
            print(self.log.splitlines()[-1])

    def mostrar_colunas(self):
        self.log += f'\n\tMostrando colunas...'
        num_col = self.df.shape[1]
        if num_col >= 2:
            txt = ['Existem','colunas']
        elif num_col == 1:
            txt = ['Existe','coluna']
        else:
            txt =['Não há colunas nesse DataFrame','']
            print(txt)
        print(f'{txt[1]} {num_col}{txt[1]}\nID -   NOME')
        for idx,coluna in enumerate(self.col):
            print(f'{idx} --> {coluna}')

    def localizar_data(self,date):
        '''[!] Não funciona'''
        '''Localiza datas simples. Para seleção mais refinada tente usar a função self.df.loc (Consulte adocumentação do Pandas).'''
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

    def media_ocorrencias_anteriores(self,coluna,quantidade):
        '''Lê dados diários e retorna dados horários'''
        self.atualizar()
        if coluna in self.col:
            if self.df[coluna].notna().sum() == 365:
                self.log += f'\n\tCalculando médias de uma quantidade de {quantidade}...'
                print(self.log.splitlines()[-1])
                nome_limite = f'{coluna.split(":")[0]}:mean{quantidade} {" ".join(coluna.split(":")[1:])}'
                self.coluna_medias = nome_limite
                tmp_df = self.df[coluna]
                tmp_df = pd.DataFrame(tmp_df[tmp_df.notna()])
                tmp_df.index = pd.date_range('1900-01-01', periods=365, freq='D')
                tmp_df_quantidade = tmp_df.loc[tmp_df.index[-(quantidade):]]
                tmp_df_quantidade.index = pd.date_range(f'1899-12-{31-quantidade}', periods=quantidade, freq='D')
                tmp_df = pd.concat([tmp_df_quantidade,tmp_df],axis=0)
                tmp_df[nome_limite] = tmp_df[coluna].rolling(quantidade,min_periods=quantidade).mean()
                tmp_df = tmp_df[[self.coluna_medias]]
                ultima_linha = tmp_df.iloc[[-1]]
                ultima_linha.index = pd.date_range('1901-01-01', periods=1, freq='D')
                tmp_df = pd.concat([tmp_df,ultima_linha],axis=0)
                self.preview = tmp_df
                tmp_df = tmp_df.resample('H').ffill()
                self.preview = tmp_df
                tmp_df = tmp_df.loc['1900-01-01':'1900-12-31']
                self.preview = tmp_df
                self.df = pd.concat([self.df,tmp_df],axis=1)
                self.atualizar()
                self.preview = tmp_df
            else:
                self.log += f'\n\t[!] A coluna {coluna.upper()} não contém dados diários'
                print(self.log.splitlines()[-1])
        else:
            self.log += f'\n\t[!] A tabela não tem a coluna {coluna.upper()}'
            print(self.log.splitlines()[-1])
        
    def calcular_limites_ashrae(self,coluna):
        coluna = coluna.lower()
        if coluna in self.col:
            self.log += f'\n\tCalculando os limites da ASHRAE para {coluna.split(":")[0].upper()}... '
            print(self.log.splitlines()[-1])
            self.limites['ashrae']['upper'] = 'ashrae:upper limit [c](daily)'
            self.limites['ashrae']['lower'] = 'ashrae:lower limit [c](daily)'
            self.df[self.limites['ashrae']['upper']] = self.df[coluna] * 0.31 + 21.3
            self.df[self.limites['ashrae']['lower']] = self.df[coluna] * 0.31 + 14.3
        else:
            self.log += f'\n\t[!] Não encontrada a coluna {coluna.upper()}'
            print(self.log.splitlines()[-1])
        self.atualizar()

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

    def avaliar_adequacao_limites(self,*colunas):
        for metodo in self.limites:
            if self.limites[metodo] != {}:
                for limite in self.limites[metodo]:
                    for coluna in colunas:
                        nome_coluna = coluna.split(':')[0]
                        nome_limite = self.limites[metodo][limite].split(':')
                        self.log += f'\n\tAvaliando adequação de {nome_coluna}'
                        if limite == 'upper':
                            onde = 'above'
                            adequacao = self.df[coluna] >= self.df[':'.join(nome_limite)]
                        if limite == 'lower':
                            onde = 'below'
                            adequacao = self.df[coluna] <= self.df[':'.join(nome_limite)]
                        nome = f'{nome_coluna}:{onde} the {nome_limite[0]} {nome_limite[1][:-10]}[](daily)'
                        adequacao = adequacao.astype(int)
                        self.df[nome] = adequacao
            else:
                self.log += f'\n\t[!] Os limites para {metodo.upper()} não foram calculados'
                print(self.log.splitlines()[-1])
        self.atualizar()

    def salvar_tabela(self,nome,caminho=''):
        self.log += f'\n\tSalvando tabela com os dados brutos...'
        print(self.log.splitlines()[-1])
        novo_arquivo = f'{caminho}{self.nome}_{nome}'
        self.df.to_csv(f'{novo_arquivo}.csv',index=True,header=True)
        self.df.to_excel(f'{novo_arquivo}.xlsx',sheet_name='BaseCalculo',index=False,header=False)

    def salvar_log(self,nome,caminho=''):
        novo_arquivo = f'{caminho}{self.nome}_{nome}'
        self.log += f'\n\tSalvando logs...'
        f = open(f'{novo_arquivo}.log','w')
        f.write(self.log)
        f.close()
        pass

    def calcular_grauhora(self,coluna,tmax=26,tmin=18):
        self.log += f'\n\tCalculando Grau-hora para Resfriamento e Aquecimento'
        print(self.log.splitlines()[-1])
        nome = coluna.split(':')[0]
        ghr = pd.Series(self.df[coluna].apply(lambda x: x-tmax if x >= tmax else 0))
        gha = pd.Series(self.df[coluna].apply(lambda x: tmin-x if x <= tmin else 0))
        self.df[f'{nome}:cooling degree hours [](hours)'] = ghr
        self.df[f'{nome}:heating degree hours [](hours)'] = gha

    def resumo_ashrae(self,zona,ocup):
        '''Retorna um DICT.'''
        resultado = {}
        ab = self.colunas_com(zona,'above the ashrae upper limit')[0]
        be = self.colunas_com(zona,'below the ashrae upper limit')[0]
        ab = self.df[ab]
        be = self.df[be]


        resultado['ash_sup'] = ab.sum()
        resultado['ash_inf'] = be.sum()
        resultado['ash_sup_ocp'] = ocup[ab].sum()
        resultado['ash_inf_ocp'] = ocup[be].sum()

        resultado['ash_sup_per'] = round(resultado['ash_sup']/resultado['tds_horas'],4)
        resultado['ash_sup_ocp_per'] = round(resultado['ash_sup_ocp']/resultado['horas_ocp'],4)
        resultado['ash_inf_per'] = round(resultado['ash_inf']/resultado['tds_horas'],4)
        resultado['ash_inf_ocp_per'] = round(resultado['ash_inf_ocp']/resultado['horas_ocp'],4)
        return resultado

    def resumir_ach(self,zona,ocup):
        resultado = {}
        ach = self.df[self.colunas_com(zona,'afn','air change rate')[0]]
        ach_ocup = ocup[self.colunas_com(zona,'afn','air change rate')[0]]

        resultado['ach02']  = ach[ach < 2].count()
        resultado['ach24'] = ach[(ach >= 2) & (ach < 4)].count()
        resultado['ach46'] = ach[(ach >= 4) & (ach < 6)].count()
        resultado['ach68'] =ach[(ach >= 6) & (ach < 8)].count()
        resultado['ach8+']  = ach[ach >= 8].count()

        resultado['achocp02']  = ach_ocup[ach_ocup < 2].count()
        resultado['achocp24'] = ach_ocup[(ach_ocup >= 2) & (ach_ocup < 4)].count()
        resultado['achocp46'] = ach_ocup[(ach_ocup >= 4) & (ach_ocup < 6)].count()
        resultado['achocp68'] = ach_ocup[(ach_ocup >= 6) & (ach_ocup < 8)].count()
        resultado['achocp8+']  = ach_ocup[ach_ocup >= 8].count()
        return resultado

    def resumir_entradas(self,zona,ocupacao,tipo_ocup):
        self.log += f'\n\tCriando resumo dos dados de {zona}...'
        print(self.log.splitlines()[-1])
        limit_zona = self.colunas_com(zona,'limit')
        ocup_zona = self.colunas_com(ocupacao,tipo_ocup)

        resumo = {}

        # self.resumo_ashrae(self,zona,ocup)

        ab_ash = self.colunas_com('above','ashrae',onde=limit_zona)[0]
        be_ash = self.colunas_com('below','ashrae',onde=limit_zona)[0]

        ab_dde = self.colunas_com('above','de dear',onde=limit_zona)[0]
        be_dde = self.colunas_com('below','de dear',onde=limit_zona)[0]

        ghr = self.colunas_com(zona,'cooling','degree hours')[0]
        gha = self.colunas_com(zona,'heating','degree hours')[0]

        ocup = self.df[limit_zona+ocup_zona+[ghr,gha]]
        ocup = ocup[ocup[ocup_zona[0]]>0]

        tempop = self.colunas_com(zona,'operative')[0]

        ach = self.df[self.colunas_com(zona,'afn','air change rate')[0]]
        ach_ocup = self.df[self.df[ocup_zona[0]]>0][self.colunas_com(zona,'afn','air change rate')[0]]

        resumo['nome'] = limit_zona[0].split(':')[0]
        resumo['tds_horas'] = self.df.shape[0]
        resumo['horas_ocp'] = ocup.shape[0]

        resumo['tmax'] = self.df[tempop].round(2).max()
        resumo['tmin'] = self.df[tempop].round(2).min()

        resumo['ash_sup'] = self.df[ab_ash].sum()
        resumo['ash_sup_per'] = round(resumo['ash_sup']/resumo['tds_horas'],4)
        resumo['ash_sup_ocp'] = ocup[ab_ash].sum()
        resumo['ash_sup_ocp_per'] = round(resumo['ash_sup_ocp']/resumo['horas_ocp'],4)
        resumo['ash_inf'] = self.df[be_ash].sum()
        resumo['ash_inf_per'] = round(resumo['ash_inf']/resumo['tds_horas'],4)
        resumo['ash_inf_ocp'] = ocup[be_ash].sum()
        resumo['ash_inf_ocp_per'] = round(resumo['ash_inf_ocp']/resumo['horas_ocp'],4)
        
        resumo['dde_sup'] = self.df[ab_dde].sum()
        resumo['dde_sup_per'] = round(resumo['dde_sup']/resumo['tds_horas'],4)
        resumo['dde_sup_ocp'] = ocup[ab_dde].sum()
        resumo['dde_sup_ocp_per'] = round(resumo['dde_sup_ocp']/resumo['horas_ocp'],4)
        resumo['dde_inf'] = self.df[be_dde].sum()
        resumo['dde_inf_per'] = round(resumo['dde_inf']/resumo['tds_horas'],4)
        resumo['dde_inf_ocp'] = ocup[be_dde].sum()
        resumo['dde_inf_ocp_per'] = round(resumo['dde_inf_ocp']/resumo['horas_ocp'],4)

        resumo['ghr'] = round(self.df[ghr].sum(),2)
        resumo['gha'] = round(self.df[gha].sum(),2)
        resumo['ghr_ocp'] = round(ocup[ghr].sum(),2)
        resumo['gha_ocp'] = round(ocup[gha].sum(),2)

        resumo['ach2-']  = ach[ach < 2].count()
        resumo['ach2_4'] = ach[(ach >= 2) & (ach < 4)].count()
        resumo['ach4_6'] = ach[(ach >= 4) & (ach < 6)].count()
        resumo['ach6_8'] =ach[(ach >= 6) & (ach < 8)].count()
        resumo['ach8+']  = ach[ach >= 8].count()

        resumo['achocp2-']  = ach_ocup[ach_ocup < 2].count()
        resumo['achocp2_4'] = ach_ocup[(ach_ocup >= 2) & (ach_ocup < 4)].count()
        resumo['achocp4_6'] = ach_ocup[(ach_ocup >= 4) & (ach_ocup < 6)].count()
        resumo['achocp6_8'] = ach_ocup[(ach_ocup >= 6) & (ach_ocup < 8)].count()
        resumo['achocp8+']  = ach_ocup[ach_ocup >= 8].count()

        avaliacao = [
            resumo['nome'],
            resumo['tmax'],
            resumo['tmin'],
            resumo['ghr'],
            resumo['gha'],
            resumo['ghr_ocp'],
            resumo['gha_ocp'],
            resumo['ash_sup_per'],
            resumo['ash_inf_per'],
            1 - (resumo['ash_sup_per'] + resumo['ash_inf_per']),
            resumo['ash_sup_ocp_per'],
            resumo['ash_inf_ocp_per'],
            1 - (resumo['ash_sup_ocp_per'] + resumo['ash_inf_ocp_per']),
            resumo['dde_sup_per'],
            resumo['dde_inf_per'],
            1 - (resumo['dde_sup_per'] + resumo['dde_inf_per']),
            resumo['dde_sup_ocp_per'],
            resumo['dde_inf_ocp_per'],
            1 - (resumo['dde_sup_ocp_per'] + resumo['dde_inf_ocp_per']),
            resumo['ash_sup'],
            resumo['ash_inf'],
            resumo['ash_sup_ocp'],
            resumo['ash_inf_ocp'],
            resumo['dde_sup'],
            resumo['dde_inf'],
            resumo['dde_sup_ocp'],
            resumo['dde_inf_ocp'],
            round(resumo['ach2-']/resumo['tds_horas'],4),
            round(resumo['ach2_4']/resumo['tds_horas'],4),
            round(resumo['ach4_6']/resumo['tds_horas'],4),
            round(resumo['ach6_8']/resumo['tds_horas'],4),
            round(resumo['ach8+']/resumo['tds_horas'],4),
            resumo['ach2-'],
            resumo['ach2_4'],
            resumo['ach4_6'],
            resumo['ach6_8'],
            resumo['ach8+'],
            round(resumo['achocp2-']/resumo['horas_ocp'],4),
            round(resumo['achocp2_4']/resumo['horas_ocp'],4),
            round(resumo['achocp4_6']/resumo['horas_ocp'],4),
            round(resumo['achocp6_8']/resumo['horas_ocp'],4),
            round(resumo['achocp8+']/resumo['horas_ocp'],4),
            resumo['achocp2-'],
            resumo['achocp2_4'],
            resumo['achocp4_6'],
            resumo['achocp6_8'],
            resumo['achocp8+'],
            resumo['tds_horas'],
            resumo['horas_ocp']
            ]
        self.resumo.append(avaliacao)
        return avaliacao

    def calcular_adequacao_limites(self,**kwargs):
        self.media_ocorrencias_anteriores(kwargs['temp_externa'],kwargs['periodo'])
        self.calcular_limites_ashrae(self.coluna_medias)
        self.calcular_limites_dedear(self.coluna_medias)
        
        colunas_interesse = []
        for zona in kwargs['zonas']:
            coluna =self.colunas_com(zona[0],'operative')
            colunas_interesse += coluna
        for coluna in colunas_interesse:
            self.calcular_grauhora(coluna,tmax=kwargs['grauhora'][0],tmin=kwargs['grauhora'][1])
        self.avaliar_adequacao_limites(*colunas_interesse)
        for zona,ocupacao,tipo in kwargs['zonas']:
            self.resumir_entradas(zona,ocupacao,tipo)
        self.salvar_tabela('bruto')
        self.salvar_log('bruto')

def rodar():
    lista_arquivos = [arquivo for arquivo in os.listdir() if arquivo[-3:].lower()=='csv']
    zonas = (('c1sal','ocup','sala'),('c1do1','ocup','dorm'),('c1do2','ocup','dorm'))
    resumo = []
    novo_titulo = []
    novo_arquivo = 'resumo'

    for csv in lista_arquivos:
        if csv.find('bruto') < 0 and csv.find(novo_arquivo) < 0:
            modelo = EPOutputProcess(csv)
            temp_externa = modelo.colunas_com('environment','drybulb temperature')[0]
            modelo.calcular_adequacao_limites(periodo=15,temp_externa=temp_externa,grauhora=(26,18),zonas=zonas)
            for linha in modelo.resumo[1:]:
                nova_linha = [modelo.nome] + linha
                resumo.append(nova_linha)
            novo_titulo = ['modelo'] + modelo.resumo[0]
            print('\tTerminado\n\n')

    print('Criando resumo...')
    resumido = pd.DataFrame(resumo,columns=novo_titulo)
    # col = resumido['zona']
    resumido = resumido.T
    # resumido.columns = col
    print('Salvando resumo...')
    resumido.to_csv(f'{novo_arquivo}.csv',index=True,header=False)
    resumido.to_excel(f'{novo_arquivo}.xlsx',sheet_name='BaseCalculo',index=True,header=False)
    print('\n')
    pass

if __name__ == '__main__':
    print(f'{"="*80}\nCALCULATOR DESCONFORTATOR v{version}\n{"="*80}\n')
    rodar()
    print(f'\n{"-"*80}\n\nTodos dados foram calculados. Obrigado pela confiança!')
    input('Agora pressione <ENTER> para sair\nTchau\n\n')

print('\n\ncomfortassessmen.py\n','='*80)