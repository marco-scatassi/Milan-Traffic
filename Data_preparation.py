import json
import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date, time



# ----- TRAFFICO -----


# Liste coi nomi delle vie delle due circonvallazioni

bastioni=['\Bastioni_Porta_Nuova_Viale_Crispi','\Bastioni_Porta_Venezia','\Bastioni_Porta_Volta','\Viale_Caldara',
          '\Viale_D_Annunzio','\Viale_D_Este','\Viale_di_Porta_Vercellina','\Viale_Filippetti','\Viale_Gian_Galeazzo',
          '\Viale_Margherita','\Viale_Monte_Santo','\Viale_Papiniano','\Viali_Maria_Majno']
navigli=['\Piazza_Castello','\Via_Carducci','\Via_De_Amicis','\Via_Delle_Armi','\Via_Fatebenefratelli','\Via_Pontaccio',
         '\Via_Santa_Sofia','\Via_Senato','\Via_Sforza','\Via_Tivoli','\Vie_Visconti_San_Damiano']


url_bastioni_flow = 'Traffic_Weather\Data\Data_Bastioni\Traffic'
url_navigli_flow = 'Traffic_Weather\Data\Data_Navigli\Traffic'

bastioni_dict_flow = {}
navigli_dict_flow = {}


# Apertura json

for street in bastioni:
    with open(url_bastioni_flow + street + '.json') as street_file:
        bastioni_dict_flow[street[1:]] = re.split(r'""+', street_file.read())

for street in navigli:
    with open(url_navigli_flow+street+'.json') as street_file:
        navigli_dict_flow[street[1:]] = re.split(r'""+', street_file.read())


# Il primo e l'ultimo elemento di ogni lista hanno un " di troppo: eliminiamolo

for street in bastioni:
     bastioni_dict_flow[street[1:]][0]=bastioni_dict_flow[street[1:]][0][1:]
     bastioni_dict_flow[street[1:]][-1]=bastioni_dict_flow[street[1:]][-1][:-1]

for street in navigli:
     navigli_dict_flow[street[1:]][0]=navigli_dict_flow[street[1:]][0][1:]
     navigli_dict_flow[street[1:]][-1]=navigli_dict_flow[street[1:]][-1][:-1]


# Dobbiamo rimpiazzare ' con " negli header per leggerli come json
for street in bastioni:
     l = len(bastioni_dict_flow[street[1:]])
     for i in range(int(l/2)):
         string = str(bastioni_dict_flow[street[1:]][2*i+1])
         string = re.sub(r"'", '"', string)
         bastioni_dict_flow[street[1:]][2*i+1] = string

for street in navigli:
     l = len(navigli_dict_flow[street[1:]])
     for i in range(int(l/2)):
         string = str(navigli_dict_flow[street[1:]][2*i+1])
         string = re.sub(r"'", '"', string)
         navigli_dict_flow[street[1:]][2*i+1] = string

# Inoltre tutti gli \ vanno eliminati
for street in bastioni:
  l = len(bastioni_dict_flow[street[1:]])
  for i in range(l):
    bastioni_dict_flow[street[1:]][i]=re.sub(r'\\', '',bastioni_dict_flow[street[1:]][i])

for street in navigli:
  l = len(navigli_dict_flow[street[1:]])
  for i in range(l):
    navigli_dict_flow[street[1:]][i]=re.sub(r'\\', '',navigli_dict_flow[street[1:]][i])

# Identifichiamo ed eliminiamo gli elementi contenenti il body di richieste non andate a buon fine
for street in bastioni:
    l = len(bastioni_dict_flow[street[1:]])
    for i in range(0,l,2):
      if('"currentSpeed"' not in bastioni_dict_flow[street[1:]][i]):
        print(street)
        print(bastioni_dict_flow[street[1:]][i])
        print(i)
        
for street in navigli:
    l = len(navigli_dict_flow[street[1:]])
    for i in range(0,l,2):
      if('"currentSpeed"' not in navigli_dict_flow[street[1:]][i]):
          print(street)
          print(navigli_dict_flow[street[1:]][i])
          print(i)

# \Via_Carducci
#upstream connect error or disconnect/reset before headers. reset reason: connection failure
#3322
# \Via_Sforza
#upstream connect error or disconnect/reset before headers. reset reason: connection failure
#3314

