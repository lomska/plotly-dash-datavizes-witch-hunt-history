# Imports ********************************************************************************************************************

import pandas as pd
import numpy as np
import geopandas as gpd


# Datasets *******************************************************************************************************************

trials = pd.read_csv('data/trials.csv')
battles = pd.read_csv('data/battles.csv')
nuts = gpd.read_file('data/NUTS_LB_2021_4326.geojson')


# Fixing data types & some mistakes ******************************************************************************************

trials = trials.rename(columns = {'gadm.adm0':'country',
                                  'deaths':'executed'})

trials['executed'] = trials['executed'].fillna(0)
trials['executed'] = trials['executed'].astype('int')

trials = trials.drop_duplicates()

def fix_region_0(s): 
    if s['gadm.adm1'] == 'Valais': # Valais is in Switzerland, not in France.
        return 'Switzerland'
    else:
        return s['country']
trials['country'] = trials.apply(fix_region_0, axis=1)

def fix_region_1(s):
    if s['gadm.adm1'] == 'Appenzell': # there's Appenzell Ausserrhoden and Appenzell Innerrhoden, and according to the data from
                                      # surrounding years, "Appenzell" in 1550, 1560, 1570, 1580, and 1590 more likely stands
                                      # for Appenzell Ausserrhoden: 1) they have no intersectional years 2) death rate is 100% 
                                      # in both
        return 'Appenzell Ausserrhoden'
    else:
        return s['gadm.adm1']
trials['gadm.adm1'] = trials.apply(fix_region_1, axis=1)

def fix_region_2(s): 
    if s['gadm.adm1'] == 'Wallonie' and s['gadm.adm2'] == 'Luxembourg': # Luxembourg is also a region in Belgium.
        return 'Luxembourg (BE)'
    else:
        return s['gadm.adm2']
trials['gadm.adm2'] = trials.apply(fix_region_2, axis=1)

trials['city'] = trials['city'].replace('kotz', 'Kotz')
battles = battles.replace(['England', 'Northern Ireland', 'Scotland', 'Wales'], 'United Kingdom')

def fix_battle(s):
    if s['year'] == 1644 and s['battle'] == 'Beacon Hill':
        return 'Lostwithiel'
    elif s['battle'] == 'St. Omer ':
        return 'Saint-Omer'
    elif s['year'] == 1627 and s['battle'] == 'Ile de Re':
        return 'La Rochelle'
    else:
        return s['battle']

battles['battle'] = battles.apply(fix_battle, axis=1)

def fix_war(s):
    if s['war'] == "Eighty Years' War" and s['battle'] == 'Saint-Omer':
        return "Thirty Years' War"
    else:
        return s['war']
battles['war'] = battles.apply(fix_war, axis=1)


# New columns ****************************************************************************************************************

