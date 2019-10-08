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

    def resolve_name(parent, info):
        return "Spaghetti"
    
    def resolve_ingredients(parent, info):
        return ["Peanuts", "Tree Nuts", "Coconut", "Sesame"]

class Query(graphene.ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    foods = graphene.List(Food)

    def resolve_foods(parent, info):
        return [Food()]

schema = graphene.Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run()