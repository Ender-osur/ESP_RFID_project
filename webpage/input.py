from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flaskext.mysql import MySQL
import json
from decouple import config
global i

i=1
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2515'
app.config['MYSQL_DATABASE_DB'] = 'base_datos'
mysql.init_app(app)

@app.route('/', methods=["POST", "GET"])
def index():
	import mysql.connector
	from mysql.connector import Error
	conexion=mysql.connector.connect(
		host='localhost',
		user='root',
		password='2515',
		db='base_datos',
	)
	cur=conexion.cursor()
	cur.execute('select * from registro')
	datos=cur.fetchall()
	if datos[i][0] == "Por favor inciar sesión":
		return render_template("index.html",nombre="Por favor inicia sesión", id="0", saldo=0)
	else:
		cur=conexion.cursor()
		cur.execute('select * from registro')
		datos=cur.fetchall()
		print(datos)
		if conexion.is_connected():
			print('Seh')
		if request.method=="POST":
			saldo=int(request.form['saldo'])
			print(saldo)
			cur.execute(f'update registro set saldo = saldo + {saldo} where tel = "{datos[i][1]}"')

		conexion.commit()
		return render_template("index.html",nombre=datos[i][0], tel=datos[i][1], saldo=datos[i][3])



@app.route('/registro', methods=["GET", "POST"])
def registro():
	import mysql.connector
	from mysql.connector import Error
	conexion=mysql.connector.connect(
		host=('localhost'),
		user=('root'),
		password=('2515'),
		db=('base_datos'),
	)
	if conexion.is_connected():
		print('Seh')

	cur=conexion.cursor()
	if request.method == "POST":
		nombre=request.form['nombre']
		cur.execute(f'insert into registro (rfid, nombre, saldo) values ("oxooff", "{nombre}", "0")')
		conexion.commit()
		print("Register is save")
	conexion.close()
	return render_template("registro.html")

@app.route('/login', methods=["GET", "POST"])
def login():

	cur=mysql.get_db().cursor()
	cur.execute("select * from registro")
	datos=cur.fetchall()
	cur.close
	print('DATOS')

	if request.method == "POST":
		user=request.form['rfid']
		rango = range(0,len(datos))
		print(user)
		global i
		print(rango)
		
		for i in rango:
			print(datos[i][2])
			if datos[i][2]==user:
				
				return redirect(url_for('index'))
			else:
				print("nada")
				print(datos[i][2])
				#return render_template("login.html")

	return render_template("login.html")
if __name__ == "__main__":
	app.run(debug=True)