def new_region(s):
    # Denmark
    if s['gadm.adm1'] in ('Fyn', 'Ribe', 'South Jutland'):
        return 'Southern Denmark'
    elif s['gadm.adm1'] == 'Ringkobing':
        return 'Central Jutland'
    elif s['gadm.adm1'] == 'Storstrom':
        return 'Zealand'
    # Ireland
    elif s['gadm.adm1'] in ('Cork', 'Kilkenny', 'Clare', 'Wexford', 'Waterford', 'Tipperary', 'Limerick'):
        return 'Southern'
    elif s['gadm.adm1'] in ('Louth', 'Meath', 'Dublin'):
        return 'Eastern and Midland'
    elif s['gadm.adm1'] in ('Donegal', 'Galway'):
        return 'Northern and Western'
    # Germany
    elif s['gadm.adm2'] in ('Magdeburg', 'Dessau', 'Halle'): 
        return 'Sachsen-Anhalt'
    # UK
    elif s['gadm.adm2'] in ('Hertfordshire', 'Bedfordshire'):
        return 'Bedfordshire and Hertfordshire' 
    elif s['gadm.adm2'] in ('Oxfordshire', 'Buckinghamshire', 'Berkshire'):
        return 'Berkshire, Buckinghamshire and Oxfordshire'
    elif s['gadm.adm2'] == 'Cornwall':
        return 'Cornwall and Isles of Scilly'
    elif s['gadm.adm2'] in ('Nottingham', 'Derby', 'Derbyshire'):
        return 'Derbyshire and Nottinghamshire'
    elif s['gadm.adm2'] in ('Dorset', 'Somerset'):
        return 'Dorset and Somerset'
    elif s['gadm.adm2'] in ('Norfolk', 'Cambridgeshire', 'Suffolk'):
        return 'East Anglia'
    elif s['gadm.adm2'] == 'Cardiff':
        return 'East Wales'
    elif s['gadm.adm2'] == 'East Riding of Yorkshire':
        return 'East Yorkshire and Northern Lincolnshire'
    elif s['gadm.adm2'] in ('Fife', 'Stirling', 'Angus', 'Perthshire and Kinross', 'Edinburgh', 'East Lothian',
                            'West Lothian', 'Clackmannanshire', 'Dundee'):
        return 'Eastern Scotland'    
    elif s['gadm.adm2'] in ('Wiltshire', 'Bristol', 'Gloucestershire'):
        return 'Gloucestershire, Wiltshire and Bristol/Bath area'
    elif s['gadm.adm2'] == 'Manchester':
        return 'Greater Manchester'
    elif s['gadm.adm2'] in ('Hampshire', 'Southampton'):
        return 'Hampshire and Isle of Wight'
    elif s['gadm.adm2'] in ('Worcestershire', 'Warwickshire'):
        return 'Herefordshire, Worcestershire and Warwickshire'
    elif s['gadm.adm2'] in ('Highland', 'Orkney Islands', 'Argyll and Bute', 'Shetland Islands', 'Moray'):
        return 'Highlands and Islands'
    elif s['gadm.adm2'] in ('Leicester', 'Rutland', 'Northamptonshire'):
        return 'Leicestershire, Rutland and Northamptonshire'
    elif s['gadm.adm2'] in ('Aberdeenshire', 'Aberdeen'):
        return 'North Eastern Scotland'
    elif s['gadm.adm2'] == 'York':
        return 'North Yorkshire'
    elif s['gadm.adm2'] in ('Newry and Mourne', 'Lisburn', 'Dungannon', 'Derry', 'Armagh', 'Antrim'):
        return 'Northern Ireland'
    elif s['gadm.adm2'] in ('Tyne and Wear', 'Northumberland'):
        return 'Northumberland and Tyne and Wear'
    elif s['gadm.adm2'] in('Richmond upon Thames', 'Hounslow'):
        return 'Outer London — West and North West'
    elif s['gadm.adm2'] in ('Shropshire', 'Staffordshire'):
        return 'Shropshire and Staffordshire'
    elif s['gadm.adm2'] in ('Scottish Borders', 'South Ayrshire', 'Dumfries and Galloway', 'South Lanarkshire', 
                            'East Ayrshire'):
        return 'Southern Scotland'
    elif s['gadm.adm2'] in ('East Sussex', 'West Sussex', 'Brighton and Hove'):
        return 'Surrey, East and West Sussex'
    elif s['gadm.adm2'] in ('Durham', 'Darlington'):
        return 'Tees Valley and Durham'
    elif s['gadm.adm2'] in ('West Dunbartonshire', 'Renfrewshire', 'North Lanarkshire'):
        return 'West Central Scotland'
    elif s['gadm.adm2'] in ('Carmarthenshire', 'Pembrokeshire'):
        return 'West Wales and The Valleys'
    # Portugal
    elif s['gadm.adm1'] == 'Faro':
        return 'Algarve'
    elif s['gadm.adm1'] in ('Grevenmacher', 'Luxembourg'):
        return 'Luxembourg'
    # Don't need to be corrected
    elif s['country'] in ('Austria', 'Czech Republic', 'France', 'Italy', 'Netherlands', 'Poland', 'Spain', 
                          'Sweden', 'Switzerland'):
        return s['gadm.adm1']
    elif s['country'] in ('Belgium', 'Germany', 'United Kingdom'):
        return s['gadm.adm2']
    elif s['country'] in ('Estonia', 'Finland', 'Hungary', 'Norway'):
        return s['country']
    
trials['new_region'] = trials.apply(new_region, axis=1)
battles['new_region'] = battles.apply(new_region, axis=1)

