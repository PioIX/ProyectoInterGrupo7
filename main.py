from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import time
from flask_cors import CORS
from flask import session

app = Flask(__name__)
cors = CORS(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

tematica = ""
dificultad = 0
id = 0
preguntaActual = 0
puntos = 0


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
    session['puntos'] = 0
    conn = sqlite3.connect('tabla.db')
    if (request.method == "POST"):
        if (request.form["usuario"] != ""):
            nombre = request.form['usuario']
            usuario = Persona(nombre)
            session['usuarioGlobal'] = usuario.nombre
            msg = nombre
            #ES PARA VER SI YA EXISTE ESE NOMBRE
            q = f"""SELECT nombre FROM Usuarios WHERE nombre = '{usuario.nombre}'"""
            resu = conn.execute(q)

            if resu.fetchone():
                mensaje = '¡ESE USUARIO YA EXISTE!'
                return render_template('index.html', mensaje = mensaje)
            else:
                r = f"""INSERT INTO Usuarios (nombre, tiempo, puntaje)
                  VALUES ('{usuario.nombre}','0',0);"""
                conn.execute(r)
                conn.commit()
            conn.close()
    else:
        if (request.method == "GET"):
            msg = "Hola"
        else:
            msg = "Chau"
    start = time.time()
    session['tiempoInicio'] = start
    return render_template('niveles.html', nombre=msg)


@app.route('/nivel/<num_nivel>')
def nivel(num_nivel):
    session['dificultad'] = int(num_nivel)
    session['preguntaActual'] = 0
    session['datoActual'] = 0
    pregu.dificultad = dificultad
    return render_template('tematica.html')

@app.route('/tematica/<tema>')
def tematica(tema):
    pregu.tema = tema
    session['tema'] = tema
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT contenido, id_pregunta, dato FROM Preguntas WHERE  dificultad == {session['dificultad']} and tema == '{pregu.tema}' """   
    resu = conn.execute(q)
    lista = resu.fetchall()
    num_dato = int(session['datoActual'])
    num_pregunta = int(session['preguntaActual'])
    if session['dificultad'] == 1:
      if num_pregunta < 5:  
        dato = lista[num_dato][2]
        session['dato'] = dato
        session['datoActual'] = num_dato + 1 
        pregunta = lista[num_pregunta]
        session['preguntaActual'] = num_pregunta + 1 
      else:
        return redirect(url_for('ranking'))
    else:
      if num_pregunta < 10:  
        dato = lista[num_dato][2]
        session['dato'] = dato
        session['datoActual'] = num_dato + 1 
        pregunta = lista[num_pregunta]
        session['preguntaActual'] = num_pregunta + 1 
      else:
        return redirect(url_for('ranking'))
       
    q = f"""SELECT contenido, correcta FROM Respuestas WHERE id_pregunta = {lista[num_pregunta][1]} """
    resu = conn.execute(q)
    lista_r = resu.fetchall()
    opcion1 = lista_r[0]
    session['opcion1'] = opcion1[1]
    opcion2 = lista_r[1]
    session['opcion2'] = opcion2[1]
    opcion3 = lista_r[2]
    session['opcion3'] = opcion3[1]
    opcion4 = lista_r[3]
    session['opcion4'] = opcion4[1]
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
  if session['opcion1'] == 'True':
    session['respuesta'] = "¡CORRECTO!"
    if session['dificultad'] == 1:
      session['puntos'] = session['puntos'] + 1
    else:
      session['puntos'] = session['puntos'] + 2
  else:
    session['respuesta'] = "¡INCORRECTO!"
  return redirect(url_for('datos'))

@app.route('/opcion2')
def opcion2():
  if session['opcion2'] == 'True':
    session['respuesta'] = "¡CORRECTO!"
    if session['dificultad'] == 1:
      session['puntos'] = session['puntos'] + 1
    else:
      session['puntos'] = session['puntos'] + 2
  else:
    session['respuesta'] = "¡INCORRECTO!"
  return redirect(url_for('datos'))

@app.route('/opcion3')
def opcion3():
  if session['opcion3'] == 'True':
    session['respuesta'] = "¡CORRECTO!"
    if session['dificultad'] == 1:
      session['puntos'] = session['puntos'] + 1
    else:
      session['puntos'] = session['puntos'] + 2
  else:
    session['respuesta'] = "¡INCORRECTO!"
  return redirect(url_for('datos'))

@app.route('/opcion4')
def opcion4():
  if session['opcion4'] == 'True':
    session['respuesta'] = "¡CORRECTO!"
    if session['dificultad'] == 1:
      session['puntos'] = session['puntos'] + 1
    else:
      session['puntos'] = session['puntos'] + 2
  else:
    session['respuesta'] = "¡INCORRECTO!"
  return redirect(url_for('datos'))


@app.route('/datos')
def datos():
    return render_template('datos.html', dato = session['dato'], 
                                        respuesta = session['respuesta'])

@app.route('/puntaje')
def ranking():
  end = time.time()
  session['tiempoFinal'] = end
  tiempo = format(session['tiempoFinal']-session['tiempoInicio'])
  tiempo = float(tiempo)
  con_dos_decimales = round(tiempo, 2)

  conn = sqlite3.connect('tabla.db')
  q = f"""SELECT nombre, tiempo, puntaje FROM Usuarios ORDER BY puntaje DESC LIMIT 5  """   
  resu = conn.execute(q)
  lista = resu.fetchall()
  nombre1 = lista[0][0]
  tiempo1 = lista[0][1]
  puntaje1 = lista[0][2]
  nombre2 = lista[1][0]
  tiempo2 = lista[1][1]
  puntaje2 = lista[1][2]
  nombre3 = lista[2][0]
  tiempo3 = lista[2][1]
  puntaje3 = lista[2][2]
  nombre4 = lista[3][0]
  tiempo4 = lista[3][1]
  puntaje4 = lista[3][2]
  nombre5 = lista[4][0]
  tiempo5 = lista[4][1]
  puntaje5 = lista[4][2]
  
  q = f"""UPDATE Usuarios SET puntaje = '{session['puntos']}' WHERE nombre = '{session['usuarioGlobal']}' """
  conn.execute(q)
  conn.commit()
  conn.close() 
  return render_template('ranking.html', 
                         puntaje = session['puntos'], 
                         nombre = session['usuarioGlobal'], 
                         tiempo = con_dos_decimales, 
                         top1 = puntaje1, 
                         top2 = puntaje2, 
                         top3 = puntaje3, 
                         top4 = puntaje4, 
                         top5 = puntaje5, 
                         nombre1 = nombre1, 
                         nombre2 = nombre2, 
                         nombre3 = nombre3, 
                         nombre4 = nombre4, 
                         nombre5 = nombre5,
                         tiempo1 = tiempo1, 
                         tiempo2 = tiempo2, 
                         tiempo3 = tiempo3, 
                         tiempo4 = tiempo4, 
                         tiempo5 = tiempo5)

app.run(host='0.0.0.0', port=81)
