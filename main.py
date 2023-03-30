import datetime as dt
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(verbose=True)  # .envファイルが見つからない時にエラーを出す
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GENDER = "male"
WEIGHT_KG = 60
HEIGHT_CM = 170
AGE = 30

NUTRITION_ID = os.environ.get("ENV_NUTRITION_ID")
NUTRITION_KEY = os.environ.get("ENV_NUTRITION_KEY")
NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEET_ID = os.environ.get("ENV_SHEET_ID")
SHEET_KEY = os.environ.get("ENV_SHEET_KEY")
SHEET_ENDPOINT = os.environ.get("ENV_SHEET_ENDPOINT")


def get_nutrition_data():
    exercise_text = input("何のエクササイズを何分した？英語で（e.g. ran 15min, swam 30min, walked 1hour）: ")
    headers = {
        "x-app-id": NUTRITION_ID,
        "x-app-key": NUTRITION_KEY,
    }
    parameters = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE,
    }
    r = requests.post(NUTRITION_ENDPOINT, headers=headers, json=parameters)
    result = r.json()
    return result


# なくてもいい、getの練習
def get_sheets_data():
    headers = {
        "Authorization": SHEET_KEY
    }
    r = requests.get(SHEET_ENDPOINT, headers=headers)
    result = r.json()
    print(result)
#####################


def put_sheets_data():
    headers = {
        "Authorization": SHEET_KEY
    }
    today = dt.datetime.now().strftime("%d/%m/%Y")
    time = dt.datetime.now().strftime("%X")
    result = get_nutrition_data()
    result = result["exercises"]
    print(result)
    for exercise in result:
        sheets_params = {
            "workout": {
                "date": today,
                "time": time,
                "exercise": exercise["user_input"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }
        re = requests.post(SHEET_ENDPOINT, headers=headers, json=sheets_params)
        print(re.text)


put_sheets_data()