new_id_dict = {
    'Niederosterreich': 'AT12',
    'Wien': 'AT13',
    'Steiermark': 'AT22',
    'Oberosterreich': 'AT31',
    'Salzburg': 'AT32',
    'Tirol': 'AT33',
    'Vorarlberg': 'AT34',
    'Namur': 'BE35',
    'Liege': 'BE33',
    'Hainaut': 'BE32',
    'Brabant Wallon': 'BE31',
    'Luxembourg (BE)': 'BE34',
    'Bruxelles': 'BE10',
    'West-Vlaanderen': 'BE25',
    'Oost-Vlaanderen': 'BE23',
    'Vlaams Brabant': 'BE24',
    'Antwerpen': 'BE21',
    'Plzensky': 'CZ032',
    'Jihocesky': 'CZ031',
    'Prague': 'CZ010',
    'Jihomoravsky': 'CZ064',
    'Stredocesky': 'CZ020',
    'Olomoucky': 'CZ071',
    'Alsace': 'FRF1',
    'Aquitaine': 'FRI1',
    'Auvergne': 'FRK1',
    'Basse-Normandie': 'FRD1',
    'Bourgogne': 'FRC1',
    'Bretagne': 'FRH0',
    'Centre': 'FRB0',
    'Champagne-Ardenne': 'FRF2',
    'Franche-Comte': 'FRC2',
    'Haute-Normandie': 'FRD2',
    'Ile-de-France': 'FR10',
    'Languedoc-Roussillon': 'FRJ1',
    'Limousin': 'FRI2',
    'Lorraine': 'FRF3',
    'Midi-Pyrenees': 'FRJ2',
    'Nord-Pas-de-Calais': 'FRE1',
    'Pays de la Loire': 'FRG0',
    'Picardie': 'FRE2',
    'Poitou-Charentes': 'FRI3',
    "Provence-Alpes-Cote d'Azur": 'FRL0',
    'Rhone-Alpes': 'FRK2',
    'Stuttgart': 'DE11',
    'Karlsruhe': 'DE12',
    'Freiburg': 'DE13',
    'Tubingen': 'DE14',
    'Oberbayern': 'DE21',
    'Niederbayern': 'DE22',
    'Oberpfalz': 'DE23',
    'Oberfranken': 'DE24',
    'Mittelfranken': 'DE25',
    'Unterfranken': 'DE26',
    'Schwaben': 'DE27',
    'Berlin': 'DE30',
    'Brandenburg': 'DE40',
    'Hamburg': 'DE60',
    'Darmstadt': 'DE71',
    'Giessen': 'DE72',
    'Kassel': 'DE73',
    'Mecklenburg-Vorpommern': 'DE80',
    'Braunschweig': 'DE91',
    'Hannover': 'DE92',
    'Luneburg': 'DE93',
    'Weser-Ems': 'DE94',
    'Dusseldorf': 'DEA1',
    'Koln': 'DEA2',
    'Munster': 'DEA3',
    'Detmold': 'DEA4',
    'Arnsberg': 'DEA5',
    'Koblenz': 'DEB1',
    'Trier': 'DEB2',
    'Rheinhessen-Pfalz': 'DEB3',
    'Saarland': 'DEC0',
    'Dresden': 'DED2',
    'Chemnitz': 'DED4',
    'Leipzig': 'DED5',
    'Sachsen-Anhalt': 'DEE0',
    'Schleswig-Holstein': 'DEF0',
    'Thuringen': 'DEG0',
    'Piemonte': 'ITC1',
    'Lombardia': 'ITC4',
    'Trentino-Alto Adige': 'ITH2',
    'Veneto': 'ITH3',
    'Emilia-Romagna': 'ITH5',
    'Toscana': 'ITI1',
    'Umbria': 'ITI2',
    'Marche': 'ITI3',
    'Lazio': 'ITI4',
    'Luxembourg': 'LU00',
    'Groningen': 'NL11',
    'Friesland': 'NL12',
    'Overijssel': 'NL21',
    'Gelderland': 'NL22',
    'Flevoland': 'NL23',
    'Utrecht': 'NL31',
    'Noord-Holland': 'NL32',
    'Zuid-Holland': 'NL33',
    'Zeeland': 'NL34',
    'Noord-Brabant': 'NL41',
    'Limburg': 'NL42',
    'Greater Poland': 'PL41',
    'Lower Silesian': 'PL51',
    'Warmian-Masurian': 'PL62',
    'Pais Vasco': 'ES21',
    'Comunidad Foral de Navarra': 'ES22',
    'Castilla y Leon': 'ES41',
    'Cataluna': 'ES51',
    'Andalucia': 'ES61',
    'Ostergotland': 'SE123',
    'Jonkoping': 'SE211',
    'Kronoberg': 'SE212',
    'Kalmar': 'SE213',
    'Blekinge': 'SE221',
    'Skane': 'SE224',
    'Halland': 'SE231',
    'Vastra Gotaland': 'SE232',
    'Varmland': 'SE311',
    'Vaud': 'CH011',
    'Valais':  'CH012',
    'Geneve': 'CH013',
    'Bern': 'CH021',
    'Fribourg': 'CH022',
    'Solothurn': 'CH023',
    'Neuchatel': 'CH024',
    'Basel-Stadt': 'CH031',
    'Basel-Landschaft': 'CH032',
    'Aargau': 'CH033',
    'Zurich': 'CH040',
    'Glarus': 'CH051',
    'Schaffhausen': 'CH052',
    'Appenzell Ausserrhoden': 'CH053',
    'Appenzell Innerrhoden': 'CH054',
    'Sankt Gallen': 'CH055',
    'Graubunden': 'CH056',
    'Thurgau': 'CH057',
    'Lucerne': 'CH061',
    'Uri': 'CH062',
    'Schwyz': 'CH063',
    'Obwalden': 'CH064',
    'Nidwalden': 'CH065',
    'Ticino': 'CH070',
    'Zug': 'CH066',
    'Tees Valley and Durham': 'UKC1',
    'Northumberland and Tyne and Wear': 'UKC2',
    'Cumbria': 'UKD1',
    'Greater Manchester': 'UKD3',
    'Lancashire': 'UKD4',
    'Cheshire': 'UKD6',
    'East Yorkshire and Northern Lincolnshire': 'UKE1',
    'North Yorkshire': 'UKE2',
    'West Yorkshire': 'UKE4',
    'Derbyshire and Nottinghamshire': 'UKF1',
    'Leicestershire, Rutland and Northamptonshire': 'UKF2',
    'Lincolnshire': 'UKF3',
    'Herefordshire, Worcestershire and Warwickshire': 'UKG1',
    'Shropshire and Staffordshire': 'UKG2',
    'West Midlands': 'UKG3',
    'East Anglia': 'UKH1',
    'Bedfordshire and Hertfordshire': 'UKH2',
    'Essex': 'UKH3',
    'Outer London — West and North West': 'UKI7',
    'Berkshire, Buckinghamshire and Oxfordshire': 'UKJ1',
    'Surrey, East and West Sussex': 'UKJ2',
    'Hampshire and Isle of Wight': 'UKJ3',
    'Kent': 'UKJ4',
    'Gloucestershire, Wiltshire and Bristol/Bath area': 'UKK1',
    'Dorset and Somerset': 'UKK2',
    'Cornwall and Isles of Scilly': 'UKK3',
    'Devon': 'UKK4',
    'West Wales and The Valleys': 'UKL1',
    'East Wales': 'UKL2',
    'North Eastern Scotland': 'UKM5',
    'Highlands and Islands': 'UKM6',
    'Eastern Scotland': 'UKM7',
    'West Central Scotland': 'UKM8',
    'Southern Scotland': 'UKM9',
    'Northern Ireland': 'UKN0',
    'Estonia': 'EE00',
    'Finland': 'FI1',
    'Hungary': 'HU',
    'Norway': 'NO0',
    'Zealand': 'DK02',
    'Southern Denmark': 'DK03',
    'Central Jutland': 'DK04',
    'Northern and Western': 'IE04',
    'Southern': 'IE05',
    'Eastern and Midland': 'IE06',
    'Algarve': 'PT15'
}

