from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g
import datetime
from datetime import date,timedelta

from . import db
bp = Blueprint("todo", "todo", url_prefix="")

@bp.route("/")
def home():
	return render_template('index.html')

@bp.route("/about")
def about():
	return render_template('about.html')

@bp.route("/contact")
def contact():
	return render_template('contact.html')



@bp.route("/<uname>/edit", methods=["GET", "POST"])
def edit(uname):
	conn = db.get_db()
	cursor = conn.cursor()
	cursor.execute("SELECT username,description,due_date,status FROM todo WHERE username = ? ORDER BY due_date ASC",[uname])
	data = cursor.fetchall()
	if not data:
		return render_template('edit.html',uname = uname, data = data)
	elif data:
		return render_template('edit.html',uname = uname, data = data)
	elif request.method == 'GET':
		return redirect(url_for('todo.add',uname = uname))
	elif request.method == "POST":
		uname = uname
		d = request.form['d']
		due_date = request.form['due']
		conn = db.get_db()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO todo(username,description,due_date) VALUES(?,?,?);",[uname,d,due_date])
		conn.commit()
		cursor.close()
	return render_template('edit.html',uname = uname, data = data)


@bp.route("/<uname>/add", methods=["GET", "POST"])
def add(uname):
	conn = db.get_db()
	cursor = conn.cursor()
	if request.method == 'POST':
		uname = uname
		d = request.form['d']
		due_date = request.form['due']
		cursor.execute("INSERT INTO todo(username,description,due_date) VALUES(?,?,?);",[uname,d,due_date])
		conn.commit()
		cursor.execute("SELECT username,description,due_date,status FROM todo WHERE username = ? ORDER BY due_date ASC",[uname])
		data = cursor.fetchall()
		return redirect(url_for('todo.edit',uname = uname))
	cursor.close()
	return render_template('add.html',uname = uname)



@bp.route("/<d>/update",methods = ["GET", "POST"])
def update(d):
	if request.method == 'POST':
		description = request.form['d']
		due_date = request.form['due']
		status = request.form['status']
		conn = db.get_db()
		cursor = conn.cursor()
		cursor.execute("UPDATE todo SET description = ?,due_date = ?,status = ? WHERE description = ?;",[description,due_date,status,d])
		conn.commit()
		cursor.execute("SELECT username FROM todo WHERE description = ?",[description])
		uname = cursor.fetchall()[0][0]
		cursor.execute("SELECT username,description,due_date,status FROM todo WHERE username = ? ORDER BY due_date ASC",[uname])
		data = cursor.fetchall()
		cursor.close()
		#return render_template('edit.html',uname = uname,data = data)
		return redirect(url_for('todo.edit',uname = uname))
	return render_template('update.html',d = d)


@bp.route("/<d>/delete",methods = ['POST'])
def delete(d):
	conn = db.get_db()
	cursor = conn.cursor()
	cursor.execute("SELECT username,due_date FROM todo WHERE description = ?",[d])
	uname,date = cursor.fetchall()[0]
	cursor.execute("DELETE FROM todo WHERE description = ? AND due_date = ?",[d,date])
	conn.commit()
	cursor.close()
	return redirect(url_for('todo.edit',uname = uname))


@bp.route("/<uname>/overdue")
def overdue(uname):
	conn = db.get_db()
	cursor = conn.cursor()
	today = date.today()
	cursor.execute("SELECT username,description,due_date,status FROM todo WHERE (username = ? AND due_date<? AND status!= 'DONE') ORDER BY due_date ASC",[uname,today])
	data = cursor.fetchall()
	cursor.execute("SELECT COUNT(description) FROM todo WHERE (username = ? AND due_date<? AND status!= 'DONE') ORDER BY due_date ASC",[uname,today])
	count = cursor.fetchall()
	cursor.close()
	return render_template('overdue.html',uname = uname,data = data,count = count)

@bp.route("/<uname>/today")
def today(uname):
	conn = db.get_db()
	cursor = conn.cursor()
	t = date.today()
	cursor.execute("SELECT username,description,due_date,status FROM todo WHERE (username = ? AND due_date=? AND status!= 'DONE') ORDER BY due_date ASC",[uname,t])
	data = cursor.fetchall()
	cursor.execute("SELECT COUNT(description) FROM todo WHERE (username = ? AND due_date=? AND status!= 'DONE') ORDER BY due_date ASC",[uname,t])
	count = cursor.fetchall()
	cursor.close()
	return render_template('today.html',uname = uname,data = data,count = count)


@bp.route("/<uname>/week")
def week(uname):
	conn = db.get_db()
	cursor = conn.cursor()
	t = date.today()
	w = (date.today()+timedelta(days=7)).isoformat()
	cursor.execute("SELECT username,description,due_date,status FROM todo WHERE (username = ? AND (due_date>=? AND due_date<=?) AND status!= 'DONE') ORDER BY due_date ASC",[uname,t,w])
	data = cursor.fetchall()
	cursor.execute("SELECT COUNT(description) FROM todo WHERE (username = ? AND (due_date>=? AND due_date<=?) AND status!= 'DONE') ORDER BY due_date ASC",[uname,t,w])
	count = cursor.fetchall()
	cursor.close()
	return render_template('week.html',uname = uname,data = data,count = count)



@bp.route("/login",methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		uname = request.form['uname']
		pw = request.form['pw']
		conn = db.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT username,password FROM user_data")
		
		if (uname,pw) in cursor.fetchall():
			return redirect(url_for("todo.edit",uname = uname))
		else:
			return redirect(url_for("todo.register"))

	return render_template('login.html')



@bp.route("/register",methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		uname = request.form['uname']
		pw = request.form['pw']
		conn = db.get_db()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO user_data(username,password) VALUES(?,?);",[uname,pw])
		conn.commit()
		cursor.close()
		return render_template('login.html')
	return render_template('register.html')
