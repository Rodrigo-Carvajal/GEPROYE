import requests
import json

from app import app, supabase_1, supabase_2
from flask import Flask, render_template, request, url_for, redirect, flash, Blueprint, g

#Blueprint de la aplicación
geproyeBp = Blueprint('app', __name__)

#Middleware que conecta a la otra base de datos
@app.before_request
def before_request():
    try:
        connection = supabase_1
        response = connection.table('proyecto').select("*").execute()
        if response:
            g.db = connection
            print("¡Conectado a la primera base de datos!")
        else:
            raise Exception('¡Conexión fallida!')            
    except Exception as e:
        print(f"El intento de conexión a la primera base de datos arrojó el siguiente error:\n{e}")
        connection = supabase_2
        print("¡Conectado a la base de datos de respaldo!")
    # Guarda la conexión en un contexto global a través de g
    g.db = connection

@app.route('/', methods=['GET'])
def index():    
    #proyectos = g.db.table('proyecto').select('id, nombre, fecha_inicio, fecha_termino, estado').order("id").execute()
    response = requests.get('http://190.92.148.107:7070/v1/project')
    proyectos = response.json()['data']
    return render_template('views/index.html', proyectos=proyectos)

@app.route('/crearProyecto', methods=['POST']) #LISTOCA
def crearProyecto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']        
        proyecto = {'nombre': nombre, 'fechaInicio': fecha_inicio, 'fechaTermino': fecha_termino, 'estado': "Creado"}
        #insert = g.db.table('proyecto').insert(proyecto).execute()
        insert = requests.post('http://190.92.148.107:7070/v1/project/', data=proyecto)
        flash('Proyecto creado exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/eliminarProyecto/<int:id>', methods=['GET','POST']) #LISTOCA
def eliminarProyecto(id):
    #proyecto = g.db.table('proyecto').delete().eq("id", id).execute()
    delete = requests.delete('http://190.92.148.107:7070/v1/project/{}/'.format(id))
    flash('Proyecto eliminado exitosamente', 'danger')
    return redirect(url_for('index'))

@app.route('/editarProyecto/<int:id>', methods=['GET','POST']) #LISTOCO
def editarProyecto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        estado = request.form['estado']
        edit = {'nombre': nombre, 'fechaInicio': fecha_inicio, 'fechaTermino': fecha_termino, 'estado': estado}
        #update = g.db. table('proyecto').update({"nombre": nombre, "fecha_inicio": fecha_inicio, "fecha_termino":fecha_termino, "estado": estado}).eq("id", id).execute()
        update = requests.patch('http://190.92.148.107:7070/v1/project/{}/'.format(id), data=edit)
        flash('Proyecto editado exitosamente', 'info')
        return redirect(url_for('index'))
    #proyecto = g.db.table('proyecto').select("*").eq("id", id).execute()
    response = requests.get('http://190.92.148.107:7070/v1/project/{}/'.format(id))
    proyecto = response.json()['data']
    return render_template('views/editarProy.html', proyecto=proyecto[0])

@app.route('/editarIteracion/<int:id>/<int:fk_proyecto>', methods=['GET','POST']) 
def editarInteracion(id,fk_proyecto):
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        edit = {'fechaInicio' : fecha_inicio, 'fechaTermino' : fecha_termino}
        #update = g.db.table('iteracion').update({"fecha_inicio": fecha_inicio, "fecha_termino": fecha_termino}).eq("fk_proyecto", fk_proyecto).eq("id", id).execute()
        update = requests.patch('http://190.92.148.107:7070/v1/project/{}/iteration/{}/'.format(id, fk_proyecto))
        flash('Iteración editada exitosamente', 'info')
        return redirect(url_for('index'))
    #iteracion = g.db.table('iteracion').select("*").eq("id", id).execute()
    response1 = requests.get('http://190.92.148.107:7070/v1/project/{}/iteration/{}/'.format(fk_proyecto, id))
    print(response1.json())
    #proyecto = g.db.table('proyecto').select("*").eq("id", fk_proyecto).execute()
    response2 = requests.get('http://190.92.148.107:7070/v1/project/{}/'.format(fk_proyecto))
    print(response2.json())
    iteracion = response1.json()['data']
    proyecto = response2.json()['data']
    print(iteracion)
    print(proyecto)
    return render_template('views/editarIteraciones.html', proyecto=proyecto, iteracion=iteracion)

@app.route('/iteraciones/<int:id>', methods=['GET','POST']) #LISTOCO
def iteraciones(id):
    if request.method == 'POST':
        fecha_inicio= request.form['fecha_inicio']
        fecha_termino=request.form['fecha_termino']
        create = {'fechaInicio': fecha_inicio, 'fechaTermino':fecha_termino}
        #insert = g.db.table('iteracion').insert(iteracionn).execute()
        update = requests.post('http://190.92.148.107:7070/v1/project/{}/iteration/'.format(id), data=create)
        flash('Iteración creada exitosamente', 'success')
        return redirect(url_for('iteraciones', id=id))        
    #proyecto = g.db.table('proyecto').select("*").eq("id", id).order('id').execute()    
    #iteracion = g.db.table('iteracion').select("*").eq("fk_proyecto", id).order('id').execute()
    response_proyecto = requests.get('http://190.92.148.107:7070/v1/project/{}/'.format(id))
    response_iteraciones = requests.get('http://190.92.148.107:7070/v1/project/{}/iteration'.format(id))
    proyecto = response_proyecto.json()['data'][0]
    iteracion = response_iteraciones.json()['data']
    return render_template('views/iteraciones.html', proyecto=proyecto, iteracion=iteracion)

