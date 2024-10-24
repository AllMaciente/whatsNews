import os

import requests
from dotenv import load_dotenv

load_dotenv()


class CallMeBot:
    def __init__(self, apikey, number):
        self.ApiKey = apikey
        self.Number = number

    def SendMsg(self, msg):
        url = f"https://api.callmebot.com/whatsapp.php?phone={self.Number}&text={msg.replace(' ','+')}&apikey={self.ApiKey}"
        print(url)
        requests.get(url)


if __name__ == "__main__":

    bot = CallMeBot(os.getenv("TOKEN"), os.getenv("PHONE"))
    bot.SendMsg("teste feito por min no vscode")
    print()