# Eliminiamo le richieste non andate a buon fine
del navigli_dict_flow['Via_Carducci'][3322]
del navigli_dict_flow['Via_Carducci'][3322]

del navigli_dict_flow['Via_Sforza'][3314]
del navigli_dict_flow['Via_Sforza'][3314]

# Ora possiamo leggere ogni elemento delle liste come json
bastioni_flow_json = {}
bastioni_date_json = {}

navigli_flow_json = {}
navigli_date_json = {}

for street in bastioni:
    l = len(bastioni_dict_flow[street[1:]])
    bastioni_flow_json[street[1:]] = []
    bastioni_date_json[street[1:]] = []
    for i in range(int(l/2)):
        bastioni_flow_json[street[1:]].append(json.loads(bastioni_dict_flow[street[1:]][2*i]))
        bastioni_date_json[street[1:]].append(json.loads(bastioni_dict_flow[street[1:]][2*i+1])['date'])

for street in navigli:
    l = len(navigli_dict_flow[street[1:]])
    navigli_flow_json[street[1:]] = []
    navigli_date_json[street[1:]] = []
    for i in range(int(l/2)):
        navigli_flow_json[street[1:]].append(json.loads(navigli_dict_flow[street[1:]][2*i]))
        navigli_date_json[street[1:]].append(json.loads(navigli_dict_flow[street[1:]][2*i+1])['date'])


# Associamo i json delle date ai json del traffico
for street in bastioni:
    l = len(bastioni_flow_json[street[1:]])
    for i in range(l):
        date_obj = datetime.strptime(bastioni_date_json[street[1:]][i], '%a, %d %b %Y %H:%M:%S %Z')
        date_obj = date_obj + timedelta(hours = 2)
        bastioni_flow_json[street[1:]][i]['date'] = pd.to_datetime(date_obj.timestamp(), unit = 's')

for street in navigli:
    l = len(navigli_flow_json[street[1:]])
    for i in range(l):
        date_obj = datetime.strptime(navigli_date_json[street[1:]][i], '%a, %d %b %Y %H:%M:%S %Z')
        date_obj = date_obj + timedelta(hours = 2)
        navigli_flow_json[street[1:]][i]['date'] = pd.to_datetime(date_obj.timestamp(), unit = 's')

# Verifica uguaglianze coordinate
for i in range(len(bastioni_flow_json['Bastioni_Porta_Nuova_Viale_Crispi'])-1):
  a1=bastioni_flow_json['Bastioni_Porta_Nuova_Viale_Crispi'][i]['flowSegmentData']['coordinates']['coordinate']
  a2=bastioni_flow_json['Bastioni_Porta_Nuova_Viale_Crispi'][i+1]['flowSegmentData']['coordinates']['coordinate']
  if a1!=a2:
    print('male male')



# Eliminiamo l'elemento @version e rimpiazziamo le coordinate geografiche con i nomi delle vie
for street in bastioni:
    l = len(bastioni_flow_json[street[1:]])
    for i in range(l):
        del bastioni_flow_json[street[1:]][i]['flowSegmentData']['@version']
        del bastioni_flow_json[street[1:]][i]['flowSegmentData']['coordinates']
        bastioni_flow_json[street[1:]][i]['street'] = street[1:]

for street in navigli:
    l = len(navigli_flow_json[street[1:]])
    for i in range(l):
        del navigli_flow_json[street[1:]][i]['flowSegmentData']['@version']
        del navigli_flow_json[street[1:]][i]['flowSegmentData']['coordinates']
        navigli_flow_json[street[1:]][i]['street'] = street[1:]



# ----- METEO -----

url_bastioni_weather = 'Traffic_Weather\Data\Data_Bastioni\Weather'
url_navigli_weather = 'Traffic_Weather\Data\Data_Navigli\Weather'

bastioni_dict_weather = {}
navigli_dict_weather = {}


# Apertura json
for street in bastioni:
    with open(url_bastioni_weather + street + '.json') as street_file:
        bastioni_dict_weather[street[1:]] = re.split(r'""+', street_file.read())

for street in navigli:
    with open(url_navigli_weather + street + '.json') as street_file:
        navigli_dict_weather[street[1:]] = re.split(r'""+', street_file.read())