@app.route('/eliminarIteracion/<int:id>/<int:fk_proyecto>', methods=['GET','POST']) #Listoco
def eliminarInteraciones(id,fk_proyecto):
    integrante = g.db.table('iteracion').delete().eq("id", id).eq("fk_proyecto", fk_proyecto).execute()
    flash('Iteracion eliminado exitosamente', 'danger')
    return redirect(url_for('iteraciones', id=fk_proyecto))

@app.route('/requisitos/<int:id>', methods=['GET', 'POST']) #LISTOCO
def requisitos(id):
    proyecto = g.db.table('proyecto').select("*").eq("id", id).execute()
    requisitos = g.db.table('requisito').select("*").eq("fk_proyecto", id).order('id').execute()
    return render_template('views/requisitos.html', proyecto=proyecto.data[0], requisitos=requisitos.data)

@app.route('/crearRequisito/<int:id>', methods=['GET', 'POST']) #LISTOCO
def crearRequisito(id):
    if request.method == 'POST':
        idreq = request.form['id']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        requisito = {"id": idreq, "fk_proyecto": id, "tipo": tipo, "descripcion": descripcion}
        insert = g.db.table('requisito').insert(requisito).execute()
        flash('Requisito creado exitosamente', 'success')
        return redirect(url_for('requisitos', id=id))
    proyecto = g.db.table('proyecto').select("*").eq("id", id).execute()
    return redirect(url_for('requisitos', id=id)) #Así se pueden asignar las vistas en vez de tener que mandarlos a index

@app.route('/editarRequisito/<int:fk_proyecto>/<int:id>', methods=['GET', 'POST']) #LISTOCO
def editarRequisito(fk_proyecto, id):
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        update = g.db.table('requisito').update({"tipo": tipo,"descripcion": descripcion}).eq("fk_proyecto", fk_proyecto).eq("id", id).execute()
        flash('Requisito editado exitosamente', 'info')
        return redirect(url_for('requisitos', id=id))
    requisito = g.db.table('requisito').select("*").eq("id", id).execute()
    proyecto = g.db.table('proyecto').select("*").eq("id", fk_proyecto).execute()
    return render_template('views/editarRequisito.html', requisito=requisito.data[0], proyecto=proyecto.data[0])

@app.route('/eliminarRequisito/<int:fk_proyecto>/<int:id>', methods=['GET', 'POST']) #LISTOCO
def eliminarRequisito(fk_proyecto, id):
    delete = g.db.table('requisito').delete().eq("id", id).eq("fk_proyecto", fk_proyecto).execute()
    flash('Requisito eliminado exitosamente', 'danger')
    return redirect(url_for('requisitos', id=fk_proyecto))

@app.route('/integrantes/<int:id>', methods=['GET','POST']) #LISTOCO
def integrantes(id):
    if request.method == 'POST':
        id_integrante = request.form['id']
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        integrante = {'fk_proyecto': id, 'id':id_integrante, 'nombre': nombre, 'cargo':cargo}
        insert = g.db.table('integrante').insert(integrante).execute()
    proyecto = g.db.table('proyecto').select("*").eq("id", id).order('id').execute()
    integrantes = g.db.table('integrante').select("*").eq("fk_proyecto", id).order('id').execute()
    return render_template('views/integrantes.html', proyecto=proyecto.data[0], integrantes=integrantes.data)

@app.route('/editarIntegrante/<int:fk_proyecto>/<int:id>', methods=['GET','POST']) #LISTOCO
def editarIntegrante(fk_proyecto, id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        update = g.db.table('integrante').update({"nombre": nombre, "cargo": cargo}).eq("fk_proyecto", fk_proyecto).eq("id", id).execute()
        return redirect(url_for('index'))
    integrante = g.db.table('integrante').select("*").eq("id", id).execute()
    proyecto = g.db.table('proyecto').select("*").eq("id", fk_proyecto).execute()
    return render_template('views/editarIntegrante.html', proyecto=proyecto.data[0], integrante=integrante.data[0])

@app.route('/eliminarIntegrante/<int:fk_proyecto>/<int:id>', methods=['GET','POST']) #LISTOCO
def eliminarIntegrante(fk_proyecto, id):
    delete = g.db.table('integrante').delete().eq("id", id).eq("fk_proyecto", fk_proyecto).execute()
    flash('Usuario eliminado exitosamente', 'danger')
    return redirect(url_for('integrantes', id=fk_proyecto))