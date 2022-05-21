
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
# Opening JSON file
f = open('einsatzzahlen.json')
data = json.load(f)
f.close()

Ts = []
Br = []
Th = []
Rd = []
for i in data :
    Ts.append(datetime.strptime(i['zeitstempel'], '%d.%m.%Y %H:%M'))
    Br.append(int(i['werte'][0]['Brandbekämpfung']))
    Th.append(int(i['werte'][1]['Technische Hilfeleistung']))
    Rd.append(int(i['werte'][2]['Rettungsdienst']))

# Dataframe modelieren 
df = pd.DataFrame({'Time':Ts,'Rettungsdienst':Rd, 'Brandbekämpfung':Br, 'Technische Hilfeleistung':Th})

# Sicherung als csv
df.to_csv('data_out.csv')

df.plot(x = 'Time',y = ['Rettungsdienst','Brandbekämpfung','Technische Hilfeleistung'])
plt.grid()
plt.legend()
plt.show()



