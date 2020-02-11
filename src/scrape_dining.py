from bs4 import BeautifulSoup
import datetime
import sqlite3
import requests
import time
import re
import os.path


if os.path.isfile("database/foods.db"): # If the database already exists, try going ahead and reading it.
    connection = sqlite3.connect("database/foods.db")
    cursor = connection.cursor()
else: # If it does not exist, initialize it with the database/database.sql
    connection = sqlite3.connect("database/foods.db")
    cursor = connection.cursor()
    try:
        sql_file = open("database/database.sql")
        cursor.execute(sql_file.read())
    except IOError:
        print("Failed to initialize database.")
    finally:
        sql_file.close()


def location_id_to_name(id):
    locations = ["Worcester","Frank","Hampshire","Berkshire"]
    return locations[id - 1]

"""
Returns a dict which contains all the data for the desired days meals, in the following form:

{
    "meal_name":{
        "category_name":{
            "food_name":{
                "carbs":val,
                "allergens":['list', 'of', 'allergens'],
            }
        }
    }
}
"""
def load_meals(location, date):
    menu = {}
    meals = requests.get('https://umassdining.com/foodpro-menu-ajax?tid={}&date={}'.format(location, date))
    if meals.text == '': # Empty response, dining hall does not exists or is closed
        return {}
    meals = meals.json()
    for meal, meal_cats in meals.items(): # Create a new dict for each meal
        menu[meal] = {}
        for cat, cat_foods in meal_cats.items(): # Combine all of the categories into 
            menu[meal][cat] = parse_meal(cat_foods)
    return menu
            

"""
Returns a list which contains all the food items listed in the supplied html from the api.

Called as part of load_meals.
"""
def parse_meal(meal_html):

    tree = BeautifulSoup(meal_html, 'html.parser')
    foods = {}
    for food in tree.find_all('a'):
        food_facts = {}

        # Load every fact about the food which has parseable units
        for fact in ['cholesterol','dietary-fiber',
                'protein','sat-fat','sodium','sugars','total-carb','total-fat',
                'trans-fat']:
            temp = re.findall(r'[\d\.]+', food.get('data-' + fact)) # Extract number from nutrition fact
            food_facts[fact] = float(temp[0]) if len(temp) > 0 else 0 # Convert list from regex to number

        # Load every fact about the food which does not have parseable units
        for fact in ['calories','calories-from-fat','serving-size']:
            food_facts[fact] = food.get('data-' + fact)
            # Deal with empty values. This needs to be generalized TODO
            food_facts[fact] = None if food_facts[fact] == '' else food_facts[fact]

        food_facts['allergens'] = [allergen for allergen in food.get('data-allergens').replace(' ','').split(',') if allergen != '']
        food_facts['ingredients'] = food.get('data-ingredient-list')
    
        foods[food.get('data-dish-name')] = food_facts

    return foods


def upload_food(name, facts, date, location, meal, category):

    # Insert basic food information
    cursor.execute(
        "INSERT INTO foods(name, date, meal, category, location) VALUES(?,?,?,?,?)",
        (name, date, meal, category, location_id_to_name(location))
    )
    
    connection.commit()

    food_id = cursor.lastrowid
    # Insert nutrtion facts, messy code : (
    cursor.execute(
        "INSERT INTO nutrition(food_id, calories, calories_from_fat, fat, sat_fat, trans_fat, cholesterol, sodium, carbs, fiber, sugar, protein, ingredients, serving_size) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (food_id, facts['total-carb'], facts['calories-from-fat'], facts['total-fat'], facts['sat-fat'], facts['trans-fat'], facts['cholesterol'],
        facts['sodium'], facts['total-carb'], facts['dietary-fiber'], facts['sugars'], facts['protein'], facts['ingredients'], facts['serving-size'])
    )
    connection.commit()

    # Insert allergen and diet flags
    for allergen in facts['allergens']:
        cursor.execute(
            "INSERT INTO flags(name, type, food_id) VALUES(?, ? , ?)",
            (allergen, 'allergen', food_id)
        )


# Upload all the meals from a location on a day.
def upload_meals():
    print("Uploading meals")
    today = datetime.date.today()
    print("Deleting today's meals")
    cursor.execute(
        "DELETE FROM foods WHERE date=?",
        (today,)
    )
    connection.commit()

    for location in [1, 2, 3, 4]:
        print("Downloading meals from " + location_id_to_name(location))
        meals = load_meals(location, today.strftime("%m/%d/%y"))
        # These for loops reach every food, regardless of category.
        if len(meals.items()) == 0:
            print(location_id_to_name(location), "is closed.")
            continue
    
        print("Uploading meals from " + location_id_to_name(location))
        for meal, cats in meals.items():
            for cat, foods in cats.items():
                for food, facts in foods.items():
                    if food != '':
                        upload_food(food, facts, today, location, meal, cat)

    print("Upload done")

if __name__ == '__main__':
    upload_meals()
