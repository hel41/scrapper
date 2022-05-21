
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_json("einsatzzahlen.json")

time = []
RD = []
BB = []
TH =[]

#Umwandlung des DAtaframes in eine Liste
list = (df[0].to_list())
 
for i in list:
    
    a_json_format = i.replace("'", "\"")
    b = json.loads(a_json_format)
    #zeitstempel in DateTime Format
    #datetime.strptime('24.02.2022 13:29',"%d.%m.%Y %H:%M")
    time.append(datetime.strptime(b['zeitstempel'],"%d.%m.%Y %H:%M"))
    RD.append(int(b['werte'][2]['Rettungsdienst']))
    BB.append(int(b['werte'][0]['Brandbekämpfung']))
    TH.append(int(b['werte'][1]['Technische Hilfeleistung']))
    
daten = {"Time":time, "Rettungsdienst":RD, "Brandbekämpfung": BB, "Tech. Hilfeleistung":TH}

table = pd.DataFrame(daten)
#table.plot(x = 'Time',y = ['Rettungsdienst','Brandbekämpfung','Tech. Hilfeleistung'])
table.plot( x='Time', y= ['Rettungsdienst','Brandbekämpfung','Tech. Hilfeleistung'])
plt.grid()
plt.legend()
plt.show()


