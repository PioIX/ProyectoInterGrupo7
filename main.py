from flask import Flask, render_template, request
import sqlite3 
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

tematica = ""
dificultad = 0
id = 0

class Persona:
  def __init__(self, nombre=''):
    self.id_usuario = 1 
    self.nombre = nombre
    self.tiempo = 0
    self.puntaje= 0
      
class Pregunta:
  def __init__(self, tema='', dificultad=''):
    self.id_pregunta = 0 
    self.contenido = ""
    self.tema = ""
    self.dificultad = 0
    self.dato = ""

pregu = Pregunta()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/nosotras')
def nosotras():
  return render_template('nosotras.html')

@app.route('/reglas')
def reglas():
  return render_template('reglas.html')

@app.route('/niveles')
def niveles():
  return render_template('niveles.html')
  
@app.route('/signin', methods=['POST', 'GET'])
def signin():
  msg = None
  conn = sqlite3.connect('tabla.db')
  if (request.method=="POST"):
    if (request.form["usuario"]!=""):
      nombre=request.form['usuario']
      usuario=Persona(nombre)
      msg=nombre
      #ES PARA VER SI YA EXISTE ESE NOMBRE
      q = f"""SELECT nombre FROM Usuarios WHERE nombre = '{usuario.nombre}'"""
      resu = conn.execute(q)
      #probar si funciona ver si ya existe el nombre
 
      if resu.fetchone():
        print("ya existe")
      else:
        r = f"""INSERT INTO Usuarios (nombre, tiempo, puntaje)
                  VALUES ('{usuario.nombre}','0',0);"""
        conn.execute(r)
        conn.commit() 
  else:
      if (request.method=="GET"):
        msg="Hola"
      else:
        msg="Chau"
  return render_template('niveles.html', nombre=msg) 

@app.route('/nivel1')
def nivel1():
  dificultad = 1
  pregu.dificultad = dificultad
  return render_template('tematica.html')

@app.route('/nivel2')
def nivel2():
  dificultad = 2
  pregu.dificultad = dificultad
  return render_template('tematica.html')


@app.route('/tematica1')
def tematica1():
  tema = "genero"
  pregu.tema = tema
  return render_template('pregunta.html')

@app.route('/tematica2')
def tematica2():
  tema = "etnia"
  pregu.tema = tema
  print(pregu.dificultad)
  print(pregu.tema)
  conn = sqlite3.connect('tabla.db')
#https://docs.python.org/3.7/library/sqlite3.html
  q = f"""SELECT contenido FROM Preguntas WHERE id_pregunta = {pregu.id_pregunta} and dificultad == {pregu.dificultad} and tema == '{pregu.tema}' """
  print(q)
  resu = conn.execute(q)
  print(resu)
  conn.commit() 
  pregu.id_pregunta =+ 1
  return render_template('prueba.html', pregunta=resu)

@app.route('/tematica3')
def tematica3():
  tema = "educacion"
  pregu.tema = tema
  return render_template('pregunta.html')


@app.route('/preguntas')
def cargarPregunta():
  pregunta+=1
  conn = sqlite3.connect('tabla.db')
  q = f"""SELECT contenido FROM Preguntas WHERE nivel = '{pregunta.dificultad}' and tematica = '{pregunta.tema}' """
  resu = conn.execute(q)
  for fila in resu:
    return(fila)
  conn.close()
  conn.commit() 
  return render_template('prueba.html', fila=pregunta)

'''
hola
  def cargarDatos():
   conn = sqlite3.connect('tabla.db')
  #falta calcular tiempo final y puntaje
  #tiempo_final = 0
  #puntajeObtenido = 10 
  q = f"""UPDATE Usuarios SET tiempo = '{tiempo_final}', puntaje = '{puntajeObtenido}' WHERE id_usuario = '{usuario.id_usuario}';"""
  conn.execute(q)
  conn.commit()
''' 
app.run(host='0.0.0.0', port=81)