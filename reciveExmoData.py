import urllib.request
import json
import threading

def reciveJsonTickerData():
    threading.Timer(5.0, reciveJsonTickerData).start()
    with urllib.request.urlopen("https://api.exmo.com/v1.1/ticker") as url:
        tickerData = json.loads(url.read().decode())
        currency_pair = []
        with open('config.json', 'r', encoding='utf-8') as f:
            conf = json.load(f)
        for key in tickerData.keys():
            currency_pair.append(key)
        currency_pair.append("BTC_ETH")
        with open('config.json', 'w', encoding='utf-8') as f:
            conf["currency_pair"] = currency_pair
            json.dump(conf, f, ensure_ascii=False, indent=4)

        last_trade = {}
        for key in tickerData.keys():
            last_trade.update({key : tickerData[key]["last_trade"]}) 
        last_trade.update({"BTC_ETH" : str(1 / float(tickerData["ETH_BTC"]["last_trade"]))})
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(last_trade, f, ensure_ascii=False, indent=4)
        print(last_trade)

