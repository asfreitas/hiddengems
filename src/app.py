#import os
#import sys
#sys.path.insert(0, '/home/vc7mi9ics39z/public_html/cgi-bin/myenv/lib/python3.4/site-packages')
from flask import Flask, render_template, url_for, request, url_for, session, logging, redirect
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)


mysql = MySQL()

#set secret key to allow sessions
#!todo make sessions random
app.secret_key = "hiddengems"

#MYSQL: you'll have to change these when you want to use your
# own MYSQL database on the oregon state servers
app.config['MYSQL_DATABASE_USER'] = 'cs340_freitand'
app.config['MYSQL_DATABASE_PASSWORD'] = '3048'
app.config['MYSQL_DATABASE_DB'] = 'cs340_freitand'
app.config['MYSQL_DATABASE_HOST'] = 'classmysql.engr.oregonstate.edu'
mysql.init_app(app)






@app.route("/", methods=["GET", "POST"])
def index():
	dbconn = mysql.connect()
	cityDBCursor = dbconn.cursor(pymysql.cursors.DictCursor)

	cityDBCursor.execute("SELECT name, idCities FROM Cities", args=None)
	name = cityDBCursor.fetchall()

	if request.method == "POST":
		dbconn2 = mysql.connect()
		cityDBCursor2 = dbconn2.cursor(pymysql.cursors.DictCursor)

		city = request.form.get('cityid')
		app.logger.info(city)
		selectQuery = "SELECT address, type, Gems.name, description, Cities.name FROM Gems INNER JOIN Cities ON location = idCities WHERE idCities = %s"
		cityDBCursor2.execute(selectQuery, city)
		cityInfo = cityDBCursor2.fetchall()
		app.logger.info(cityInfo)
		return render_template("index.html", cityInfo = cityInfo)

	return render_template("index.html", name = name)

@app.route("/add-city", methods=["GET", "POST"])
def add_city():
	if request.method == "POST":
		city = request.form["city"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		state = request.form["state"]
		country = request.form["country"]


		dbconn = mysql.connect()
		cityDBCursor = dbconn.cursor(pymysql.cursors.DictCursor)
		insertQuery = "INSERT INTO Cities (name, latitude, longitude, state, country) VALUES (%s, %s, %s, %s, %s)"
		cityInfo = (city, latitude, longitude, state, country)
		cursor = dbconn.cursor()
		cursor.execute(insertQuery, cityInfo)
		dbconn.commit()
		dbconn.close()
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
		dbconn.close()

	return render_template("create_account.html")

@app.route("/add-gem")
def add_gem():
	return render_template("add_gem.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		password = request.form["password"]
		username = request.form["username"]
		dbconn = mysql.connect()
		cursor = dbconn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Users WHERE username=%s", (username))
		userRow = cursor.fetchone()
		if userRow:
			passwordDB = userRow["password"]
			if passwordDB == password:
				session['logged_in'] = True
				session['username'] = username
				app.logger.info("Logged in")


		dbconn.close()

	return render_template("login.html")

@app.route("/logout")
def logout():
	if session["logged_in"] == True:
		session.clear()
	return redirect(url_for("index"))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)


