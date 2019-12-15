import requests, time

# Variables
REGION = 'na1'
TFTREGION = 'americas'
APIKEY = 'RGAPI-9e42a420-48a8-4658-a50b-569bd106691c'
MATCHES = '2'
# Class 
class Summoner:
    def __init__(self, name):
        if len(name) < 17:
            URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + name + '?api_key=' + APIKEY
        else:
            URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + name + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.id = response.json()['id']
        self.puuid = response.json()['puuid']
        self.accountid = response.json()['accountId']
        self.name = response.json()['name']
        self.history = requestTFTMatchHistory(self.puuid, TFTREGION, APIKEY, MATCHES)

class MatchDetails:
    def __init__(self, match_ids):
        self.info = []
        for match_id in match_ids:
            self.info.append(requestMatchDetails(match_id, TFTREGION, APIKEY))
        self.match_participants = []
        for match in self.info:
            for participant in match['metadata']['participants']:
                self.match_participants.append(Summoner(participant).name)

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
    URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/' + matchID + '?api_key=' + APIKEY
    response = requests.get(URL)
    return response.json()


def main():
    #Set static values for just me
    a_summoner = Summoner('Bloodvault')


    #Match(a_summoner)
    #print(a_summoner.name)
    #print(Match(a_summoner).history)

    #print(Match(a_summoner).history[1])
    #print(Match(a_summoner).game_datetime)
    
    #This will be for grabbing people's units
    #print(Match(a_summoner).details['info']['participants'])

    print(MatchDetails(Summoner(a_summoner.name).history).match_participants)
    #print(Match(a_summoner).details['metadata'])

if __name__ == '__main__':
    main()