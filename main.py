import os
from flask import Flask, render_template, request, url_for, redirect, session, flash
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'vdsajjaqwjnksdivk'

#Inicializar cliente supabase
supabase_url = 'https://eaitbimlcshobgdjzttc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhaXRiaW1sY3Nob2JnZGp6dHRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk5NjExNTksImV4cCI6MTk5NTUzNzE1OX0.rk_9XJgZ1x3oaEfKJs8pmb3tnlrMxByFDfG8EGUMXOI'
supabase: Client = create_client(supabase_url, supabase_key)

#Rutas
@app.route('/', methods=['GET','POST'])
def index():    
    proyectos = supabase.table('proyecto').select('id, nombre, fecha_inicio, fecha_termino, estado').execute()
    return render_template('views/index.html', proyectos=proyectos.data)

@app.route('/crearProyecto', methods=['POST'])
def crearProyecto():
    if request.method == 'POST':
        idproye = request.form['id']
        nombre = request.form['nombre']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        proyecto = {'id': idproye, 'nombre': nombre, 'fecha_inicio': fecha_inicio, 'fecha_termino': fecha_termino, 'estado': False }
        insert = supabase.table('proyecto').insert(proyecto).execute()
        flash('Proyecto eliminado exitosamente', 'info')
    return redirect(url_for('index'))

@app.route('/iteraciones/<int:id>', methods=['GET','POST'])
def iteraciones(id):
    proyecto = supabase.table('proyecto').select("*").eq("id", id).execute()    
    return render_template('views/iteraciones.html', proyecto=proyecto)

@app.route('/editarProy/<int:id>', methods=['GET','POST'])
def editar(id):
    proyecto = supabase.table('proyecto').select("*").eq("id", id).execute()
    print(proyecto.data[0])
    return render_template('views/editarProy.html', proyecto=proyecto.data[0])

@app.route('/eliminarProy/<int:id>', methods=['GET','POST'])
def eliminar(id):
    proyecto = supabase.table('proyecto').delete().eq("id", id).execute()
    flash('Proyecto eliminado exitosamente', 'danger')
    return redirect(url_for('index'))

if __name__ =="__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
