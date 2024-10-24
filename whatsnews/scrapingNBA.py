from pprint import pprint

import requests
from bs4 import BeautifulSoup

nba_teams = {
    "ATL": "Hawks",
    "BOS": "Celtics",
    "BKN": "Nets",
    "CHA": "Hornets",
    "CHI": "Bulls",
    "CLE": "Cavaliers",
    "DAL": "Mavericks",
    "DEN": "Nuggets",
    "DET": "Pistons",
    "GS": "Warriors",  # Sigla conforme a ESPN
    "HOU": "Rockets",
    "IND": "Pacers",
    "LAC": "Clippers",
    "LAL": "Lakers",
    "MEM": "Grizzlies",
    "MIA": "Heat",
    "MIL": "Bucks",
    "MIN": "Timberwolves",
    "NO": "Pelicans",
    "NY": "Knicks",  # Sigla conforme a ESPN
    "OKC": "Thunder",
    "ORL": "Magic",
    "PHI": "76ers",
    "PHX": "Suns",
    "POR": "Trail Blazers",
    "SAC": "Kings",
    "SAS": "Spurs",
    "TOR": "Raptors",
    "UTAH": "Jazz",
    "WSH": "Wizards",  # Sigla conforme a ESPN
}


class Scrap:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }

    def __init__(self, data: str):
        self.data = data
        self.url = f"https://www.espn.com.br/nba/calendario/_/data/{data}"

    def getHtml(self):
        response = requests.get(url=self.url, headers=self.headers)
        self.html = response.text

    def getGames(self):
        self.getHtml()
        soup = BeautifulSoup(self.html, "html.parser")

        # Extrai o título
        events = soup.find_all("div", class_="mt3")
        day = events[1] if len(events) > 1 else None

        if day:
            title_element = day.find("div", class_="Table__Title")
            self.title = (
                title_element.text.strip() if title_element else "Título não encontrado"
            )
        else:
            print("Eventos do dia não encontrados")

        # Seleciona o contêiner da tabela
        table = soup.find("div", class_="Table__Scroller")
        if not table:
            print("Tabela não encontrada")
            return

        # Extrai as linhas da tabela
        rows = table.find_all("tr", class_="Table__TR Table__TR--sm Table__even")
        self.games = []

        for row in rows:
            matchup = row.find("td", class_="events__col").get_text(strip=True)
            location = row.find("td", class_="colspan__col").get_text(strip=True)
            result = row.find("td", class_="teams__col").get_text(strip=True)

            if result != "Cancelado":
                teams = result.split(",")
                siglaTeam1, pointsTeam1 = teams[0].split(" ")
                siglaTeam2, pointsTeam2 = teams[1][1:].split(" ", 1)
                team1 = nba_teams[siglaTeam1]
                team2 = nba_teams[siglaTeam2]
                if pointsTeam1 > pointsTeam2:
                    result = (
                        f"{team1} : {pointsTeam1}Pts \n{team2} : {pointsTeam2}Pts\n"
                    )
                else:
                    result = (
                        f"{team2} : {pointsTeam2}Pts \n{team1} : {pointsTeam1}Pts\n"
                    )
            self.games.append(
                {
                    "Partida": f"{matchup} - {location.replace('em','')}\n",
                    "Resultado": result,
                }
            )


if __name__ == "__main__":
    s = Scrap("20241022")
    s.getGames()
    print(s.title)
    for game in s.games:
        for i in game:
            print(game[i])
        print()
