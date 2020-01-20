import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "hero_association"
app.config["MONGO_URI"] = "mongodb+srv://ablshk:Zc0d1ng%2C%2E%2F@schooldb-3btdc.mongodb.net/hero_association?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("index.html", classlist=mongo.db.classlist.find())

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/newentry", methods=['POST'])
def addhero():
    heroes = mongo.db.classlist
    heroes.insert_one(request.form.to_dict())
    return redirect(url_for("home"))

@app.route("/edithero/<hero_id>")
def edithero(hero_id):
    the_hero = mongo.db.classlist.find_one({"_id": ObjectId(hero_id)})
    return render_template("editheroes.html", hero=the_hero)

@app.route("/updatehero/<hero_id>", methods=["POST"])
def updatehero(hero_id):
    heroes = mongo.db.classlist
    heroes.update({"_id": ObjectId(hero_id)}, 
    {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'hero_name': request.form.get('hero_name'),
        'class': request.form.get('class'),
        'rank': request.form.get('rank'),
        'abilities': request.form.get('abilities')
    })
    return redirect(url_for("home"))

@app.route("/deletehero/<hero_id>")
def deletehero(hero_id):
    heroes = mongo.db.classlist
    heroes.delete_one({"_id": ObjectId(hero_id)})
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run()