# Il primo e l'ultimo elemento di ogni lista hanno un " di troppo: eliminiamolo
for street in bastioni:
     bastioni_dict_weather[street[1:]][0] = bastioni_dict_weather[street[1:]][0][1:]
     bastioni_dict_weather[street[1:]][-1] = bastioni_dict_weather[street[1:]][-1][:-1]

for street in navigli:
     navigli_dict_weather[street[1:]][0] = navigli_dict_weather[street[1:]][0][1:]
     navigli_dict_weather[street[1:]][-1] = navigli_dict_weather[street[1:]][-1][:-1]

# Dobbiamo rimpiazzare ' con " negli header per leggerli come json
for street in bastioni:
     l = len(bastioni_dict_weather[street[1:]])
     for i in range(int(l/2)):
         string = str(bastioni_dict_weather[street[1:]][2*i+1])
         string = re.sub(r"'", '"', string)
         bastioni_dict_weather[street[1:]][2*i+1] = string

for street in navigli:
     l = len(navigli_dict_weather[street[1:]])
     for i in range(int(l/2)):
         string = str(navigli_dict_weather[street[1:]][2*i+1])
         string = re.sub(r"'", '"', string)
         navigli_dict_weather[street[1:]][2*i+1] = string

# Inoltre tutti gli \ vanno eliminati
for street in bastioni:
  l = len(bastioni_dict_weather[street[1:]])
  for i in range(l):
    bastioni_dict_weather[street[1:]][i]=re.sub(r'\\', '',bastioni_dict_weather[street[1:]][i])

for street in navigli:
  l = len(navigli_dict_weather[street[1:]])
  for i in range(l):
    navigli_dict_weather[street[1:]][i]=re.sub(r'\\', '',navigli_dict_weather[street[1:]][i])

# Identifichiamo ed eliminiamo gli elementi contenenti il body di richieste non andate a buon fine
for street in bastioni:
    l = len(bastioni_dict_weather[street[1:]])
    for i in range(0,l,2):
      if('"cod":200' not in bastioni_dict_weather[street[1:]][i]):
        print(street)
        print(bastioni_dict_weather[street[1:]][i])
        print(i)
        
for street in navigli:
    l = len(navigli_dict_weather[street[1:]])
    for i in range(0,l,2):
      if('"cod":200' not in navigli_dict_weather[street[1:]][i]):
        print(street)
        print(navigli_dict_weather[street[1:]][i])
        print(i)

# Tutte le richieste sono andate a buon fine

# Ora possiamo leggere ogni elemento delle liste come json 
bastioni_weather_json = {}
navigli_weather_json = {}

for street in bastioni:
    l = len(bastioni_dict_weather[street[1:]])
    bastioni_weather_json[street[1:]] = []
    for i in range(0,l,2):
        bastioni_weather_json[street[1:]].append(json.loads(bastioni_dict_weather[street[1:]][i]))

for street in navigli:
    l = len(navigli_dict_weather[street[1:]])
    navigli_weather_json[street[1:]] = []
    for i in range(0,l,2):
        navigli_weather_json[street[1:]].append(json.loads(navigli_dict_weather[street[1:]][i]))


# Eliminiamo le coordinate geografiche (rimpiazzate dai nomi delle vie nei dati del traffico) e
# convertiamo l'attributo dt (tempo in Unix time) in data (con lo stesso formato della data nel traffico)

for street in bastioni:
    l = len(bastioni_weather_json[street[1:]])
    for i in range(l):
        bastioni_weather_json[street[1:]][i]['street'] = street[1:]
        del bastioni_weather_json[street[1:]][i]['coord']
        bastioni_weather_json[street[1:]][i]['lastUpdate'] = pd.to_datetime(bastioni_weather_json[street[1:]][i]['dt'], unit = 's') + timedelta(hours = 1)
        del bastioni_weather_json[street[1:]][i]['dt']
        bastioni_weather_json[street[1:]][i]['sys']['sunrise'] = pd.to_datetime(bastioni_weather_json[street[1:]][i]['sys']['sunrise'], unit = 's')
        bastioni_weather_json[street[1:]][i]['sys']['sunset'] = pd.to_datetime(bastioni_weather_json[street[1:]][i]['sys']['sunset'], unit = 's')
        bastioni_weather_json[street[1:]][i]['weather'] = bastioni_weather_json[street[1:]][i]['weather'][0]

