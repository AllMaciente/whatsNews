import os
import time as tm
from datetime import datetime, timedelta
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI

# Corrigido para importar do arquivo scrapingNBA.py
from .scrapingNBA import Scrap
from .sendMsg import CallMeBot

load_dotenv()


# * util functions
def dia_anterior():
    ontem = datetime.now() - timedelta(days=1)
    return ontem.strftime("%Y%m%d")


def genNBAMsg():
    msg = ""
    dia = dia_anterior()
    nba = Scrap(dia)
    nba.getGames()
    msg += nba.title + "\n" + "_" * len(nba.title) + "\n\n"
    for game in nba.games:
        for i in game:
            msg += game[i]
        msg += "\n"
    return msg


app = FastAPI()


@app.get("/sendmsg")
def sendNBA():
    bot = CallMeBot(os.getenv("TOKEN"), os.getenv("PHONE"))
    msg = genNBAMsg()
    bot.SendMsg(msg)
    return {"MSG": msg}
