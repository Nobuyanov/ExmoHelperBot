import json
import botLogic
import reciveExmoData


reciveExmoData.reciveJsonTickerData()
 
botLogic.bot.polling(none_stop=True)