for street in navigli:
    l = len(navigli_weather_json[street[1:]])
    for i in range(l):
        navigli_weather_json[street[1:]][i]['street'] = street[1:]
        del navigli_weather_json[street[1:]][i]['coord']
        navigli_weather_json[street[1:]][i]['lastUpdate'] = pd.to_datetime(navigli_weather_json[street[1:]][i]['dt'], unit = 's') + timedelta(hours = 1)
        del navigli_weather_json[street[1:]][i]['dt']
        navigli_weather_json[street[1:]][i]['sys']['sunrise'] = pd.to_datetime(navigli_weather_json[street[1:]][i]['sys']['sunrise'], unit = 's')
        navigli_weather_json[street[1:]][i]['sys']['sunset'] = pd.to_datetime(navigli_weather_json[street[1:]][i]['sys']['sunset'], unit = 's')
        navigli_weather_json[street[1:]][i]['weather'] = navigli_weather_json[street[1:]][i]['weather'][0]


# Per vedere un esempio dei json
'''
print('Struttura json del traffico (Bastioni):')
print(bastioni_flow_json['Bastioni_Porta_Nuova_Viale_Crispi'][0])
print('\n')
print('Struttura json del traffico (Navigli):')
print(navigli_flow_json['Piazza_Castello'][0])
print('\n')
print('Struttura json del meteo (Bastioni):')
print(bastioni_weather_json['Bastioni_Porta_Nuova_Viale_Crispi'][0])
print('\n')
print('Struttura json del meteo (Navigli):')
print(navigli_weather_json['Piazza_Castello'][0])
'''


# Adesso occupiamoci dell'integrazione tra traffico e meteo, partendo dal traffico


# Aggiungiamo come campo ai json la circonvallazione di appartenenza, poi uniamo le vie

for street in bastioni_flow_json:
  l = len(bastioni_flow_json[street])
  for i in range(l):
    bastioni_flow_json[street][i]['ringRoad'] = 'Bastioni'

for street in navigli_flow_json:
  l = len(navigli_flow_json[street])
  for i in range(l):
    navigli_flow_json[street][i]['ringRoad'] = 'Navigli'

flow_json = {**bastioni_flow_json, **navigli_flow_json} 


# 1. Cambiamo i valori del campo 'frc':
# FRC3: Strada secondaria
# FRC4: Strada di collegamento locale
#
# 2. Rinominiamo i campi frc e flowSegmentData in roadType e flowData
#
# 3. Aggiungiamo il campo 'LTZ', i.e. zona a traffico limitato:
# Navigli: Tutti i giorni, 20:00-7:00
# Bastioni: Lun-Ven, 7:30-19:30, esclusi festivi
# Tuttavia, la cerchia dei navigli è all'interno della cerchia dei bastioni.
# Pertanto, la ztl nei navigli è attiva anche quando lo è solo nei bastioni.
#
# 4. Aggiungiamo il campo 'flowConditions', i.e. condizioni generali del traffico.
# Ci basiamo sulla differenza percentuale tra la velocità di percorrenza senza 
# traffico (freeFlowSpeed) e la velocità di percorrenza attuale (currentSpeed).
# Scorrevole (Flowing): delta = 0-25%
# Moderato (Moderate): delta = 25-50%
# Congestionato (Congested): delta = 50-75%
# Bloccato (Blocked): delta = 75-100%

