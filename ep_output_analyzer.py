import pandas as pd
import os

def list_files_with_extension(folder, extension):
    file_paths = []
    for file in os.listdir(folder):
        if file.endswith(extension) and "table" not in file.lower():
            file_path = os.path.join(folder, file)
            file_paths.append(file_path)
    return file_paths

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, index_col=0)
        return df
    except Exception as e:
        print(f'\n! {file_path} não pode ser lido.\nError: {e}')
        return False

def read_eio_file(file_path):
    try:
        base = []
        header_line = ''
        copy = False
        with open(file_path[:-4] + '.eio', "r") as f:
            for line in f:
                if '! <Zone Information>' in line:
                    copy = True
                    header_line = line.strip()
                elif copy:
                    if '! <' in line and line != header_line:
                        break
                    else:
                        base.append(line.strip().split(','))
        df = pd.DataFrame(base, columns=header_line.split(',')) if base else pd.DataFrame()
        return df
    except Exception as e:
        print(f'{file_path} Error: {e}')
        return False

def get_column_names(dataframes):
    if isinstance(dataframes, list):
        column_names = set()
        for df in dataframes:
            column_names.update(df.columns)
    elif isinstance(dataframes, dict):
        column_names = set()
        for df in dataframes.values():
            column_names.update(df.columns)
    else:
        try:
            dataframes = list(dataframes)
            column_names = set()
            for df in dataframes:
                column_names.update(df.columns)
        except:
            print('Não foi possível converter em lista')
            return False
    return column_names

def get_long_stay_zones(all_columns):
    long_stay_zones = []
    for column in all_columns:
        if 'Zone Operative Temperature [C](Hourly)' in column:
            if ('C1' in column) and ('DO1' in column or 'DO2' in column or 'SAL' in column):
                long_stay_zones.append(column)
            elif ('DO1' in column or 'DO2' in column or 'SAL' in column) and 'C2' not in column:
                long_stay_zones.append(column)
            elif 'DORM' in column and 'COB' not in column:
                long_stay_zones.append(column)
    return long_stay_zones

def calculate_average_previous_occurrences(dataframe, column_name, previus_hours):
    previus_serie = dataframe[column_name].tail(previus_hours)
    new_serie = pd.concat([previus_serie, dataframe[column_name]])
    new_serie = new_serie.rolling(previus_hours).mean().iloc[previus_hours:]
    return new_serie

def calculate_ashrae_limits(temperature_column):
    cons = 0.31
    up_add = 21.3
    low_add = 14.3
    try:
        upper_limit = temperature_column * cons + up_add
        lower_limit = temperature_column * cons + low_add
        upper_limit.name = 'ashrae: upper limit'
        lower_limit.name = 'ashrae: lower limit'
        return lower_limit, upper_limit
    except:
        return (0,0)

def calculate_de_dear_limits(temperature_column):
    cons = 0.26
    up_add = 21.25
    low_add = 12.25
    try:
        upper_limit = temperature_column * cons + up_add
        lower_limit = temperature_column * cons + low_add
        upper_limit.name = 'de dear: upper limit'
        lower_limit.name = 'de dear: lower limit'
        return lower_limit, upper_limit
    except:
        return (0,0)

def calculate_ach(df, n_br, n_mod, location):
    col = df.columns
    area_factor = {'PQ': 0.5, 'SP': 0.25}.get(location.capitalize(), 1)
    floor_area = df[col[22]].astype(float).sum() * area_factor
    q_tot = 0.15 * floor_area + 3.5 * (n_br + 1 + n_mod)
    df['Total Required Ventilation Rate [L/s]'] = q_tot
    df['ACH Required'] = round(3.6 * q_tot / df[col[19]].astype(float), 3)
    df[col[1]] = df[col[1]].str.strip()
    df.columns = df.columns.str.strip()
    return df.iloc[:,[1,19,22,-2,-1]]

