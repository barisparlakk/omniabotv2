import os
import random
import requests
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from datetime import datetime

load_dotenv()
name = "Omnia"

#help module
def help_info(user_input):
    if "help weather" in user_input.lower():
        return "WeatherBot commands:\n- weather: Get the current weather for a specified location."
    elif "help reminders" in user_input.lower():
        return "ReminderBot commands:\n- add reminder: Add a new reminder.\n- delete reminder: Delete an existing reminder.\n- show reminders: Show all reminders."
    else:
        return "Available commands:\n- help weather: List WeatherBot commands.\n- help reminders: List ReminderBot commands."

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

    @abstractmethod
    def generate_response(self, user_input):
        pass

class WeatherBot(Chatbot):
    def __init__(self, name, weather_api_key):
        super().__init__(name)
        self.weather_api_key = weather_api_key

    def generate_response(self, user_input):
        if  user_input.lower() == "weather":
            city = input("Which city or town would you like to learn the weather for?  ")
            return self.get_weather(city)

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

    def generate_response(self, user_input):
        if "add reminder" in user_input.lower():
            reminder_name = input("What is the name of the reminder? ")
            reminder_date = input("What is the date of the reminder? (YYYY-MM-DD) ")
            reminder_time = input("What is the time of the reminder? (HH:MM) ")
            return self.add_reminder(reminder_name, reminder_date, reminder_time)
        elif "delete reminder" in user_input.lower():
            reminder_name = input("What is the name of the reminder you want to delete? ")
            return self.del_reminder(reminder_name)
        elif "show reminders" in user_input.lower():
            return self.show_reminders()

    def add_reminder(self, reminder_name, reminder_date, reminder_time):
        reminder = {
            "name": reminder_name,
            "date": reminder_date,
            "time": reminder_time
        }
        self.__reminders.append(reminder)
        return "Reminder added successfully. "

    def del_reminder(self, reminder_name):
        for reminder in self.__reminders:
            if reminder["name"] == reminder_name:
                self.__reminders.remove(reminder)
                return "Reminder deleted successfully. "
        return "Reminder not found. "

    def get_reminders(self):
        return self.__reminders

    def show_reminders(self):
        if not self.__reminders:
            return "No reminders set."
        reminders_list = "\n".join([f"{reminder['name']} on {reminder['date']} at {reminder['time']}" for reminder in self.get_reminders()])
        return f"Your reminders:\n{reminders_list}"

if __name__ == "__main__":
    weather_bot = WeatherBot(name, os.getenv("weather_api_key"))
    reminder_bot = ReminderBot(name)
    try:
        while True:
            print(Chatbot.greet())
            user_input = weather_bot.get_input()
            if "help" in user_input.lower():
                response = help_info(user_input)
            elif "weather" in user_input.lower() and "help" not in user_input.lower():
                response = weather_bot.generate_response(user_input)
            elif "reminder" in user_input.lower():
                response = reminder_bot.generate_response(user_input)
            else:
                response = "I can only provide weather information or manage reminders, for now. Type 'help weather' or 'help reminders' for spesific information. "
            print(response)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
#Until this part was before the midterm. I'll update the following code until the final exam of OOP. ( Line-122, Line-68 Line-39 and Line-31)