for street in flow_json:
  l = len(flow_json[street])
  for i in range(l):
    # 1.
    if(flow_json[street][i]['flowSegmentData']['frc'] == 'FRC3'):
        flow_json[street][i]['flowSegmentData']['frc'] = 'Secondary_Road'
    else:
        flow_json[street][i]['flowSegmentData']['frc'] = 'Local_Connecting_Road'
    # 2.
    flow_json[street][i]['roadType'] = flow_json[street][i]['flowSegmentData'].pop('frc')
    flow_json[street][i]['flowData'] = flow_json[street][i].pop('flowSegmentData')
    # 3.
    if flow_json[street][i]['ringRoad'] == 'Navigli':
      if(time(hour = 7, minute = 0) <= flow_json[street][i]['date'].time() <= time(hour = 20, minute = 0)):
        if(flow_json[street][i]['date'].date() == date(2022, 1, 1) or flow_json[street][i]['date'].date() == date(2022, 1, 2) or 
         flow_json[street][i]['date'].date() == date(2022, 1, 6) or flow_json[street][i]['date'].date() == date(2022, 1, 8) or 
         flow_json[street][i]['date'].date() == date(2022, 1, 9)):
          flow_json[street][i]['LTZ'] = False
        else:
          if(time(hour = 7, minute = 0) <= flow_json[street][i]['date'].time() < time(hour = 7, minute = 30) or
             time(hour = 19, minute = 30) <= flow_json[street][i]['date'].time() < time(hour = 20, minute = 0)):
            flow_json[street][i]['LTZ'] = False
          else:
            flow_json[street][i]['LTZ'] = True
      else:
          flow_json[street][i]['LTZ'] = True
    else:
      if(flow_json[street][i]['date'].date() == date(2022, 1, 1) or flow_json[street][i]['date'].date() == date(2022, 1, 2) or 
         flow_json[street][i]['date'].date() == date(2022, 1, 6) or flow_json[street][i]['date'].date() == date(2022, 1, 8) or 
         flow_json[street][i]['date'].date() == date(2022, 1, 9)):
         flow_json[street][i]['LTZ'] = False
      else:
        if(time(hour = 7, minute = 30) <= flow_json[street][i]['date'].time() <= time(hour = 19, minute = 30)):
          flow_json[street][i]['LTZ'] = True
        else:
          flow_json[street][i]['LTZ'] = False
    # 4.
    delta = flow_json[street][i]['flowData']['freeFlowSpeed'] - flow_json[street][i]['flowData']['currentSpeed']
    delta_perc = (delta/flow_json[street][i]['flowData']['freeFlowSpeed']) * 100
    if(delta_perc < 25):
      flow_json[street][i]['flowData']['flowConditions'] = 'Flowing'
    elif(25 <= delta_perc < 50):
      flow_json[street][i]['flowData']['flowConditions'] = 'Moderate'
    elif(50 <= delta_perc < 75):
      flow_json[street][i]['flowData']['flowConditions'] = 'Congested'
    else:
      flow_json[street][i]['flowData']['flowConditions'] = 'Blocked'


# Per vedere un esempio dei json

print('\n')
print('Struttura json del traffico:')
print(flow_json['Bastioni_Porta_Nuova_Viale_Crispi'][0])
print(flow_json['Piazza_Castello'][0])
print(flow_json['Bastioni_Porta_Nuova_Viale_Crispi'][-1])
print(flow_json['Piazza_Castello'][-1])



# Ora passiamo al meteo


# Aggiungiamo come campo ai json la circonvallazione di appartenenza, poi uniamo le vie
for street in bastioni_weather_json:
  l = len(bastioni_weather_json[street])
  for i in range(l):
    bastioni_weather_json[street][i]['ringRoad'] = 'Bastioni'

for street in navigli_weather_json:
  l = len(navigli_weather_json[street])
  for i in range(l):
    navigli_weather_json[street][i]['ringRoad'] = 'Navigli'

weather_json = {**bastioni_weather_json, **navigli_weather_json}


# Eliminiamo i campi ridondanti o irrilevanti e riorganizziamo il dizionario
for street in weather_json:
  l = len(weather_json[street])
  for i in range(l):
    weather_json[street][i]['temperature'] =  weather_json[street][i]['main']
    weather_json[street][i]['pressure'] =  weather_json[street][i]['temperature']['pressure']
    weather_json[street][i]['humidity'] =  weather_json[street][i]['temperature']['humidity']
    del  weather_json[street][i]['temperature']['pressure']
    del  weather_json[street][i]['temperature']['humidity']
    weather_json[street][i]['main'] =  weather_json[street][i]['weather']['main']
    del weather_json[street][i]['weather']
    del weather_json[street][i]['base']
    weather_json[street][i]['clouds'] = weather_json[street][i]['clouds']['all']
    weather_json[street][i]['sunrise'] =  weather_json[street][i]['sys']['sunrise']
    weather_json[street][i]['sunset'] =  weather_json[street][i]['sys']['sunset']
    del weather_json[street][i]['sys']
    del weather_json[street][i]['timezone'] 
    del weather_json[street][i]['id'] 
    del weather_json[street][i]['name'] 
    del weather_json[street][i]['cod']
    weather_json[street][i]['temperature']['feelsLike'] = weather_json[street][i]['temperature'].pop('feels_like')
    weather_json[street][i]['temperature']['tempMin'] = weather_json[street][i]['temperature'].pop('temp_min')
    weather_json[street][i]['temperature']['tempMax'] = weather_json[street][i]['temperature'].pop('temp_max')
   

