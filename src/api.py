from flask import Flask
from flask_graphql import GraphQLView
import graphene

import sqlite3

connection = sqlite3.connect("foods.db", check_same_thread=False)

cursor = connection.cursor()

class Food(graphene.ObjectType):
    name = graphene.String()
    ingredients = graphene.String()
    allergens = graphene.List(graphene.String)
    diets = graphene.List(graphene.String)
    location = graphene.String()

    def resolve_name(parent, info):
        cursor.execute("SELECT name FROM foods WHERE id=%s", (parent["id"],))
        result = cursor.fetchone()
        return result["name"]
    
    def resolve_ingredients(parent, info):
        cursor.execute("SELECT ingredients FROM nutrition WHERE food_id=%s", (parent["id"],))
        result = cursor.fetchone()
        return result["ingredients"]

    def resolve_allergens(parent, info):
        cursor.execute("SELECT name FROM flags WHERE type='allergen' AND food_id=%s", (parent["id"],))
        result = cursor.fetchall()
        return [item["name"] for item in result]

    # TODO: Make the database actually get diet information
    def resolve_diets(parent, info):
        cursor.execute("SELECT name FROM flags WHERE type='diet' AND food_id=%s", (parent["id"],))
        result = cursor.fetchall()
        return [item["name"] for item in result]

    def resolve_location(parent, info):
        cursor.execute("SELECT location FROM foods WHERE id=%s", (parent["id"],))
        result = cursor.fetchone()
        return result["location"]

class Category(graphene.ObjectType):
    name = graphene.String()
    foods = graphene.List(Food)

    def resolve_foods(parent, info):
        cursor.execute("SELECT id FROM foods WHERE location=%s AND meal=%s AND category=%s" , (parent["location"], parent["name"], parent["category"]))
        result = cursor.fetchall()
        return [{"id": item["id"]} for item in result]

    def resolve_name(parent, info):
        return parent["name"]

class Meal(graphene.ObjectType):
    name = graphene.String()
    foods = graphene.List(Food)
    categories = graphene.List(Category)

    def resolve_foods(parent, info):
        cursor.execute("SELECT id FROM foods WHERE location=%s AND meal=%s" , (parent["location"], parent["name"]))
        result = cursor.fetchall()
        return [{"id": item["id"]} for item in result]

    def resolve_categories(parent, info):
        cursor.execute("SELECT DISTINCT category FROM foods WHERE meal=%s", (parent["name"],))
        result = cursor.fetchall()
        return [{"location": parent["location"], "meal": parent["name"], "name": item["category"]} for item in result]

    def resolve_name(parent, info):
        return parent["name"]


class DiningHall(graphene.ObjectType):
    name = graphene.String()
    foods = graphene.List(Food)
    meals = graphene.List(Meal)

    def resolve_name(parent, info):
        return parent["name"]

    def resolve_foods(parent, info):
        cursor.execute("SELECT id FROM foods WHERE location=%s", (parent["name"],))
        result = cursor.fetchall()
        return [{"id": item["id"]} for item in result]

    def resolve_meals(parent, info):
        meals = ['breakfast','lunch','dinner','late night','grabngo']
        return [{"location": parent["name"], "name": meal} for meal in meals]


class Query(graphene.ObjectType):
    foods = graphene.List(Food)
    dining_halls = graphene.List(DiningHall)

    def resolve_foods(parent, info):
        cursor.execute("SELECT id FROM foods WHERE location")
        result = cursor.fetchall()
        return [{"id": item["id"]} for item in result]

    def resolve_dining_halls(parent, info):
        halls = ['worcester', 'frank', 'hampshire', 'berkshire']
        return [{"name": hall} for hall in halls]

schema = graphene.Schema(query=Query)


app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run(host='0.0.0.0')