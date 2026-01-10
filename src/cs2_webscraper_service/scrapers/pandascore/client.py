from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


class PandascoreClient:

    def __init__(self):
        self.base_url = "https://api.pandascore.co/"
        self.pandascore_auth_token = "AxVPy94ttMbp42PZsOnFjduTEUIkdi67_oc0VRJ1jLyEgO5KQGM"
        self.headers = {"Authorization": "Bearer " + self.pandascore_auth_token}

    def get_matches(self):
        r = requests.get(self.base_url + "csgo/matches", headers=self.headers)
        return r.json()

    def get_results(self):
        r = requests.get(self.base_url + " csgo/matches/past", headers=self.headers)
        return r.json()

    def get_teams(self):
        r = requests.get(self.base_url + 'csgo/teams', headers=self.headers)
        return r.json()

    # This seems to be a thing that we get strictly from HLTV, so we are going to have some work to do
    def get_team_rankings(self):
        r = requests.get(self.base_url + '')
        return ""

    def get_tournaments(self):
        r = requests.get(self.base_url + 'csgo/tournaments', headers=self.headers)
        return r.json()