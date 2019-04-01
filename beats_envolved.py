import requests
import ast 
import codecs
from datetime import datetime

enemy_list = [[], [], []]
which = 0
temp = []
fp = codecs.open('紀錄.txt', 'r', encoding='UTF-8')
for i in fp.readlines():
    i = i.encode('utf-8').decode('utf-8-sig').strip()
    if '===' in i:
        break
    if '' == i:
        continue
    elif i == '[SERVER1]':
        which = 0
    elif i == '[SERVER2]':
        which = 1
    elif i == '[SERVER3]':
        which = 2
    else:
        a = i.find(',')
        enemy_list[which].append(int(i[0: a-1]))
        
for i in enemy_list:
    i.sort()

enemy_info_list = [[], [], []]
for server, enemies in enumerate(enemy_list):
    url = 'http://mstore.r2games.com/?ac=getRole&gameid=377&os=android&server=' + str(server+1) + '&roleid='
    for enemy in enemies:
        temp = {}
        res = requests.get(url+str(enemy))
        r = res.text.replace('false', 'False')
        r = r.replace('true', 'True')
        r = ast.literal_eval(r)
        if r['state'] == False:
            #print(i, ",", res.text)
            continue
        temp['id'] = r['data'][0]['roleid']
        temp['name'] = r['data'][0]['character']
        temp['level'] = r['data'][0]['level']
        temp['diamond'] = r['data'][0]['remaincoin']
        temp['create'] = datetime.fromtimestamp(r['data'][0]['createtime'])
        temp['last'] = datetime.fromtimestamp(r['data'][0]['lastlogintime'])
        enemy_info_list[server].append(temp)
        
server_list = ['覺醒之巔', '起源之地', 'Loveshack']
for s, enemies in enumerate(enemy_info_list):
    server = "S" + str(s+1) + " " + server_list[s]
    for l in enemies:
        print('=SPLIT("', server, ',', l['name'], ',', l['level'], ',', l['id'], ',', l['diamond'], ',', l['last'], ',', l['create'], '", ",")')