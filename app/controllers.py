import requests
import json

from app import app, supabase_1, supabase_2
from flask import Flask, render_template, request, url_for, redirect, flash, Blueprint, g

#Blueprint de la aplicación
geproyeBp = Blueprint('app', __name__)

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        data = response.json()
        public_ip = data['ip']
        return public_ip
    else:
        return None

#Ruta que compara los datos de las dos bases de datos
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    proyectos_1 = supabase_1.table('proyecto').select("*").execute()
    proyectos_2 = supabase_2.table('proyecto').select("*").execute()
    proyectos_1_iteraciones = supabase_1.table('iteracion').select("*").execute()
    proyectos_2_iteraciones = supabase_2.table('iteracion').select("*").execute()
    proyectos_1_integrantes = supabase_1.table('integrante').select("*").execute()
    proyectos_2_integrantes = supabase_2.table('integrante').select("*").execute()
    proyectos_1_requisitos = supabase_1.table('requisito').select("*").execute()
    proyectos_2_requisitos = supabase_2.table('requisito').select("*").execute()
    return render_template('views/compare.html', proyectos_1=proyectos_1.data, proyectos_2=proyectos_2.data, proyectos_1_iteraciones=proyectos_1_iteraciones.data, proyectos_2_iteraciones=proyectos_2_iteraciones.data, proyectos_1_requisitos=proyectos_1_requisitos.data, proyectos_2_requisitos=proyectos_2_requisitos.data, proyectos_1_integrantes=proyectos_1_integrantes.data, proyectos_2_integrantes=proyectos_2_integrantes.data)

#Función que actualiza los datos de la base de datos de respaldo en base a la original
@app.route('/backup', methods=['GET','POST'])
def backup():
    proyectos_1 = supabase_1.table('proyecto').select("*").execute()
    dictionary_1 = proyectos_1.data
    proyectos_1_iteracion = supabase_1.table('iteracion').select("*").execute()
    dictionary_1_iteracion = proyectos_1_iteracion.data
    proyectos_1_requisito = supabase_1.table('requisito').select("*").execute()
    dictionary_1_requisito = proyectos_1_requisito.data
    proyectos_1_integrante = supabase_1.table('integrante').select("*").execute()
    dictionary_1_integrante = proyectos_1_integrante.data
    proyectos_2 = supabase_2.table('proyecto').select("id").execute()
    dictionary_2 = proyectos_2.data
    for list in dictionary_2:
        value = list['id']
        deleteProyecto = supabase_2.table("proyecto").delete().eq("id", value).execute()
        deleteIteracion = supabase_2.table("iteracion").delete().eq("id", value).execute()
        deleteIntegrante = supabase_2.table("integrante").delete().eq("id", value).execute()
        deleteRequisito = supabase_2.table("requisito").delete().eq("id", value).execute()
    for list in dictionary_1:
        insertProyecto = supabase_2.table("proyecto").insert(list).execute()
    for list in dictionary_1_iteracion:
        insertProyecto = supabase_2.table("iteracion").insert(list).execute()
    for list in dictionary_1_integrante:
        insertProyecto = supabase_2.table("integrante").insert(list).execute()
    for list in dictionary_1_requisito:
        insertProyecto = supabase_2.table("requisito").insert(list).execute()
    return redirect(url_for('compare'))

@app.route('/update2', methods=['GET','POST'])
def update2():
    proyectos_2 = supabase_2.table('proyecto').select("*").execute()
    dictionary_2 = proyectos_2.data
    proyectos_2_iteracion = supabase_2.table('iteracion').select("*").execute()
    dictionary_2_iteracion = proyectos_2_iteracion.data
    proyectos_2_requisito = supabase_2.table('requisito').select("*").execute()
    dictionary_2_requisito = proyectos_2_requisito.data
    proyectos_2_integrante = supabase_2.table('integrante').select("*").execute()
    dictionary_2_integrante = proyectos_2_integrante.data
    proyectos_1 = supabase_1.table('proyecto').select("id").execute()
    dictionary_1 = proyectos_1.data
    for list in dictionary_1:
        value = list['id']
        deleteProyecto = supabase_1.table("proyecto").delete().eq("id", value).execute()
        deleteIteracion = supabase_1.table("iteracion").delete().eq("id", value).execute()
        deleteIntegrante = supabase_1.table("integrante").delete().eq("id", value).execute()
        deleteRequisito = supabase_1.table("requisito").delete().eq("id", value).execute()
    for list in dictionary_2:
        insertProyecto = supabase_1.table("proyecto").insert(list).execute()
    for list in dictionary_2_iteracion:
        insertProyecto = supabase_1.table("iteracion").insert(list).execute()
    for list in dictionary_2_integrante:
        insertProyecto = supabase_1.table("integrante").insert(list).execute()
    for list in dictionary_2_requisito:
        insertProyecto = supabase_1.table("requisito").insert(list).execute()
    return redirect(url_for('compare'))

