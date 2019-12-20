import requests, time, pandas, json

# Variables
REGION = 'na1'
TFTREGION = 'americas'
APIKEY = 'RGAPI-9d7722ed-75f7-43a7-be7a-0b99073323ac'
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
        URL = 'https://'+ REGION +'.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + APIKEY
        response = requests.get(URL)
        return response.json()['name']

class Match:
    def __init__(self, Summoner):
        if type(Summoner) == list:
           for x in Summoner:
               self.matchhistory = self.getmatchhistory(x.puuid)
        else:
            self.matchhistory = self.getmatchhistory(Summoner.puuid)
        self.matchdetails = self.getmatchdetails(self.matchhistory)
    
    def getmatchhistory(self, puuid):
        URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=' + MATCHES + '&api_key=' + APIKEY
        response = requests.get(URL)
        return response.json()

    def getmatchdetails(self, matchid):
        for match in matchid:
            URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + APIKEY
            response = requests.get(URL)
            return response.json()

def main():

    a_summoner = Summoner('Bloodvault')
    #print(a_summoner.puuid)
    #print(Match(a_summoner).matchhistory)
    #print(Match(a_summoner).matchdetails)

    #Format details as JSON
    #data = Match(a_summoner).matchdetails
    #values = [{'match_details': k, 'unit_details': v} for k, v in data.items()]
    #print(json.dumps(values, indent=4))

    #Working with pandas data frames to store the match info
    data = Match(a_summoner).matchdetails['info']
    df = pandas.DataFrame.from_dict(data=data).T
    print(df)

if __name__ == '__main__':
    main()