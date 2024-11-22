import os
import random
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
name = "Omnia"
class Chatbot:
    def __init__(self, name):
        self.__name = name #private variable.

    def get_name(self):
        return self.__name

    @staticmethod
    def greet():
        return "Hi ,"

#getter kullandigim kisim.
    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def get_input(self):
        user_input = input(f"I'm your {self.get_class_name()},and my name is {self.get_name()}, what can I help you with today? ")
        return user_input


    def generate_response(self, user_input):
        greeting_responses = ["Hi! How can I help you today?",
                              "Hello, How can I help you today?",
                              "Hey! How can I help you today?",
                              "Hi! What can I help you with today?"]
        if "hi" in user_input.lower():
            return random.choice(greeting_responses)
        elif "hello" in user_input.lower():
            return random.choice(greeting_responses)
        elif "how are you" in user_input.lower():
            return "I'm a chatbot made by humans. I don't have any feelings."
        elif "weather" in user_input.lower():
            city = input("Which city or town would you like to know the weather for?  ")
            weather_bot = WeatherBot(self.get_name(), os.getenv("weather_api_key"))
            return weather_bot.get_weather(city)
        elif "add reminder" in user_input.lower():
            reminder_name = input("What is the name of the reminder? ")
            reminder_date = input("What is the date of the reminder? (YYYY-MM-DD) ")
            reminder_time = input("What is the time of the reminder? (HH:MM) ")
            return reminder_bot.add_reminder(reminder_name, reminder_date, reminder_time)
        elif "delete reminder" in user_input.lower():
            reminder_name = input("What is the name of the reminder you want to delete? ")
            return reminder_bot.del_reminder(reminder_name)
        elif "show reminders" in user_input.lower():
            return reminder_bot.show_reminders()

class WeatherBot(Chatbot):
    def __init__(self, name, weather_api_key):
        super().__init__(name)
        self.weather_api_key = weather_api_key

    def get_weather(self, location):
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": self.weather_api_key,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            temp = data["main"]["temp"]
            return f"The weather in {location} is {data['weather'][0]['description']} with a temperature of {temp}°C."
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"
        except KeyError:
            return f"Error parsing weather data"

class ReminderBot(Chatbot):
    def __init__(self, name):
        super().__init__(name)
        self.__reminders = []

    def add_reminder(self, reminder_name, reminder_date, reminder_time):
        reminder = {
            "name": reminder_name,
            "date": reminder_date,
            "time": reminder_time
        }
        self.__reminders.append(reminder)
        return "Reminder added successfully"

    def del_reminder(self, reminder_name):
        for reminder in self.__reminders:
            if reminder["name"] == reminder_name:
                self.__reminders.remove(reminder)
                return "Reminder deleted successfully"
        return "Reminder not found."

    def get_reminders(self):
        return self.__reminders


    def show_reminders(self):
        if not self.__reminders:
            return "No reminders set."
        reminders_list = "\n".join([f"{reminder['name']} on {reminder['date']} at {reminder['time']}" for reminder in self.get_reminders()])
        return f"Your reminders:\n{reminders_list}"

if __name__ == "__main__":
    Chatbot.get_class_name() #
    chatbot = Chatbot(name)
    reminder_bot = ReminderBot(name)
    try:
        while True:
            print(Chatbot.greet())
            user_input = chatbot.get_input()
            response = chatbot.generate_response(user_input)
            print(response)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting... ")


#class TranslateBot:
#    def __init__(self, name, google_translate_api_key):
#        super().__init__(name)
#        self.__google_translate_api_key = google_translate_api_key
#     self.__languages = self.get_supported_languages()
#    def get_supported_languages(self):
#        base_url = "https://translation.googleapis.com/language/translate/v2/languages"
#        params = { "key": self.__google_translate_api_key }
#        response = requests.get(base_url, params=params)

