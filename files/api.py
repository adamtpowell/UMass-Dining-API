from flask import Flask
from flask import request
import datetime
import mysql.connector
import requests
import time
import re

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="dining"
)
cursor = mydb.cursor(dictionary=True)

@app.route("/")
def get():
    res = {}
    try:
        cursor.execute("SELECT * FROM foods WHERE date LIKE '" + datetime.date.today(
        ).strftime("%Y-%m-%d") + "'")
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            res[row['name']] = {
                'category': row['category'],
                'meal': row['meal'],
                'date': row['date'],
                'location': row['location'],
                'details': {
                    'href': '/details?food-id=' + str(row['id'])
                }
            }
    finally:
        cursor.close()

    return res

@app.route("/details")
def details():
    allergens = []
    id = request.args.get('food-id')

    cursor.execute("SELECT * FROM flags WHERE food_id=" + id + " AND type='allergen'")
    rows = cursor.fetchall()
    for row in rows:
        allergens.append(row['name'])

    cursor.execute("SELECT * FROM nutritLion WHERE food_id=" + id)
    nutrition = cursor.fetchone()

    return {
        "allergens": allergens,
        "ingredients": nutrition['ingredients']
    }

if __name__ == "__main__":
    app.run()
