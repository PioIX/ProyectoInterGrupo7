from flask import Flask, render_template, request
import sqlite3
from flask_cors import CORS
from flask import session

app = Flask(__name__)
cors = CORS(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

tematica = ""
dificultad = 0
id = 0


class Persona:
    def __init__(self, nombre=''):
        self.id_usuario = 1
        self.nombre = nombre
        self.tiempo = 0
        self.puntaje = 0


class Pregunta:
    def __init__(self, tema='', dificultad=''):
        self.id = 0
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
    if (request.method == "POST"):
        if (request.form["usuario"] != ""):
            
            nombre = request.form['usuario']
            usuario = Persona(nombre)
            session['usuarioGlobal'] = usuario
            msg = nombre
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
                print(r)
            conn.close()
    else:
        if (request.method == "GET"):
            msg = "Hola"
        else:
            msg = "Chau"
    return render_template('niveles.html', nombre=msg)


@app.route('/nivel1')
def nivel1():
    session['dificultad'] = 1
    pregu.dificultad = dificultad
    return render_template('tematica.html')


@app.route('/nivel2')
def nivel2():
    session['dificultad'] = 2
    pregu.dificultad = dificultad
    return render_template('tematica.html')


@app.route('/tematica1')
def tematica1():
    try:
        session['preguntaActual'] += 1
    except:
        session['preguntaActual'] = 0
    tema = "genero"
    pregu.tema = tema
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT contenido, id_pregunta FROM Preguntas WHERE  dificultad == {session['dificultad']} and tema == '{pregu.tema}' """
    resu = conn.execute(q)
    lista = resu.fetchall()
    pregunta = lista[0]
    q = f"""SELECT contenido, correcto, id_respuesta FROM Respuestas WHERE id_pregunta = {lista[0][1]} """
    resu = conn.execute(q)
    lista_r = resu.fetchall()
    opcion1 = lista_r[0]
    opcion2 = lista_r[1]
    opcion3 = lista_r[2]
    opcion4 = lista_r[3]
    conn.commit()
    conn.close()
    return render_template('pregunta.html',
                           pregunta=pregunta[0],
                           opcion1=opcion1[0],
                           opcion2=opcion2[0],
                           opcion3=opcion3[0],
                           opcion4=opcion4[0])


@app.route('/tematica2')
def tematica2():
    try:
        session['preguntaActual'] += 1
    except:
        session['preguntaActual'] = 0
    tema = "etnia"
    pregu.tema = tema
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT contenido, id_pregunta FROM Preguntas WHERE  dificultad == {session['dificultad']} and tema == '{pregu.tema}' """
    resu = conn.execute(q)
    lista = resu.fetchall()
    pregunta = lista[0]
    q = f"""SELECT contenido FROM Respuestas WHERE id_pregunta = {lista[0][1]} """
    resu = conn.execute(q)
    lista_r = resu.fetchall()
    opcion1 = lista_r[0]
    opcion2 = lista_r[1]
    opcion3 = lista_r[2]
    opcion4 = lista_r[3]
    conn.commit()
    conn.close()
    return render_template('pregunta.html',
                           pregunta=pregunta[0],
                           opcion1=opcion1[0],
                           opcion2=opcion2[0],
                           opcion3=opcion3[0],
                           opcion4=opcion4[0])


@app.route('/tematica3')
def tematica3():
    try:
        session['preguntaActual'] += 1
    except:
        session['preguntaActual'] = 0
    tema = "educacion"
    pregu.tema = tema
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT contenido, id_pregunta FROM Preguntas WHERE  dificultad == {session['dificultad']} and tema == '{pregu.tema}' """
    resu = conn.execute(q)
    lista = resu.fetchall()
    pregunta = lista[0]
    q = f"""SELECT contenido FROM Respuestas WHERE id_pregunta = {lista[0][1]} """
    resu = conn.execute(q)
    lista_r = resu.fetchall()
    opcion1 = lista_r[0]
    opcion2 = lista_r[1]
    opcion3 = lista_r[2]
    opcion4 = lista_r[3]
    conn.commit()
    conn.close()
    return render_template('pregunta.html',
                           pregunta=pregunta[0],
                           opcion1=opcion1[0],
                           opcion2=opcion2[0],
                           opcion3=opcion3[0],
                           opcion4=opcion4[0])


@app.route('/pregunta')
def pregunta():
    return render_template('pregunta.html')

@app.route('/opcion1')
def opcion1():
  conn = sqlite3.connect('tabla.db')
  q = f"""SELECT coreecto FROM Respuestas WHERE id_respuesta = {lista[0][1]} """
  conn.commit()
  conn.close()
  return render_template('datos.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')


@app.route('/puntaje')
def cargarDatos():
    conn = sqlite3.connect('tabla.db')
    session['puntajeGlobal'] = 11
    q = f"""UPDATE Usuarios SET usuario.puntaje = '{session['puntajeGlobal']}' WHERE usuario.nombre = '{session['usuarioGlobal']}';"""

    conn.execute(q)
    conn.commit()


'''
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
