from flask import Flask, request, jsonify, render_template  # Importa render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_datos import Base, Persona
from datetime import datetime


app = Flask(__name__)

# Conectar a la base de datos
engine = create_engine('sqlite:///consultorio_veterinario.db')
Session = sessionmaker(bind=engine)
session = Session()

# Rutas de la API
@app.route('/personas', methods=['GET'])
def get_personas():
    personas = session.query(Persona).all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'fecha_nacimiento': p.fecha_nacimiento.isoformat() if p.fecha_nacimiento else None,
        'sexo': p.sexo,
        'correo': p.correo,
        'telefono': p.telefono,
        'domicilio': p.domicilio
    } for p in personas])

@app.route('/personas/<int:id>', methods=['GET'])
def get_persona(id):
    persona = session.query(Persona).filter(Persona.id == id).first()
    if persona:
        return jsonify({
            'id': persona.id,
            'nombre': persona.nombre,
            'fecha_nacimiento': persona.fecha_nacimiento.isoformat() if persona.fecha_nacimiento else None,
            'sexo': persona.sexo,
            'correo': persona.correo,
            'telefono': persona.telefono,
            'domicilio': persona.domicilio
        })
    return jsonify({'error': 'Persona no encontrada'}), 404

@app.route('/personas', methods=['POST'])
def create_persona():
    data = request.get_json()
    fecha_nacimiento_str = data.get('fecha_nacimiento')
    if fecha_nacimiento_str:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Fecha de nacimiento inválida. Debe ser en formato YYYY-MM-DD.'}), 400
    else:
        fecha_nacimiento = None

    nueva_persona = Persona(
        nombre=data['nombre'],
        fecha_nacimiento=fecha_nacimiento,
        sexo=data.get('sexo'),
        correo=data['correo'],
        telefono=data.get('telefono'),
        domicilio=data.get('domicilio')
    )

    session.add(nueva_persona)
    session.commit()
    return jsonify({'id': nueva_persona.id}), 201

@app.route('/personas/<int:id>', methods=['PUT'])
def update_persona(id):
    data = request.get_json()
    persona = session.query(Persona).filter(Persona.id == id).first()
    if persona:
        persona.nombre = data.get('nombre', persona.nombre)
        persona.fecha_nacimiento = data.get('fecha_nacimiento', persona.fecha_nacimiento)
        persona.sexo = data.get('sexo', persona.sexo)
        persona.correo = data.get('correo', persona.correo)
        persona.telefono = data.get('telefono', persona.telefono)
        persona.domicilio = data.get('domicilio', persona.domicilio)
        session.commit()
        return jsonify({'message': 'Persona actualizada'})
    return jsonify({'error': 'Persona no encontrada'}), 404

@app.route('/personas/<int:id>', methods=['DELETE'])
def delete_persona(id):
    persona = session.query(Persona).filter(Persona.id == id).first()
    if persona:
        session.delete(persona)
        session.commit()
        return jsonify({'message': 'Persona eliminada'})
    return jsonify({'error': 'Persona no encontrada'}), 404

# Ruta para servir el archivo HTML
@app.route('/')
def index():
    return render_template('index.html')  # Cambiado a render_template

if __name__ == '__main__':
    app.run(debug=True)
