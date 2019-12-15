import requests, time

# Variables
REGION = 'na1'
TFTREGION = 'americas'
APIKEY = 'RGAPI-9e42a420-48a8-4658-a50b-569bd106691c'

# Class 
class Summoner:
    def __init__(self, name):
        if len(name) < 40:
            URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + name + '?api_key=' + APIKEY
        else:
            URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + name + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.id = response.json()['id']
        self.puuid = response.json()['puuid']
        self.accountid = response.json()['accountId']
        self.name = response.json()['name']

class Match:
    def __init__(self, summoner):
        self.summoner = summoner
        ID = self.summoner.puuid
        self.history = requestTFTMatchHistory(ID, TFTREGION, APIKEY, Match.matches)
        self.details = requestMatchDetails(self.history, TFTREGION, APIKEY)
        self.game_datetime = self.details['info']['game_datetime']
        self.game_version = self.details['info']['game_version']
        self.match_id = self.details['metadata']['match_id']
        self.match_participants = self.details['metadata']['participants']


def requestSummonerData(REGION, summonerName, APIKEY):
    URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + summonerName + '?api_key=' + APIKEY
    response = requests.get(URL)
    return response.json()
def requestTFTMatchHistory(ID, TFTREGION, APIKEY, matches):
    URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/by-puuid/' + ID + '/ids?count=' + matches + '&api_key=' + APIKEY
    response = requests.get(URL)
    return response.json()
def requestTFTSummonerData(ID, REGION, APIKEY, playerlist, uniqueplayerlist):
    URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + ID + '?api_key=' + APIKEY
    response = requests.get(URL)
    return response.json()
def requestMatchDetails(matchID, TFTREGION, APIKEY):
    for match in matchID:
        URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + APIKEY
        response = requests.get(URL)
        return response.json()


def main():
    #Set static values for just me
    Match.matches = '2'
    a_summoner = Summoner('Bloodvault')


    Match(a_summoner)
    print(a_summoner.name)
    print(Match(a_summoner).history)
    #print(Match(a_summoner).history[1])
    #print(Match(a_summoner).game_datetime)
    
    #This will be for grabbing people's units
    #print(Match(a_summoner).details['info']['participants'])

    print(Match(a_summoner).match_participants)
    #print(Match(a_summoner).details['metadata'])

    for person in Match(a_summoner).match_participants:
        b_summoner = Summoner(person)
        print(b_summoner.name)
if __name__ == '__main__':
    main()