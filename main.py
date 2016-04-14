import sqlite3
from flask import Flask , render_template, g, session, redirect, url_for, abort, flash, request
from contextlib import closing
import txttohtml

#config
DATABASE = "/tmp/flaskr.db"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "password"

#application
app = Flask(__name__)
app.config.from_object(__name__)

#Connects to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()



#ROUTING
@app.route('/')
@app.route('/index')
@app.route('/index/<var>')
def show_entries(var=0):

	entries=[]
	titles = txttohtml.allentries()["titles"]
	bodies = txttohtml.allentries()["bodies"]
	taglist = txttohtml.allentries()["tags"]

	length = len(txttohtml.allentries()["entries"])
	start = int(var)*4
	rangenum = start+4

	if (length-start) < 4:
		rangenum = start+length-start

	for i in range(start, rangenum):
		entries = entries + [txttohtml.allentries()["entries"][i]]


	return render_template('show_entries.html', entries = entries, taglist = taglist, bodies = bodies, titles = titles, var=int(var), length=length)


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = "Invalid username"
		elif request.form['password'] != app.config['PASSWORD']:
			error = "Invalid password"
		else:
			session['logged_in'] = True
			flash("You were logged in!")
			return redirect(url_for("show_entries"))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash("You were logged out!")
	return redirect(url_for("show_entries"))


@app.route('/tag/')
@app.route('/tag/<tag>')
def tag(tag = None):
	if tag:
		tag = str(tag)

	tagslist = txttohtml.allentries()["tags"]

	#finds indexes of the tag array containing the tag that was searched for
	valid = []
	for tags in tagslist:
		for each in tags:
			if tag in each:
				valid = valid + [tagslist.index(tags)]


	entries = []

	for i in valid:
		entries = entries +[txttohtml.allentries()["entries"][i]]

	tagslist = txttohtml.allentries()["tags"]
	titles = txttohtml.allentries()["titles"]
	bodies = txttohtml.allentries()["bodies"]

	return render_template("tag.html", entries = entries, tags = tagslist, titles=titles, bodies=bodies)


@app.route('/entry/')
@app.route('/entry/<var>')
def entryvar(var = None):
	if var:
		var = int(var)

	entries = txttohtml.allentries()["entries"][var]
	titles = txttohtml.allentries()["titles"][var]
	bodies = txttohtml.allentries()["bodies"][var]
	taglist = txttohtml.allentries()["tags"][var]

	cur = g.db.execute('SELECT name, comment, entry, id FROM comments')
	comments = [dict(name=row[0], comment=row[1], entry=row[2], id=row[3]) for row in cur.fetchall()]
	
	return render_template("entry.html", var = var, entry = entries, tags = taglist, comments = comments, title = titles, body=bodies)

@app.route('/submit_comment', methods=["POST"])
def submit_comment():
	g.db.execute('INSERT INTO comments (entry, name, comment) VALUES (?, ?, ?)', [request.form['entry'], request.form['name'], request.form['comment']])
	g.db.commit()
	flash("You added a comment!")
	a = request.form['entry']
	return redirect(url_for("entryvar", var=request.form['entry']))

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
	g.db.execute('DELETE FROM comments WHERE id=(?)', [request.form['id']])
	g.db.commit()
	flash("Comment was deleted!")
	return redirect(url_for("entryvar", var=request.form['entry']))




#Runs server
if __name__ == "__main__":
	app.run()