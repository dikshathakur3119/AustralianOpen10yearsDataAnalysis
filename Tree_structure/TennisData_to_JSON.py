import pandas as pd
import numpy as np
import json


data = pd.read_excel('TennisTreeData.xlsx')

years = np.array(data['Year'].unique())
years.sort()


final = {"name":"Tennis", "children":[]}


def recrounds(name,round, year):
    thisplayer = {"name":name,"children":[]}

    #print(round)
    players = data.loc[(data['Year'] == year) & (data['Round'] == round-1) & (data['player1']==name)]
    p1, p2 = np.array(players['player1']), np.array(players.loc[:, 'player2'])

    if len(p1)!=0:
        #print(p1)
        p1 = str(p1[0])
        thisplayer["children"].append(recrounds(p1,round-1,year))

    if len(p2)!=0:
        #print(p2)
        p2 = str(p2[0])
        thisplayer["children"].append(recrounds(p2, round - 1, year))

    return thisplayer


for year in years:
    thisyear = {"name":str(year),"children":[]}

    round = 7
    players = data.loc[(data['Year']==year) & (data['Round']==round)]
    p1, p2 = np.array(players['player1']), np.array(players.loc[:,'player2'])
    p1 = str(p1[0])
    p2 = str(p2[0])

    #next round
    nextround = []
    for p in [p1,p2]:
        nextround.append(recrounds(p,round,year))

    thisyear["children"].append ({"name":p1,"children":nextround})

    final["children"].append(thisyear)

json = json.dumps(final)
f = open("flare.json","w")
f.write(json)
f.close()

