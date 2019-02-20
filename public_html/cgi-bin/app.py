#import os
#import sys
#sys.path.insert(0, '/home/vc7mi9ics39z/public_html/cgi-bin/myenv/lib/python3.4/site-packages')
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/")
def index():
	return render_template("index.html")


@app.route("/add-city")
def add_city():
    return render_template("add_city.html")

@app.route('/reviews')
def reviews():
    return render_template("reviews.html")

@app.route("/create-account")
def create_account():
	return render_template("create_account.html")

@app.route("/add-gem")
def add_gem():
	return render_template("add_gem.html")









if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)




