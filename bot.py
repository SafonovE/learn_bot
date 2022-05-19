import ephem
from datetime import datetime
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
logging.basicConfig(filename='bot.log', level=logging.INFO)

#Прокси
'''PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PPROXY_PASSWORD}}'''

today = datetime.date(datetime.now())

planet_dict = {'Mars': ephem.Mars(today), 'Venus': ephem.Venus(today), 'Saturn': ephem.Saturn(today), 
'Jupiter': ephem.Jupiter(today), 'Neptune': ephem.Neptune(today), 
'Uranus': ephem.Uranus(today), 'Mercury': ephem.Mercury(today), 'Sun': ephem.Sun(today)}

def greet_user(update, context):
    print('Вызван / start')
    update.message.reply_text('Привет! Ты стартовал')
    print(update)

def talk_to_me(update, context):
    text = update.message.text 
    print(text)
    update.message.reply_text(text)

def what_constellation(update, context):
    planet_name = update.message.text.split()[1].lower().capitalize()
    ephem_body = planet_dict.get(planet_name, None)
    if ephem_body!=None:
        constellation = ephem.constellation(planet_dict[planet_name])
        update.message.reply_text(constellation[1])
    else:
        update.message.reply_text('Понятия не имею что за планета')


def main():
    mybot = Updater(settings.API_KEY, use_context = True)
    
    #с прокси 
    # mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', what_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()

