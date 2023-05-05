from app import app, supabase_1, supabase_2
from flask import Flask, render_template, request, url_for, redirect, flash, Blueprint, g
import supabase

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

    # Save the connection to the global context
    g.db = connection

@app.route('/', methods=['GET','POST'])
def index():    
    proyectos = g.db.table('proyecto').select('id, nombre, fecha_inicio, fecha_termino, estado').order("id").execute()
    return render_template('views/index.html', proyectos=proyectos.data)

@app.route('/crearProyecto', methods=['POST']) #LISTOCA
def crearProyecto():
    if request.method == 'POST':
        idproye = request.form['id']
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']        
        proyecto = {'id': idproye, 'nombre': nombre, 'fecha_inicio': fecha_inicio, 'fecha_termino': fecha_termino}
        insert = g.db.table('proyecto').insert(proyecto).execute()
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

@app.route('/iteraciones/<int:id>', methods=['GET','POST']) #LISTOCO
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
    proyecto = g.db.table('proyecto').select("*").eq("id", id).order('id').execute()    
    iteracion = g.db.table('iteracion').select("*").eq("fk_proyecto", id).order('id').execute()
    return render_template('views/iteraciones.html', proyecto=proyecto.data[0], iteracion=iteracion.data)

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