@app.route('/chat', methods=['GET'])
def chat():
    ip = get_public_ip()
    r = requests.post('http://192.168.1.114:25565/v1/discover', data={ 'email': 'ejemplo@gmail.com', 'ip': ip })
    response = requests.get('http://192.168.1.114:25565/v1/discover')
    chatUsers = response.json()
    print(ip)
    print(chatUsers)
    
    return render_template('views/index.html')

@app.route('/', methods=['GET'])
def index():    
    response = requests.get('http://190.92.148.107:7070/v1/project')
    proyectos = response.json()['data']
    
    return render_template('views/index.html', proyectos=proyectos)

@app.route('/crearProyecto', methods=['POST']) #LISTOCA
def crearProyecto():
    if request.method == 'POST':
        idproye = request.form['id']
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']        
        proyecto = {'id': idproye, 'nombre': nombre, 'fecha_inicio': fecha_inicio, 'fecha_termino': fecha_termino}
        #insert = g.db.table('proyecto').insert(proyecto).execute()
        response = requests.post('http://190.92.148.107:7070/v1/project', data=proyecto)
        if response.error: 
            flash('Error al crear proyecto: {}'.format(response.error), 'error')
        else:
            flash('Proyecto creado exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/eliminarProyecto/<int:id>', methods=['GET','POST']) #LISTOCA
def eliminarProyecto(id):
    proyecto = g.db.table('proyecto').delete().eq("id", id).execute()
    flash('Proyecto eliminado exitosamente', 'danger')
    return redirect(url_for('index'))

@app.route('/editarProyecto/<int:id>', methods=['GET','POST']) #LISTOCO
def editarProyecto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        estado = request.form['estado']
        update = g.db. table('proyecto').update({"nombre": nombre, "fecha_inicio": fecha_inicio, "fecha_termino":fecha_termino, "estado": estado}).eq("id", id).execute()
        flash('Proyecto editado exitosamente', 'info')
        return redirect(url_for('index'))
    proyecto = g.db.table('proyecto').select("*").eq("id", id).execute()
    return render_template('views/editarProy.html', proyecto=proyecto.data[0])

@app.route('/editarIteracion/<int:id>/<int:fk_proyecto>', methods=['GET','POST']) 
def editarInteracion(id,fk_proyecto):
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        update = g.db.table('iteracion').update({"fecha_inicio": fecha_inicio, "fecha_termino": fecha_termino}).eq("fk_proyecto", fk_proyecto).eq("id", id).execute()
        flash('Iteración editada exitosamente', 'info')
        return redirect(url_for('index'))
    iteracion = g.db.table('iteracion').select("*").eq("id", id).execute()
    proyecto = g.db.table('proyecto').select("*").eq("id", fk_proyecto).execute()
    return render_template('views/editarIteraciones.html', proyecto=proyecto.data[0], iteracion=iteracion.data[0])

@app.route('/<int:id>/iteraciones', methods=['GET','POST']) #LISTOCO
def iteraciones(id):
    if request.method == 'POST':
        fk_proyecto = id
        id_iteracion = request.form['id']
        fecha_inicio= request.form['fecha_inicio']
        fecha_termino=request.form['fecha_termino']
        iteracion = {'id': id_iteracion, 'fk_proyecto': fk_proyecto, 'fecha_inicio': fecha_inicio, 'fecha_termino':fecha_termino}
        insert = g.db.table('iteracion').insert(iteracion).execute()
        flash('Iteración creada exitosamente', 'success')
        return redirect(url_for('iteraciones', id=id))        
    #proyecto = g.db.table('proyecto').select("*").eq("id", id).order('id').execute()    
    #iteracion = g.db.table('iteracion').select("*").eq("fk_proyecto", id).order('id').execute()
    response_proyecto = requests.get('http://190.92.148.107:7070/v1/project/{}/'.format(id))
    response_iteraciones = requests.get('http://190.92.148.107:7070/v1/project/{}/iteracion'.format(id))
    proyecto = response_proyecto.json()['data'][0]
    return render_template('views/iteraciones.html', proyecto=proyecto, iteracion=iteracion.data)

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