# Per vedere un esempio dei json
print('\n')
print('Struttura json del meteo:')
print(weather_json['Bastioni_Porta_Nuova_Viale_Crispi'][0])
print(weather_json['Piazza_Castello'][0])
print(weather_json['Bastioni_Porta_Nuova_Viale_Crispi'][-1])
print(weather_json['Piazza_Castello'][-1])



# Ora dobbiamo integrare il dataset del traffico col dataset del meteo
final_json = {}


# Riorganizziamo i dati 
for street in flow_json:  
  l = len(flow_json[street])
  final_json[street] = []
  for i in range(l):
    date = flow_json[street][i]['date']
    ringRoad = flow_json[street][i]['ringRoad']
    roadType = flow_json[street][i]['roadType']
    LTZ = flow_json[street][i]['LTZ']
    traffic = flow_json[street][i]['flowData']
    final_json[street].append({'date': date, 'street': street, 'ringRoad': ringRoad, 'roadType': roadType, 'LTZ': LTZ, 'traffic': traffic})


# Assicuriamoci che le differenze tra le lunghezze di meteo e traffico siano minori di 8,
# in modo da definire in sicurezza un intorno di 16 record in cui ricercare 'lastUpdate'
for street in flow_json:
  if(len(flow_json[street]) - len(weather_json[street]) > 8):
    print('Intorno superato: '+ street)


# Aggiungiamo i dati del meteo in maniera sincronizzata:
# minimizziamo la differenza tra il campo 'lastUpdate' di weather_json e 'date' di final_json
for street in final_json:
  l1 = len(final_json[street])
  l2 = len(weather_json[street])
  for i in range(l1):
    optimal = abs(weather_json[street][0]['lastUpdate'] - final_json[street][i]['date']).total_seconds()
    optimal_index = 0
    # Ricerca del valore ottimo di 'lastUpdate' in un intorno di 16 record rispetto al traffico
    if(l1 - i <= 8):
      start = l1 - 16
      end = l1
    elif(i < 7):
      start = 0
      end = 16
    else:
      start = i - 8
      end = i + 8
    if(end >= l2):
      end = l2
    for j in range(start, end):
      delta = abs(weather_json[street][j]['lastUpdate'] - final_json[street][i]['date']).total_seconds()
      if (delta < optimal):
        optimal = delta
        optimal_index = j
    weather = {}
    weather['main'] = weather_json[street][optimal_index]['main']
    weather['clouds'] = weather_json[street][optimal_index]['clouds']
    weather['wind'] = weather_json[street][optimal_index]['wind']
    weather['temperature'] = weather_json[street][optimal_index]['temperature']
    weather['pressure'] = weather_json[street][optimal_index]['pressure']
    weather['humidity'] = weather_json[street][optimal_index]['humidity']
    weather['visibility'] = weather_json[street][optimal_index]['visibility']
    weather['sunrise'] = weather_json[street][optimal_index]['sunrise']
    weather['sunset'] = weather_json[street][optimal_index]['sunset']
    weather['lastUpdate'] = weather_json[street][optimal_index]['lastUpdate']
    final_json[street][i]['weather'] = weather

#---------------------------------------------------------------CSV---------------------------------------------------------------------
# creiamo una versione csv dei dati prima di completare la creazione dei json
json_csv={'csv':[]}
counter=0

