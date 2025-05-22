import telebot  
from Token import bot
from currency import Currency
from currency_conventer import CurrencyConventer





class Commands(Currency):
    @bot.message_handler(commands = ["start", "help"])
    def start_help(message:telebot.types.Message): 
        text = "Инструкция по пользованию ботом: <имя первой валюты> <имя валюты, в которую надо перевести> <количество>.\nВсе команды работают исключительно со знаком / перед ними."
        bot.reply_to(message, text) 

    def values(self, message: telebot.types.Message):
        text ="Доступные валюты для конвертации:\n" + "\n".join([f"{k}: {v}" for k, v in self.currency.items()])
        bot.reply_to(message, text)


commands = Commands()

@bot.message_handler(comands = ["value"])
def send_values(message):   
    commands.values(message)





        
bot.polling()







        