file_folder_source = '/energyplus/output/'
file_folder_output = '/energyplus/analyzed/'
outdoor_temperature = 'Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)'
prev_ext_air_temp_last_hours = 15 * 24
prev_ext_air_temp_column_name = f'Environment:Prevailing External Air Temperature In The Last {prev_ext_air_temp_last_hours} Hours [C](Hourly)'
csv_output = list_files_with_extension(file_folder_source,'.csv')
eio_output = list_files_with_extension(file_folder_source,'.eio')
analyzed = 'analyzed'
resume= [['building',
    'zone_name',
    'min_temperature',
    'mean_temperature',
    'max_temperature',
    'below_ashrae_limit',
    'between_ashrae_limit',
    'above_ashrae_limit',
    'below_de_dear_limit',
    'between_de_dear_limit',
    'above_de_dear_limit',
    'min_ach',
    'mean_ach',
    'max_ach',
    'sufficient_ach',
    'below_ashrae_limit_when_occupied',
    'between_ashrae_limit_when_occupied',
    'above_ashrae_limit_when_occupied',
    'below_de_dear_limit_when_occupied',
    'between_de_dear_limit_when_occupied',
    'above_de_dear_limit_when_occupied',
    'sufficient_ach_when_occupied']]
house = {}

for file_path in csv_output:
    name = file_path.split(os.sep)[-1][:-4]
    house[name] = {}
    house[name]['csv'] = read_csv_file(file_path)
    house[name]['eio'] = read_eio_file(file_path)

dataframes = [data_set['csv'] for data_set in house.values()]
long_stay_zones = get_long_stay_zones(get_column_names(dataframes))
long_stay_zones_code = []

