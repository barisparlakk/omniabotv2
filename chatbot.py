import os
import random
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
name = "Omnia"
class Chatbot:
    def __init__(self, name):
        self.name = name
    def get_input(self):
        user_input = input("Hello, I'm Omnia, what can I help you with today? ")
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
            city = input("Which city or town would you like to know the weather for? ")
            weather_bot = WeatherBot(self.name, os.getenv("weather_api_key"))
            return weather_bot.get_weather(city)

        ###
        elif "reminder" in user_input.lower():
            reminder = input("What reminder would you like to add? ")
            return self.add_reminder(reminder)
###

class WeatherBot(Chatbot):
    def __init__(self, name, weather_api_key):
        super().__init__(name)
        self.weather_api_key = weather_api_key

    def get_weather(self, location):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
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
        self.reminders = []

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        return "Reminder added successfully"


if __name__ == "__main__":
    chatbot = Chatbot(name)
    while True:
        user_input = chatbot.get_input()
        response = chatbot.generate_response(user_input)
        print(response)