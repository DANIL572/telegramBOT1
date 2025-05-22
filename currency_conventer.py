import telebot
import requests
import json
from currency import Currency
from Token import bot



class CurrencyConventer(Currency):
    def convert(self, message: telebot.types.Message):
        try:

            value = message.text.split(" ")
                
            if len(value) != 3:
                raise IndexError("Аргументов должно быть 3.")
                
            
            quote, base, amount = value

            
            if quote == base:
                raise KeyError("Невозможно конвертировать одинаковые валюты.")

                
            try:    
                amount = float(amount)
            except:
                raise ValueError("Третий аргумент должен быть числом.")
            
            if amount <= 0:
                raise IndexError("Число конвертируемой валюты не может быть меньше 1.")
            
            if quote not in self.currency or base not in self.currency:
                raise ValueError("Конвертируемой валюты не существует или убедитесь что правильно ввели название валюты.")

            try:
                api = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={self.currency[quote]}&tsyms={self.currency[base]}")
            except requests.exceptions.ConnectionError:
                bot.send_message(message.chat.id, f"Ошибка работы API")
  
            response_data = json.loads(api.content)
            converted_value = float(response_data[self.currency[base]])
            total = converted_value * amount
            bot.send_message(message.chat.id, f"{amount} {quote} = {total:.2f} {base}")
        except ValueError as v:
            bot.send_message(message.chat.id, f"Ошибка: {v}")
        except KeyError as k:
            bot.send_message(message.chat.id, f"Ошибка: {k}")
        except IndexError as i:
            bot.send_message(message.chat.id, f"Ошибка: {i}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Непредвиденная ошибка: {e}")

currency_converter = CurrencyConventer()

@bot.message_handler(content_types = {"text"})
def sent_convert(message):
    currency_converter.convert(message)