trials['map_id'] = trials['new_region'].map(new_id_dict)
battles['map_id'] = battles['new_region'].map(new_id_dict)

def set_nuts(s):
    if len(str(s['map_id'])) == 5:
        return 3
    elif len(str(s['map_id'])) == 4:
        return 2
    elif len(str(s['map_id'])) == 3 and str(s['map_id']) != 'nan':
        return 1
    elif len(str(s['map_id'])) == 2:
        return 0
    else:
        return s['map_id']

trials['nuts_level'] = trials.apply(set_nuts, axis=1)
battles['nuts_level'] = battles.apply(set_nuts, axis=1)

trials['cntr_code'] = trials['map_id'].str[:2]
battles['cntr_code'] = battles['map_id'].str[:2]

def region_map(s):
    
    if s['country'] in ('Austria', 'Belgium', 'Czech Republic', 'Denmark', 'Germany', 'France', 'Netherlands', 'Sweden',
                        'Switzerland', 'United Kingdom', 'Italy', 'Poland', 'Spain', 'Luxembourg', 'Portugal'):
        return s['new_region']
    elif s['country'] in ('Estonia', 'Finland', 'Hungary', 'Ireland', 'Norway'):
        return 'Undefined Regions'
    else:
        return np.nan
    
trials['region_map'] = trials.apply(region_map, axis=1)


# Scattermap Data ************************************************************************************************************

# trials map

df_map_dec = nuts[['id', 'CNTR_CODE', 'LEVL_CODE', 'NAME_LATN', 'geometry']].set_index('id').join(
    trials[['map_id', 'decade', 'tried', 'executed']].groupby(
        ['map_id', 'decade']).agg('sum').reset_index().set_index('map_id')).reset_index()

nuts_dict = trials.set_index('cntr_code')['nuts_level'].dropna().to_dict()
nuts_dict.update(battles.set_index('cntr_code')['nuts_level'].dropna().to_dict())

df_map_dec['tried'] = df_map_dec['tried'].fillna(0)
df_map_dec['executed'] = df_map_dec['executed'].fillna(0)
df_map_dec['nuts_lvl'] = df_map_dec['CNTR_CODE'].map(nuts_dict).fillna(0).astype('int')
df_map_dec = df_map_dec[df_map_dec['decade'] == df_map_dec['decade']]

lon = []
lat = []

for i in df_map_dec['geometry']:
    lon.append(i.x)
    lat.append(i.y)
    
df_map_dec['lon'] = lon
df_map_dec['lat'] = lat

df_scatter = df_map_dec[['decade', 'CNTR_CODE', 'NAME_LATN', 'tried', 'executed', 'lat', 'lon']]
df_scatter[['decade', 'tried', 'executed']] = df_scatter[['decade', 'tried', 'executed']].astype('int')

df_scatter = df_scatter.rename(columns = {'NAME_LATN': 'place'})
df_scatter['min_decade'] = df_scatter.groupby('place')['decade'].transform('min')
df_scatter['max_decade'] = df_scatter.groupby('place')['decade'].transform('max')

df_scatter = df_scatter.set_index('decade').sort_index()

