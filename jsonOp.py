import json



def newUserId(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    if not str(id) in data.keys():
        currency_set = {}
        new_user = {}
        for item in conf["currency_pair"]:
            currency_set.update({item : {"min" : 0, "max" : 0}})
        new_user.update({id : {"currency_pair" : currency_set, "alert_set": 1, "alert_count" : 0}})
        data.update(new_user)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def pairUpdate(id, pair, min, max):
    pass


