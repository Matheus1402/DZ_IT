import psycopg2
from flask import Flask
import pandas as pd
import os
from flask import render_template,request,redirect, url_for, send_file
import winreg

app = Flask(__name__)

con = psycopg2.connect(user="*****", 
                       password="*****",
                       host="127.0.0.1",
                       port="5432",
                       database="proc_data")
    
@app.route('/',methods=['GET','POST'])
def menu(): 
	c = con.cursor()
	c.execute("""SELECT * FROM proc_schema.timetable ORDER BY s_name;""")
	data = c.fetchall()
	return render_template('/menu.html', data = data)
	
@app.route('/booking',methods=['GET','POST'])
def getting_booking_page():
	if request.method == 'POST':
		data = request.form['submit']
		num = data[-2:]
		data = data[:-2]
		if data[-1:] == ".":
			data = data[:-1]
		if num[0] == ".":
			num = num[1:]
		num = str(num)
		time = data[-5:] + ":00"
		return render_template('/booking.html', data = data, num = num, time = time)
		
@app.route('/answer',methods=['GET','POST'])
def generate_answer():
	if request.method == 'POST':
		user_name = request.form.get('user_name')
		amount = request.form.get('amount')
		key = request.form['submit']
		c = con.cursor()
		c.execute("""SELECT s_places FROM proc_schema.timetable WHERE s_time LIKE '%s';""" %key)
		old_am = c.fetchall()
		old_am = int(old_am[0][0])
		amount = str(old_am - int(amount))
		c.execute("""UPDATE proc_schema.timetable SET s_places=%s WHERE s_time LIKE '%s';""" %(amount, key))
		con.commit()
		return render_template('/booking_answ.html')

app.run(port=5001,host="0.0.0.0",debug=True)