new_index = pd.DataFrame(dict(decade  = np.arange(1300, 1860, 10))).set_index('decade')

df_scatter = new_index.join(df_scatter)

df_scatter[['tried', 'executed']] = df_scatter[['tried', 'executed']].fillna(0)

df_scatter = df_scatter.reset_index().set_index(['decade', 'place'])

df_scatter['mortality'] = df_scatter['executed'] / df_scatter['tried']

country_dict = trials.set_index('cntr_code')['country'].to_dict()
df_scatter['country'] = df_scatter['CNTR_CODE'].map(country_dict)
df_scatter = df_scatter.drop('CNTR_CODE', axis=1)

# battles map

b_scatter = battles[['year', 'country', 'decade', 'city', 'lon', 'lat', 'war', 'battle']]

def battle_date(s):
    if not str(s['battle']) == 'nan':
        return s['battle'] + ', ' +str(int(s['year']))
    else:
        return np.nan
b_scatter['battle_date'] = b_scatter.apply(battle_date, axis=1)

b_scatter = b_scatter.drop_duplicates()

b_scatter['battle_num'] = b_scatter.sort_values(by = 'year').groupby(['decade', 'city']).cumcount()

b_scatter_piv = b_scatter.pivot(index = ['decade', 'city'], columns = 'battle_num', values = 'battle_date')
b_scatter_piv = b_scatter_piv.rename(columns = {0: 'battle_1', 1: 'battle_2', 2: 'battle_3'})

b_scatter = b_scatter.set_index(['decade', 'city']).join(b_scatter_piv[['battle_1', 'battle_2', 'battle_3']])

def battles_in_place(s):
    if str(s['battle_3']) !='nan':
        return str(s['battle_1']) + '<br>' + str(s['battle_2']) + '<br>' + str(s['battle_3'])
    elif str(s['battle_2']) !='nan':
        return str(s['battle_1']) + '<br>' + str(s['battle_2'])
    else:
        return str(s['battle_1'])
    
b_scatter['battles_in_place'] = b_scatter.apply(battles_in_place, axis=1)
b_scatter = b_scatter.drop(['battle_num', 'battle_date', 'battle_1', 'battle_2', 'battle_3', 'battle', 'year'], axis=1).drop_duplicates()
b_scatter = b_scatter.rename(columns = {'battles_in_place': 'battle'})

df_scatter['event'] = 'trial'
b_scatter['event'] = 'battle'

all_scatter = pd.concat([df_scatter, b_scatter]).sort_index()

def size_1(s): # calculate size of circles to compare their areas, not radiuses
    if s['tried'] == 0 or s['tried'] == np.nan:
        return 0
    else:
        return np.sqrt(s['tried']/3.141592653589793)
all_scatter['size_1'] = all_scatter.apply(size_1, axis=1)

new_dec = dict()
for i in all_scatter.index.levels[0].tolist():
    new_dec[i] = (str(i) + '–' + str(i+9))
    
all_scatter = all_scatter.reset_index()
all_scatter['decade_hov'] = all_scatter['decade'].map(new_dec)
all_scatter = all_scatter.set_index(['decade', 'place'])


# Scattermap Total Data ******************************************************************************************************

# trials map

df_map_dec = nuts[['id', 'CNTR_CODE', 'LEVL_CODE', 'NAME_LATN', 'geometry']].set_index('id').join(
    trials[['map_id', 'decade', 'tried', 'executed']].groupby(
        ['map_id', 'decade']).agg('sum').reset_index().set_index('map_id')).reset_index()

nuts_dict = trials.set_index('cntr_code')['nuts_level'].dropna().to_dict()
nuts_dict.update(battles.set_index('cntr_code')['nuts_level'].dropna().to_dict())

df_map_dec['tried'] = df_map_dec['tried'].fillna(0)
df_map_dec['executed'] = df_map_dec['executed'].fillna(0)
df_map_dec['nuts_lvl'] = df_map_dec['CNTR_CODE'].map(nuts_dict).fillna(0).astype('int')
df_map_dec = df_map_dec[df_map_dec['decade'] == df_map_dec['decade']]

lon = []
lat = []

for i in df_map_dec['geometry']:
    lon.append(i.x)
    lat.append(i.y)
    
df_map_dec['lon'] = lon
df_map_dec['lat'] = lat

df_scatter_1 = df_map_dec[['decade', 'CNTR_CODE', 'NAME_LATN', 'lat', 'lon']]
df_scatter_2 = df_map_dec[['NAME_LATN', 'tried', 'executed']]
df_scatter_1['decade'] = df_scatter_1['decade'].astype('int')
df_scatter_2[['tried', 'executed']] = df_scatter_2[['tried', 'executed']].astype('int')

df_scatter_1 = df_scatter_1.rename(columns = {'NAME_LATN': 'place'})
df_scatter_2 = df_scatter_2.rename(columns = {'NAME_LATN': 'place'})

