from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='crud_py'
)

@app.route('/')
def lista_personas():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    personas = cursor.fetchall()
    cursor.close()
    return render_template('lista_personas.html', personas=personas)

@app.route('/agregar_persona', methods=['GET', 'POST'])
def agregar_persona():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']

        cursor = db.cursor()
        cursor.execute('INSERT INTO personas (nombre, apellido, correo, contrasena, telefono) VALUES (%s, %s, %s, %s, %s)', (nombre, apellido, correo, contrasena, telefono))
        db.commit()
        cursor.close()

        flash(f'Nombre de la persona {nombre}, se enviaron los datos con éxito.', 'success')
        return redirect(url_for('lista_personas'))

    return render_template('agregar_persona.html')

@app.route('/editar_persona/<int:id>', methods=['GET', 'POST'])
def editar_persona(id):
    cursor = db.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']

        cursor.execute('UPDATE personas SET nombre = %s, apellido = %s, correo = %s, contrasena = %s, telefono = %s WHERE id = %s',
                       (nombre, apellido, correo, contrasena, telefono, id))
        db.commit()

        flash(f'Los datos de la persona se actualizaron con éxito.', 'success')
        return redirect(url_for('lista_personas'))

    cursor.execute('SELECT * FROM personas WHERE id = %s', (id,))
    persona = cursor.fetchone()
    cursor.close()

    return render_template('editar_persona.html', persona=persona)

@app.route('/eliminar_persona/<int:id>', methods=['POST'])
def eliminar_persona(id):
    cursor = db.cursor()

    cursor.execute('DELETE FROM personas WHERE id = %s', (id,))
    db.commit()

    flash(f'La persona se eliminó con éxito.', 'success')
    return redirect(url_for('lista_personas'))

if __name__ == '__main__':
    app.run(debug=True)