for building, data in house.items():
    csv_data = data['csv']
    eio_data = data['eio']
    try:
        eio_data = calculate_ach(eio_data,n_br=2,n_mod=1,location=building[:2])
    except:
        pass
    csv_data[prev_ext_air_temp_column_name] = calculate_average_previous_occurrences(csv_data, outdoor_temperature, prev_ext_air_temp_last_hours)
    csv_data['ASHRAE: lower limits'], csv_data['ASHRAE: upper limits'] = calculate_ashrae_limits(csv_data[prev_ext_air_temp_column_name])
    csv_data['De Dear: lower limits'], csv_data['De Dear: upper limits'] = calculate_de_dear_limits(csv_data[prev_ext_air_temp_column_name])

    for zone in long_stay_zones:
        if zone in csv_data.columns:
            zone_name = zone.split(':')[0]
            long_stay_zones_code.append(zone_name)

            csv_data[zone_name + ':Is Below ASHRAE Limits'] = csv_data[zone].lt(csv_data['ASHRAE: lower limits'])
            csv_data[zone_name + ':Is Between ASHRAE Limits'] = csv_data[zone].between(csv_data['ASHRAE: lower limits'], csv_data['ASHRAE: upper limits'])
            csv_data[zone_name + ':Is Above ASHRAE Limits'] = csv_data[zone].gt(csv_data['ASHRAE: upper limits'])

            csv_data[zone_name + ':Is Below De Dear Limits'] = csv_data[zone].lt(csv_data['De Dear: lower limits'])
            csv_data[zone_name + ':Is Between De Dear Limits'] = csv_data[zone].between(csv_data['De Dear: lower limits'], csv_data['De Dear: upper limits'])
            csv_data[zone_name + ':Is Above De Dear Limits'] = csv_data[zone].gt(csv_data['De Dear: upper limits'])

            zone_ach = float(eio_data[eio_data['Zone Name'].isin([zone_name])]['ACH Required'])
            csv_data[zone_name + ':Sufficient ACH'] = csv_data[zone_name + ':AFN Zone Infiltration Air Change Rate [ach](Hourly)'].ge(zone_ach)

            min_temperature = float(csv_data[zone].min())
            mean_temperature = float(csv_data[zone].mean())
            max_temperature = float(csv_data[zone].max())

            if 'SAL' in zone_name:
                occupied = csv_data['SCH_OCUP_DORM:Schedule Value [](Hourly)'] == 1
            elif 'DO' in zone_name:
                occupied = csv_data['SCH_OCUP_DORM:Schedule Value [](Hourly)'] == 1

            below_ashrae_limit = 100 * csv_data[zone_name + ':Is Below ASHRAE Limits'].sum() / csv_data.shape[0]
            between_ashrae_limit = 100 * csv_data[zone_name + ':Is Between ASHRAE Limits'].sum() / csv_data.shape[0]
            above_ashrae_limit = 100 * csv_data[zone_name + ':Is Above ASHRAE Limits'].sum() / csv_data.shape[0]
            below_de_dear_limit = 100 * csv_data[zone_name + ':Is Below De Dear Limits'].sum() / csv_data.shape[0]
            between_de_dear_limit = 100 * csv_data[zone_name + ':Is Between De Dear Limits'].sum() / csv_data.shape[0]
            above_de_dear_limit = 100 * csv_data[zone_name + ':Is Above ASHRAE Limits'].sum() / csv_data.shape[0]
            sufficient_ach = 100 * csv_data[zone_name + ':Sufficient ACH'].sum() / csv_data.shape[0]
            min_ach = float(csv_data[zone_name + ':AFN Zone Infiltration Air Change Rate [ach](Hourly)'].min())
            mean_ach = float(csv_data[zone_name + ':AFN Zone Infiltration Air Change Rate [ach](Hourly)'].mean())
            max_ach = float(csv_data[zone_name + ':AFN Zone Infiltration Air Change Rate [ach](Hourly)'].max())

            below_ashrae_limit_when_occupied = 100 * csv_data[zone_name + ':Is Below ASHRAE Limits'][occupied].sum() / csv_data.shape[0]
            between_ashrae_limit_when_occupied = 100 * csv_data[zone_name + ':Is Between ASHRAE Limits'][occupied].sum() / csv_data.shape[0]
            above_ashrae_limit_when_occupied = 100 * csv_data[zone_name + ':Is Above ASHRAE Limits'][occupied].sum() / csv_data.shape[0]
            below_de_dear_limit_when_occupied = 100 * csv_data[zone_name + ':Is Below De Dear Limits'][occupied].sum() / csv_data.shape[0]
            between_de_dear_limit_when_occupied = 100 * csv_data[zone_name + ':Is Between De Dear Limits'][occupied].sum() / csv_data.shape[0]
            above_de_dear_limit_when_occupied = 100 * csv_data[zone_name + ':Is Above ASHRAE Limits'][occupied].sum() / csv_data.shape[0]
            sufficient_ach_when_occupied = 100 * csv_data[zone_name + ':Sufficient ACH'][occupied].sum() / csv_data.shape[0]

            resume.append([building,
                            zone_name,
                            min_temperature,
                            mean_temperature,
                            max_temperature,
                            below_ashrae_limit,
                            between_ashrae_limit,
                            above_ashrae_limit,
                            below_de_dear_limit,
                            between_de_dear_limit,
                            above_de_dear_limit,
                            min_ach,
                            mean_ach,
                            max_ach,
                            sufficient_ach,
                            below_ashrae_limit_when_occupied,
                            between_ashrae_limit_when_occupied,
                            above_ashrae_limit_when_occupied,
                            below_de_dear_limit_when_occupied,
                            between_de_dear_limit_when_occupied,
                            above_de_dear_limit_when_occupied,
                            sufficient_ach_when_occupied])

    csv_data.to_csv(f"{file_folder_output}{building}_{analyzed}.csv", index=False)

resume = pd.DataFrame(resume[1:],columns=resume[0])
resume.to_csv(f"{file_folder_output}resume.csv", index=False)

print('END')