df_scatter_1['min_decade'] = df_scatter_1.groupby('place')['decade'].transform('min')
df_scatter_1['max_decade'] = df_scatter_1.groupby('place')['decade'].transform('max')
df_scatter_1 = df_scatter_1.drop('decade', axis=1)

df_scatter_1 = df_scatter_1.groupby('place').agg('max')
df_scatter_2 = df_scatter_2.groupby('place').agg('sum')[['tried', 'executed']]

df_scatter_total = df_scatter_1.join(df_scatter_2)

df_scatter_total['mortality'] = df_scatter_total['executed'] / df_scatter_total['tried']

country_dict = trials.set_index('cntr_code')['country'].to_dict()
df_scatter_total['country'] = df_scatter_total['CNTR_CODE'].map(country_dict)
df_scatter_total = df_scatter_total.drop('CNTR_CODE', axis=1)

# battles map

b_scatter_total = battles[['year', 'country', 'decade', 'city', 'lon', 'lat', 'war', 'battle']]

def battle_date(s):
    if not str(s['battle']) == 'nan':
        return s['battle'] + ', ' + str(int(s['year'])) + ' | ' + str(s['war'])
    else:
        return np.nan
b_scatter_total['battle_date'] = b_scatter_total.apply(battle_date, axis=1)

b_scatter_total = b_scatter_total.drop_duplicates()
b_scatter_total = b_scatter_total.rename(columns = {'city': 'place'})

b_scatter_total['battle_num'] = b_scatter_total.sort_values(by = 'year').groupby('place').cumcount()

b_scatter_total_piv = b_scatter_total.pivot(index = 'place', columns = 'battle_num', values = 'battle_date')
b_scatter_total_piv = b_scatter_total_piv.rename(columns = {0: 'battle_1', 1: 'battle_2', 2: 'battle_3', 3: 'battle_4'})

b_scatter_total = b_scatter_total.set_index('place').join(b_scatter_total_piv[['battle_1', 'battle_2', 'battle_3', 'battle_4']])

def battles_in_place(s):
    if str(s['battle_4']) !='nan':
        return str(s['battle_1']) + '<br>' + str(s['battle_2']) + '<br>' + str(s['battle_3']) + '<br>' + str(s['battle_4'])
    elif str(s['battle_3']) !='nan':
        return str(s['battle_1']) + '<br>' + str(s['battle_2']) + '<br>' + str(s['battle_3'])
    elif str(s['battle_2']) !='nan':
        return str(s['battle_1']) + '<br>' + str(s['battle_2'])
    else:
        return str(s['battle_1'])
    
b_scatter_total['battles_in_place'] = b_scatter_total.apply(battles_in_place, axis=1)
b_scatter_total = b_scatter_total.drop(['battle_num', 'battle_date', 'battle_1', 'battle_2', 'battle_3', 'battle_4', 'battle', 'year', 'war'], axis=1).drop_duplicates()
b_scatter_total = b_scatter_total.rename(columns = {'battles_in_place': 'battle'})

df_scatter_total['event'] = 'trial'
b_scatter_total['event'] = 'battle'

all_scatter_total = pd.concat([df_scatter_total, b_scatter_total]).sort_index()

def size(s): # calculate size of circles to compare their areas, not radiuses
    if s['tried'] == 0 or s['tried'] == np.nan:
        return 0
    else:
        return np.sqrt(s['tried']/3.141592653589793)
all_scatter_total['size'] = all_scatter_total.apply(size, axis=1)


# Scatter Data ***************************************************************************************************************

# cross joining the countries and all the decades between 1300 and 1850, to include missing time slots:
a = np.arange(1300, 1860, 10)
b = trials['country'].sort_values().unique()
c = 0
index_df = pd.melt(pd.DataFrame(data=c, index=a, columns=b).reset_index().rename(columns = {'index':'decade'}),
                   id_vars = 'decade', var_name = 'country') 

trials_by_decade = trials[['decade', 'tried', 'executed']].groupby('decade').agg('sum').reset_index()
battles_by_decade = battles[['decade', 'battle']].groupby('decade').agg('count').reset_index()
trials_by_country = trials[['country', 'tried', 'executed']].groupby('country').agg('sum').reset_index().sort_values(by='tried')

trials_by_decade_and_country = trials[['country', 'decade', 'tried', 'executed']].groupby(
    ['country', 'decade']).agg('sum').reset_index()

# columns to sort - by the decade of the first trial, than by the maximum number of people tried:
trials_by_decade_and_country['min_decade'] = trials_by_decade_and_country.groupby('country')['decade'].transform('min')
trials_by_decade_and_country['max_tried'] = trials_by_decade_and_country.groupby('country')['tried'].transform('sum')

# joining everything
trials_by_decade_and_country = index_df.drop('value', axis=1).set_index(['decade', 'country']).join(
    trials_by_decade_and_country[['tried', 'executed', 'decade', 'country']].set_index(['decade', 'country']),
    how = 'left').reset_index().set_index('country').join(
    trials_by_decade_and_country[['min_decade', 'max_tried', 'country']].drop_duplicates().set_index('country'),
    how = 'left').reset_index().set_index(['decade', 'country'])

