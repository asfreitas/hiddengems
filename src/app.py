#import os
#import sys
#sys.path.insert(0, '/home/vc7mi9ics39z/public_html/cgi-bin/myenv/lib/python3.4/site-packages')
from flask import Flask, flash, render_template, url_for, request, url_for, session, logging, redirect
from flaskext.mysql import MySQL
import pymysql
from datetime import datetime
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

#get the user id from sessions
def get_user_id():
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)

	cursor.execute("SELECT idUsers FROM Users WHERE username = %s", (session['username']))
	username = cursor.fetchone()
	conn.close()
	return username['idUsers']

@app.route("/", methods=["GET", "POST"])
def index():
	dbconn = mysql.connect()
	cityDBCursor = dbconn.cursor(pymysql.cursors.DictCursor)

	cityDBCursor.execute("SELECT name, idCities FROM Cities", args=None)
	name = cityDBCursor.fetchall()

	if request.method == "POST":
		dbconn2 = mysql.connect()
		cityDBCursor2 = dbconn2.cursor(pymysql.cursors.DictCursor)
		cityInfo = request.form.get('city')
		selectQuery = "SELECT address, type, Gems.name, description, Cities.name as cityname FROM Gems INNER JOIN Cities ON location = idCities WHERE idCities = %s"
		cityDBCursor2.execute(selectQuery, (cityInfo))
		cityInfo = cityDBCursor2.fetchall()
		app.logger.info(cityInfo)
		return render_template("index.html", cityInfo = cityInfo, name = name)

	return render_template("index.html", name = name)

