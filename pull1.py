import requests, time, pandas, json, datetime, pytz
from pandas.io.json import json_normalize

# Variables
REGION = 'na1'
TFTREGION = 'americas'
APIKEY = 'RGAPI-9c8101d2-d38d-49ff-a96a-7a4500588ebd'
MATCHES = '1'
# Class 
class Summoner:
    def __init__(self, name):
        if type(name) == list:
            for name in name:
                self.getpuuid(name)
        elif len(name) < 17:
            self.getpuuid(name)
        else:
            self.getname(name)

    def getpuuid(self, name):
        URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + name + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.puuid = response.json()['puuid']

    def getname(self, puuid):
        URL = 'https://'+ REGION +'.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + puuid + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.name = response.json()['name']

class Match:
    def __init__(self, Summoner):
        if type(Summoner) == list:
           for x in Summoner:
               self.matchhistory = self.getmatchhistory(x.puuid)
        else:
            self.matchhistory = self.getmatchhistory(Summoner.puuid)
        self.matchdetails = self.getmatchdetails(self.matchhistory)
        self.data = pandas.io.json.json_normalize(self.matchdetails)
        self.data_dict = self.data.to_dict()
    
    def getmatchhistory(self, puuid):
        URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=' + MATCHES + '&api_key=' + APIKEY
        response = requests.get(URL)
        return response.json()

    def getmatchdetails(self, matchid):
        for match in matchid:
            URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + APIKEY
            response = requests.get(URL)
            return response.json()
    
    def getfirstplace(self):
        for x in self.data_dict['info.participants'][0]:
            print(Summoner(x['puuid']).name + ' placed: ' + str(x['placement']))

    def getsetbuffs(self):
        z = 0
        for y in self.data_dict['metadata.participants'][0]:
            print(Summoner(y).name)
            print('<----------------->')
            print(self.data_dict['info.participants'][0][z]['traits'])
            print('<----------------->')
            z += 1

            

    def getitems(self):
        for x in self.data_dict['info.participants'][0][0]['units']:
            print(x['name'])
            for y in x['items']:
                with open('en_us_20191208.json') as json_file:
                    json_data = json.load(json_file)
                    json_data2 = pandas.io.json.json_normalize(json_data)
                    json_dict = json_data2.to_dict()
                for x in json_dict['items'][0]:
                    if y == x['id']:
                        print('---> ' + x['name'])


    def getmatchdate(self):
        ts = self.data_dict['info.game_datetime'][0]
        pacific = datetime.timedelta(hours=8)
        print((datetime.datetime.utcfromtimestamp(ts/1000) - pacific).strftime('%Y-%m-%d %H:%M:%S'))

def main():

    a_summoner = Summoner('Bloodvault')
    #print(Match.getitems(Match(a_summoner)))
    #print(Match.getmatchdate(Match(a_summoner)))
    print(Match.getsetbuffs(Match(a_summoner)))


if __name__ == '__main__':
    main()