battles_by_decade_and_country = battles[['decade', 'country', 'battle']].groupby(['decade', 'country']).agg('count')

trials_by_decade_and_country_app = trials_by_decade_and_country.join(battles_by_decade_and_country).reset_index()

trials_by_decade_and_country_app[['tried', 'executed', 'battle']] = trials_by_decade_and_country_app[[
    'tried', 'executed', 'battle']].fillna(0)
trials_by_decade_and_country_app = trials_by_decade_and_country_app.sort_values(by = ['min_decade', 'max_tried'],
                                                                                ascending = [False, True])

trials_by_decade_and_country_app = trials_by_decade_and_country_app.sort_values(
    by = ['min_decade', 'max_tried'], ascending = [False, True])

# extra lines between the countries and the total
new_row_1 = {'decade': np.nan, 'country': 'line_1', 'tried': 0, 'executed': np.nan, 'min_decade': 1300,
             'max_tried': 5000, 'battle': np.nan}
new_row_2 = {'decade': np.nan, 'country': 'line_2', 'tried': 0, 'executed': np.nan, 'min_decade': 1300,
             'max_tried': 5100, 'battle': np.nan}
new_row_3 = []
decades = np.arange(1300, 1860, 10)
for i in decades:
    r = {'decade': i, 'country': 'Decade', 'tried': 0, 'executed': np.nan, 'min_decade': 1300,
         'max_tried': 5200, 'battle': np.nan, 'decade_t': str(i)+'s'}
    new_row_3.append(r)
new_row_4 = {'decade': np.nan, 'country': 'line_3', 'tried': 0, 'executed': np.nan, 'min_decade': 1300,
             'max_tried': 5300, 'battle': np.nan}
new_row_5 = {'decade': np.nan, 'country': 'line_4', 'tried': 0, 'executed': np.nan, 'min_decade': 1300,
             'max_tried': 5400, 'battle': np.nan}

# extra lines below
new_row_6 = {'decade': np.nan, 'country': 'line_5', 'tried': 0, 'executed': np.nan, 'min_decade': 2000,
             'max_tried': 0, 'battle': np.nan}

new_row_7 = {'decade': np.nan, 'country': 'line_6', 'tried': 0, 'executed': np.nan, 'min_decade': 2000,
             'max_tried': 0, 'battle': np.nan}

trials_by_decade_and_country_app = trials_by_decade_and_country_app.append([new_row_1, new_row_2,
                                                                            new_row_4, new_row_5,
                                                                            new_row_6, new_row_7], ignore_index=True)
trials_by_decade_and_country_app = trials_by_decade_and_country_app.append(new_row_3, ignore_index=True)

# adding totals for countries and for decades
trials_net_1 = pd.concat([trials_by_decade_and_country_app, pd.DataFrame(np.arange(1300, 1860, 10), 
                                                                         columns = ['decade']).set_index('decade').join(
    trials_by_decade.set_index('decade')).fillna(0).join(
    battles_by_decade.set_index('decade')).fillna(0).reset_index()])

trials_net_1['country'] = trials_net_1['country'].fillna('Europe')
trials_net_1['min_decade'] = trials_net_1['min_decade'].fillna(1300)
trials_net_1['max_tried'] = trials_net_1['max_tried'].fillna(16007)

trials_net = pd.concat([trials_net_1, trials_by_country.set_index('country').join(
    battles[['country', 'battle']].groupby('country').agg('count')).reset_index()])

trials_net['decade'] = trials_net['decade'].fillna(1900)
trials_net['min_decade'] = trials_net['min_decade'].fillna(2000)
trials_net['mortality'] = trials_net['executed'] / trials_net['tried']

trials_net = trials_net.reset_index(drop=True)

trials_net['country'] = trials_net['country'].replace('United Kingdom', 'UK')
trials_net['country'] = trials_net['country'].replace('Czech Republic', 'Czechia')

# size of the outer circles - recount to area from radius
def size_1(s):
    if s['tried'] == 0 or s['tried'] == np.nan:
        return 0
    else:
        return np.sqrt(s['tried']/3.141592653589793)
trials_net['size_1'] = trials_net.apply(size_1, axis=1)

# size of the inner circles
def size_2(s):
    if s['tried'] == 0 or s['tried'] == np.nan:
        return 0
    else:
        return 1.5
trials_net['size_2'] = trials_net.apply(size_2, axis=1)

trials_net['decade'] = trials_net['decade'].astype('int')

# marker text for totals
def text_country(s):
    if s['decade'] == 1900 and s['country'] not in ('line_1', 'line_2', 'line_3', 'line_4', 'line_5', 'line_6', 'Decade'):
        return s['tried']
    else:
        return np.nan

def text_decade(s):
    if s['country'] == 'Europe':
        return s['tried']
    else:
        return np.nan

