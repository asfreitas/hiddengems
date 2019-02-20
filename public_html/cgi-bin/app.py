#import os
#import sys
#sys.path.insert(0, '/home/vc7mi9ics39z/public_html/cgi-bin/myenv/lib/python3.4/site-packages')
from flask import Flask, render_template, url_for, request, url_for, session
from flaskext.mysql import MySQL
import pymysql
app = Flask(__name__)


mysql = MySQL()


#MYSQL: you'll have to change these when you want to use your
# own MYSQL database on the oregon state servers
app.config['MYSQL_DATABASE_USER'] = 'cs340_freitand'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cs340_freitand'
app.config['MYSQL_DATABASE_HOST'] = 'classmysql.engr.oregonstate.edu'
mysql.init_app(app)



@app.route("/")
def index():
	return render_template("index.html")


@app.route("/add-city")
def add_city():
    return render_template("add_city.html")

@app.route('/reviews')
def reviews():
    return render_template("reviews.html")

@app.route("/create-account", methods=["GET", "POST"])
def create_account():

	if request.method == "POST":
		user = request.form["user"]
		password = request.form["password"]
		hometown = request.form["hometown"]
		#connect to database and insert row

		dbconn = mysql.connect()
		userDBCursor = dbconn.cursor(pymysql.cursors.DictCursor)
		hometownCursor = dbconn.cursor(pymysql.cursors.DictCursor)
		cityIDQuery = "SELECT idCities FROM Cities WHERE name = %s"
		hometownCursor.execute(cityIDQuery, hometown)
		hometownRow = hometownCursor.fetchone()
		# get cityid from row received from DB
		hometown = hometownRow["idCities"]
		insertQuery = "INSERT INTO Users (username, home_city, password) VALUES (%s, %s, %s)"
		userInfo = (user, hometown, password)
		cursor = dbconn.cursor()
		cursor.execute(insertQuery, userInfo)
		dbconn.commit()



	return render_template("create_account.html")

@app.route("/add-gem")
def add_gem():
	return render_template("add_gem.html")




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)



