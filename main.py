import json
import botLogic
import reciveExmoData


reciveExmoData.reciveJsonTickerData()
botLogic.check_values()
 
botLogic.bot.polling(none_stop=True)