# hovertext
def decade_hov(s):
    if s['tried'] == 0:
        return np.nan
    else: return s['decade']
    
def decade_name_hov(s):
    if s['tried'] == 0:
        return np.nan
    elif s['decade'] == 1900:
        return 'Europe'
    else: return str(s['decade'])+'–'+str(s['decade']+9)
    
def country_hov(s):
    if s['tried'] == 0:
        return np.nan
    else: return s['country']
    
def tried_hov(s):
    if s['tried'] == 0:
        return np.nan
    else: return s['tried']

def executed_hov(s):
    if s['tried'] == 0:
        return np.nan
    else: return s['executed']
    
def mortal_hov(s):
    if s['tried'] == 0:
        return np.nan
    else: return s['mortality']

trials_net['text_country'] = trials_net.apply(text_country, axis=1)
trials_net['text_country'] = trials_net['text_country'].apply(lambda x: "{:,.0f}".format(x)+' ').replace('nan ', np.nan)

trials_net['text_decade'] = trials_net.apply(text_decade, axis=1)
trials_net['text_decade'] = trials_net['text_decade'].apply(lambda x: "{:,.0f}".format(x)+' ').replace('nan ', np.nan)

trials_net['decade_hov'] = trials_net.apply(decade_hov, axis=1)
trials_net['decade_name_hov'] = trials_net.apply(decade_name_hov, axis=1)
trials_net['country_hov'] = trials_net.apply(country_hov, axis=1)
trials_net['tried_hov'] = trials_net.apply(tried_hov, axis=1)
trials_net['executed_hov'] = trials_net.apply(executed_hov, axis=1)
trials_net['mortal_hov'] = trials_net.apply(mortal_hov, axis=1)

trials_net = trials_net.sort_values(by = ['min_decade', 'max_tried'], ascending = [False, True])


# Treemap Data ***************************************************************************************************************

# For structure to be mapped correctly, we need to count the trials which doesn't apply to any region (the "undefigned"
# regions) for each country, and those that doesn't apply to any city (the "undefigned" settlements) for each region.

# regional level 

treemap_df = trials.groupby(['country', 'region_map']).agg('sum')[['tried', 'executed']].reset_index()

treemap_df_other = treemap_df[['country', 'tried', 'executed']].groupby('country').agg('sum').join(
    trials[['country', 'tried', 'executed']].groupby('country').agg('sum'), rsuffix='_all')
treemap_df_other['tried_other'] = treemap_df_other['tried_all']-treemap_df_other['tried']
treemap_df_other['executed_other'] = treemap_df_other['executed_all']-treemap_df_other['executed']
treemap_df_other['region_map'] = 'Undefined Regions'
treemap_df_other = treemap_df_other.reset_index()[['country', 'region_map', 'tried_other', 'executed_other']].rename(
    columns = {'tried_other': 'tried', 'executed_other': 'executed'})

treemap_df_other = treemap_df_other[treemap_df_other['tried'] > 0]

treemap_df = pd.concat([treemap_df, treemap_df_other], axis=0)

# settlements level

treemap_df_city = trials.groupby(['country', 'region_map', 'city']).agg('sum')[['tried', 'executed']].reset_index()

treemap_df_city_other = treemap_df.set_index(['country', 'region_map']).join(
    treemap_df_city.groupby(['country', 'region_map']).agg('sum'), how='left', lsuffix='_all')
treemap_df_city_other[['tried', 'executed']] = treemap_df_city_other[['tried', 'executed']].fillna(0)
treemap_df_city_other['tried_other'] = treemap_df_city_other['tried_all'] - treemap_df_city_other['tried']
treemap_df_city_other['executed_other'] = treemap_df_city_other['executed_all'] - treemap_df_city_other['executed']
treemap_df_city_other['city'] = 'Undefigned Settlements'

treemap_df_city_other = treemap_df_city_other.reset_index()[['country',
                                                             'region_map',
                                                             'city',
                                                             'tried_other',
                                                             'executed_other']].rename(columns = {'tried_other': 'tried',
                                                                                                  'executed_other': 'executed'})

treemap_df_city_other = treemap_df_city_other[treemap_df_city_other['tried'] > 0]
treemap = pd.concat([treemap_df_city, treemap_df_city_other], axis=0)

# more indicators

treemap['mortality'] = treemap['executed'] / treemap['tried']
treemap['perc_of_total'] = treemap['executed'] / trials['executed'].sum()

# fixing duplicated "parents" and "children" for plotly

treemap['region_map'] = treemap['region_map'].replace('Luxembourg', 'Luxembourg (region)')
treemap['city'] = treemap['city'].replace('Luxembourg', 'Luxembourg (city)')


# Saving the datasets ********************************************************************************************************

all_scatter.to_csv('data_scattermapbox.csv')
all_scatter_total.to_csv('data_scattermapbox_total.csv')
trials_net.to_csv('data_scattertimeline.csv')
treemap.to_csv('data_treemap.csv')