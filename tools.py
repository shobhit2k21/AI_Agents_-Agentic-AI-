#standard library imports
from datetime import datetime
import json

#third party imports
import requests

#local modules
from Utilities.utilities import log


def get_current_time():
    """Returns the current time as a string in the format 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout = 10)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text 


def get_my_city():
    return "Lucknow"


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
                        },
                        "required" : ["city"]
                     }
                 } 
    },

     {
             "type" : "function",
             "function" : {
                 "name" : "get_my_city",
                 "description" : "returns the user's city or where the user lives.",
                 "parameters" : {
                    "type" : "object",
                    "properties" : {}
                 }
             }
        }
]

FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_my_city": get_my_city
}

def run_tools(tool_call):
    func_name = tool_call.function.name
    
    try:
     func_args = json.loads(tool_call.function.arguments or "{}")
     log(f"Calling function: {func_name} with arguments: {func_args}")
     fn = FUNCTION_MAP[func_name]
     result = fn(**func_args)
                
    except Exception as e:
     result = f"Error occurred while calling function {func_name}: {e}"

    log(f"Function {func_name} returned: {result}")
    return result