for street in final_json:
  for i in range(len(final_json[street])):
    TrafficDate=final_json[street][i]['date']
    Street=final_json[street][i]['street']
    RingRoad=final_json[street][i]['ringRoad']
    LTZ=final_json[street][i]['LTZ']
    CurrentSpeed=final_json[street][i]['traffic']['currentSpeed']
    FreeFlowSpeed=final_json[street][i]['traffic']['freeFlowSpeed']
    RoadClosure=final_json[street][i]['traffic']['roadClosure']
    WeatherDate=final_json[street][i]['weather']['lastUpdate']
    Weather=final_json[street][i]['weather']['main']
    WindSpeed=final_json[street][i]['weather']['wind']['speed']
    WindDeg=final_json[street][i]['weather']['wind']['deg']
    Temperature=final_json[street][i]['weather']['temperature']['temp']
    Visibility=final_json[street][i]['weather']['visibility']
    json_csv['csv'].append({'ID':i+counter, 'IdealDate':'', 'TrafficDate':TrafficDate,'Street':Street,
                                'RingRoad':RingRoad,'LTZ':LTZ,'CurrentSpeed':CurrentSpeed,
                                'FreeFlowSpeed':FreeFlowSpeed,'RoadClosure':RoadClosure,
                                'Weather':Weather,'WindSpeed':WindSpeed,'WindDeg':WindDeg,
                                'Temperature':Temperature,'Visibility':Visibility,
                                'WeatherDate':WeatherDate})

  counter=counter+len(final_json[street])

# Spezziamo il campo date in data e ora in modo da agevolare le query sui dati
minutes = np.array([0, 10, 20, 30, 40, 50])

for street in flow_json:
  l = len(final_json[street])
  for i in range(l):
    dt = final_json[street][i]['date']
    dt2 = final_json[street][i]['weather']['lastUpdate']

    # Creiamo il campo datetime
    final_json[street][i]['dateTime'] = {}

    # Aggiungiamo le informazioni relative all'orario del traffico
    final_json[street][i]['dateTime']['trafficDate'] = datetime.strftime(dt, '%Y-%m-%d')
    final_json[street][i]['dateTime']['effectiveTrafficTime'] = datetime.strftime(dt, '%H:%M:%S')
    
    # Aggiungiamo le informazioni relative all'orario del meteo
    final_json[street][i]['dateTime']['weatherDate'] = datetime.strftime(dt2, '%Y-%m-%d')
    final_json[street][i]['dateTime']['effectiveWeatherTime'] = datetime.strftime(dt2, '%H:%M:%S')

    if minutes[abs(minutes-dt.minute).argmin()] == 0:
      final_json[street][i]['dateTime']['time'] = datetime.strftime(dt, '%H')+':'+str(minutes[abs(minutes-dt.minute).argmin()])+'0:00'
    else:
      final_json[street][i]['dateTime']['time'] = datetime.strftime(dt, '%H')+':'+str(minutes[abs(minutes-dt.minute).argmin()])+':00'

    # Eliminiamo i campi vecchi
    del final_json[street][i]['date']
    del final_json[street][i]['weather']['lastUpdate']

counter=0
for street in final_json:
  for i in range(len(final_json[street])):
    json_csv['csv'][i+counter]['IdealDate']=final_json[street][i]['dateTime']['trafficDate']+' '+final_json[street][i]['dateTime']['time']
  counter=counter+len(final_json[street])

# salviamo il csv
json_csv=pd.json_normalize(json_csv['csv'])
json_csv.to_csv('Traffic_Weather\DB.csv', index=False)

# Per vedere un esempio dei json
print('\n')
print('STRUTTURA FINALE:')
print(final_json['Bastioni_Porta_Nuova_Viale_Crispi'][0])
print(final_json['Bastioni_Porta_Nuova_Viale_Crispi'][-1])

# Salvataggio in json
for street in final_json:
  for i in range (len(final_json[street])):
    day = final_json[street][i]['dateTime']['trafficDate']
    hour = final_json[street][i]['dateTime']['time'][:2] + '_' + final_json[street][i]['dateTime']['time'][3:5]
    with open('Traffic_Weather/DB/' + street + '_' + day + '_' + hour + '.json', 'w') as f:
      jsonobj = json.dumps(final_json[street][i], indent = 4, default = str) 
      f.write(jsonobj)


# to view an example of json document
navigli_weather_json['Piazza_Castello'][0]
data=navigli_flow_json['Piazza_Castello'][0]['Date']

datetime.strftime(navigli_flow_json['Piazza_Castello'][2]['Date'], '%H:%M:%S')

