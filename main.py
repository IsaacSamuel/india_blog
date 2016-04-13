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
def show_entries():
	entries = txttohtml.allentries()["entries"]
	titles = txttohtml.allentries()["titles"]
	bodies = txttohtml.allentries()["bodies"]
	taglist = txttohtml.allentries()["tags"]

	return render_template('show_entries.html', entries = entries, taglist = taglist, bodies = bodies, titles = titles)
"""
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
		[request.form['title'], request.form['text']])
	g.db.commit()
	flash("New entry was successfully posted!")
	return redirect(url_for('show_entries'))

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

@app.route('/delete', methods=['POST'])
def delete():
	g.db.execute('DELETE FROM entries WHERE id=(?)',
		[request.form['id']])
	g.db.commit()
	flash("Entry was deleted!")
	return redirect(url_for('show_entries'))

@app.route('/edit', methods=['POST'])
def edit():
	cur = g.db.execute('SELECT * FROM entries WHERE id=(?)', [request.form['id']])
	part = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
	return render_template('edit.html', entry=part[0])

@app.route('/update', methods=["POST"])
def update():
	g.db.execute('UPDATE entries SET title=?, text=? WHERE id=?', [request.form['title'], request.form['text'], request.form['id']])
	g.db.commit()
	flash("You updated entry %s" %request.form['title'])
	return redirect(url_for('show_entries'))

@app.route('/add_tag', methods=['POST'])
def add_tag():
	g.db.execute('DELETE FROM tags WHERE entry=(?)', [request.form['entry']])
	g.db.commit()
	if ", " in request.form['name']:
		split = request.form['name'].split(",")
		for i in split:
			g.db.execute('INSERT INTO tags (entry, name) VALUES (?, ?)', [request.form['entry'], i])
			g.db.commit()
	else:
		g.db.execute('INSERT INTO tags (entry, name) VALUES (?, ?)', [request.form['entry'], request.form['name']])
		g.db.commit()
	flash("You added some tags.")
	return redirect(url_for('show_entries'))

@app.route('/tag/')
@app.route('/tag/<tag>')
def tag(tag = None):
	cur = g.db.execute('SELECT entry FROM tags WHERE name=(?)', [tag])
	entry_numbers= cur.fetchall()
	entries = []
	for each in entry_numbers:
		cur = g.db.execute('SELECT * FROM entries WHERE id =(?)', [each[0]])
		entries = entries + [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
	cur = g.db.execute('SELECT entry, name FROM tags')
	tags = [dict(entry=row[0], name=row[1]) for row in cur.fetchall()]
	return render_template("tag.html", entries = entries, tags = tags, entry_numbers = entry_numbers, tagnames=tagnames)


@app.route('/entry/')
@app.route('/entry/<var>')
def entryvar(var = None):
	cur = g.db.execute('SELECT * FROM entries where id=(?)', [var])
	entry = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
	cur = g.db.execute('SELECT entry, name FROM tags')
	tags = [dict(entry=row[0], name=row[1]) for row in cur.fetchall()]
	cur = g.db.execute('SELECT name, comment, entry, id FROM comments')
	comments = [dict(name=row[0], comment=row[1], entry=row[2], id=row[3]) for row in cur.fetchall()]
	return render_template("entry.html", var = var, entry = entry[0], tags = tags, comments = comments)

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
"""




#Runs server
if __name__ == "__main__":
	app.run()