@app.route("/add-city", methods=["GET", "POST"])
def add_city():

	dbconn = mysql.connect()
	cursor = dbconn.cursor(pymysql.cursors.DictCursor)

	cursor.execute("SELECT name FROM Cities")
	cities = cursor.fetchall()

	if request.method == "POST":
		city = request.form["city"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		state = request.form["state"]
		country = request.form["country"]
		for x in cities:
			if city == x['name']:
				flash('Your city is already in Hidden Gems')
				return render_template("add_city.html")



		dbconn = mysql.connect()
		cursor = dbconn.cursor(pymysql.cursors.DictCursor)
		insertQuery = "INSERT INTO Cities (name, latitude, longitude, state, country) VALUES (%s, %s, %s, %s, %s)"
		cityInfo = (city, latitude, longitude, state, country)
		cursor.execute(insertQuery, cityInfo)
		dbconn.commit()
		dbconn.close()
	return render_template("add_city.html")

@app.route('/reviews')
def reviews():
	dbconn = mysql.connect()
	return render_template("reviews.html")

@app.route("/create-account", methods=["GET", "POST"])
def create_account():
	dbconn = mysql.connect()
	cursor = dbconn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT idCities, name FROM Cities", args=None)
	cities = cursor.fetchall()
	if request.method == "POST":
		user = request.form["user"]
		password = request.form["password"]
		hometown = request.form["hometown"]

		#connect to database and insert row

		# get cityid from row received from DB
		hometown = hometownRow["idCities"]
		insertQuery = "INSERT INTO Users (username, home_city, password) VALUES (%s, %s, %s)"
		userInfo = (user, hometown, password)
		cursor = dbconn.cursor()
		cursor.execute(insertQuery, userInfo)
		dbconn.commit()
		dbconn.close()

	return render_template("create_account.html", cities=cities)

@app.route("/gems")
def gems():
	dbconn = mysql.connect()
	cursor = dbconn.cursor(pymysql.cursors.DictCursor)
	# Information for displaying all gems
	query = """
SELECT
    `Gems`.`idGems`,
    `Gems`.`name`,
    `Gems`.`description`,
    `Gems`.`type`,
    `Cities`.`name` AS `cityName`,
    `Users`.`username` AS `discoveredByUsername`
FROM
    `Gems`
        LEFT JOIN
    `Cities` ON `Gems`.`location` = `Cities`.`idCities`
        LEFT JOIN
    `Users` ON `Gems`.`created_by` = `Users`.`idUsers`
	"""
	args = ()
	filters = []

	filter_values = {
		'city': request.args.get('city', default='', type=int),
		'type': request.args.get('type', default='')
	}
	if (filter_values['city'] != ''):
		filters.append('`Gems`.`location` = %s')
		args += (filter_values['city'], )

	if (filter_values['type'] != ''):
		filters.append('`Gems`.`type` = %s')
		args += (filter_values['type'], )

	if (len(filters) > 0):
		query += 'WHERE '
		query += ' and '.join(filters)
		print(query)

	cursor.execute(query, args)
	gems = cursor.fetchall()

	# Information for filtering / creating a gem
	cursor.execute("""
SELECT
    `idCities`, `name`
FROM
    `Cities`;
	""")
	cities = cursor.fetchall()

	cursor.execute("""
SELECT DISTINCT
    `type`
FROM
    `Gems`;
	""")
	types = cursor.fetchall()


	dbconn.close()
	return render_template("gems.html", gems = gems, cities = cities, types = types, filter_values = filter_values)

@app.route("/edit-gem", methods = ['GET', 'POST'], defaults = {'gemId': -1})
@app.route("/edit-gem/<gemId>", methods = ['GET', 'POST'])
def create_gem(gemId):
	dbconn = mysql.connect()
	cursor = dbconn.cursor(pymysql.cursors.DictCursor)
	
	cursor.execute("SELECT `idUsers` FROM `Users` WHERE `username` = %s", (session['username']))
	row = cursor.fetchone()
	userId = row['idUsers']

	print(str(gemId))

	if (request.method == 'POST'):

		args = (
			pymysql.escape_string(request.form['address']),
			pymysql.escape_string(request.form['type']),
			pymysql.escape_string(request.form['title']),
			pymysql.escape_string(request.form['description']),
			pymysql.escape_string(str(userId)),
			pymysql.escape_string(request.form['city'])
		)

		query = ""
		if (gemId != -1):
			# Check if the user created the gem or not
			cursor.execute("SELECT `created_by` FROM `Gems` WHERE `idGems` = %s", (gemId))
			row = cursor.fetchone()
			if (row['created_by'] != userId):
				return render_template('error.html', message = "Only the creator of a gem may edit it.")


			query = """
UPDATE `Gems` SET `address` = %s, `type` = %s, `name` = %s, `description` = %s, `created_by` = %s, `location` = %s WHERE `idGems` = %s
			"""
			args += (str(gemId), )
		else:
			query = """
INSERT INTO `Gems` (`address`, `type`, `name`, `description`, `created_by`, `location`)
	VALUES (%s, %s, %s, %s, %s, %s)
			"""

		affectedRows = cursor.execute(query, args)
		dbconn.commit();

		if (affectedRows == 1):
			query = """
	SELECT `idGems` FROM `Gems` WHERE `address` = %s and `type` = %s and `name` = %s and `description` = %s and `created_by` = %s and `location` = %s
			"""
			numResults = cursor.execute(query, (request.form['address'], request.form['type'], request.form['title'], request.form['description'], userId, request.form['city']))
			row = cursor.fetchone()
			newGemId = row['idGems']
			return redirect(url_for('gem_solo', gemId = newGemId))
		else:
			return render_template('error.html', message = "We were unable to create / edit the gem.")
	else:
		if ('username' in session):
			cursor.execute("""
		SELECT
		    `idCities`, `name`
		FROM
		    `Cities`;
			""")
			cities = cursor.fetchall()

			gem = False
			if (gemId != -1):
				# Check if the user created the gem or not
				cursor.execute("SELECT * FROM `Gems` WHERE `idGems` = %s", (gemId))
				gem = cursor.fetchone()
				if (gem['created_by'] != userId):
					return render_template('error.html', message = "Only the creator of a gem may edit it.")

			return render_template('edit_gem.html', cities = cities, gem = gem)
		else:
			return render_template('error.html', message = "You need to be logged in to create a gem.")

@app.route("/gem/<gemId>")
def gem_solo(gemId):
	if (gemId == None):
		return render_tempalte("error.html", message = "Missing a gem id.")
	else:
		dbconn = mysql.connect()
		cursor = dbconn.cursor(pymysql.cursors.DictCursor)

		cursor.execute("""
SELECT
    `Gems`.`idGems`,
    `Gems`.`name`,
    `Gems`.`description`,
    `Cities`.`name` AS `cityName`,
    `Cities`.`idCities`,
    `Users`.`username` AS `discoveredByUsername`,
    COUNT(`Favorites`.`user`) AS `stars`
FROM
    `Gems`
        LEFT JOIN
    `Cities` ON `Gems`.`location` = `Cities`.`idCities`
        LEFT JOIN
    `Users` ON `Gems`.`created_by` = `Users`.`idUsers`
        LEFT JOIN
    `Favorites` ON `Gems`.`idGems` = `Favorites`.`gem`
WHERE
    `Gems`.`idGems` = %s
GROUP BY `Gems`.`idGems`;
		""", (gemId))
		gem = cursor.fetchone()

		cursor.execute("""
SELECT
    `Reviews`.`created`,
    `Reviews`.`contents`,
    `Users`.`username`
FROM
    `Reviews`
        LEFT JOIN
    `Users` ON `Users`.`idUsers` = `Reviews`.`written_by`
WHERE
    `Reviews`.`gem` = %s
		""", (gemId))
		reviews = cursor.fetchall()

		dbconn.close()
		return render_template("solo_gem.html", gem = gem, reviews = reviews)

@app.route("/login", methods=["GET", "POST"])
def login():
	dbconn = mysql.connect()
	if request.method == "POST":
		password = request.form["password"]
		username = request.form["username"]
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

@app.route("/delete/<gemId>", methods=["POST", "GET"])
def delete_gem(gemId):
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("DELETE FROM Gems WHERE idGems = %s", (gemId))
	conn.commit()

	cursor.execute("DELETE FROM Favorites WHERE gem = %s", (gemId))
	conn.commit()
	conn.close()
	return redirect(url_for("index"))

@app.route("/makereview/<gemId>", methods=["POST"])
def create_review(gemId):
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	#I got this from here https://www.tutorialspoint.com/How-to-insert-date-object-in-MySQL-using-Python
	now = datetime.now()
	formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
	review = request.form["reviewtext"]
	userid = get_user_id()
	print(userid)
	data = (formatted_date, review, userid, gemId)
	cursor.execute("INSERT INTO Reviews (created, contents, written_by, gem) VALUES (%s,%s,%s,%s)",data)
	conn.commit()
	conn.close()
	return redirect(url_for("gem_solo", gemId=gemId))


@app.route("/profile")
def profile():
	return render_template("profile.html")



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
