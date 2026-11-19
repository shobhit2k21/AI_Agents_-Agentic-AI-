from datetime import datetime
import requests

def get_current_time():
    """Returns the current time as a string in the format 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout = 10)
    return response.text 

TOOLS = [
    {
         "type" : "function",
         "function" : {
             "name" : "get_current_time",
             "description" : "returns the current time.",
             "parameters" : {
                "type" : "object",
                "properties" : {}
             }
         }
    },  
    {   

         "type" : "function",
                 "function" : {
                     "name" : "get_city_weather",
                     "description" : "returns the weather for a given city.",
                     "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "city" : {
                                "type" : "string",
                                "description" : "The name of the city for which to get weather information."
                            }
                        }
                     }
                 } 
    }
]

FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather
}