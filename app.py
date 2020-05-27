from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route('/')
def home():

    marsInfo = mongo.db.marsInfo.find_one()

    return render_template('index.html', info = marsInfo)

@app.route('/scrape')
def scrapestuff():
    
    data = scrape_mars.ScrapeMars()

    mongo.db.marsInfo.update({}, data, upsert=True)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

