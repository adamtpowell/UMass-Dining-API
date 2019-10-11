from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="root",
#     database="dining"
# )
# cursor = mydb.cursor(dictionary=True)

class Food(graphene.ObjectType):
    name = graphene.String()
    ingredients = graphene.List(graphene.String)
    subfoods = graphene.List(Food)

    def resolve_name(parent, info):
        return parent["name"]
    
    def resolve_ingredients(parent, info):
        return parent["ingredients"]
    
    def resolve_subfoods(parent, info):
        return [{"name": "Sub"}]

class Query(graphene.ObjectType):
    foods = graphene.List(Food)

    def resolve_foods(parent, info):
        return [{"name": "Spaghetti", "ingredients": ["Test"]}, {"name": "Meatballs", "ingredients": ["Test"]}]

schema = graphene.Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run()