from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Configuración inicial
Base = declarative_base()

# Tabla Persona
class Persona(Base):
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha_nacimiento = Column(Date)
    sexo = Column(String)
    correo = Column(String, unique=True)
    telefono = Column(String)
    domicilio = Column(String)
    
    # Relación con Mascotas
    mascotas = relationship("Mascota", back_populates="dueno")

# Tabla Especie
class Especie(Base):
    __tablename__ = 'especies'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    
    # Relación con Mascotas
    mascotas = relationship("Mascota", back_populates="especie")

# Tabla Mascota
class Mascota(Base):
    __tablename__ = 'mascotas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer)
    sexo = Column(String)
    peso = Column(Float)
    persona_id = Column(Integer, ForeignKey('personas.id'))
    especie_id = Column(Integer, ForeignKey('especies.id'))
    
    # Relación con Persona y Especie
    dueno = relationship("Persona", back_populates="mascotas")
    especie = relationship("Especie", back_populates="mascotas")

# Conectar con SQLite
engine = create_engine('sqlite:///consultorio_veterinario.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

print("Base de datos creada exitosamente.")




