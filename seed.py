import hashlib
import uuid
from datetime import datetime, timezone
from app.database import SessionLocal, engine, Base
from app.models.carrera import Carrera
from app.models.contacto import Contacto
from app.models.lugar import Lugar
from app.models.pago import Pago
from app.models.profesor import Profesor
from app.models.usuario import Usuario
from app.models.curso import Curso
from app.models.evento import Evento
from app.models.servicio import Servicio

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def run():
    db = SessionLocal()

    # si ya existe el admin, el seed ya corrió — no hace nada
    if db.query(Usuario).filter(Usuario.email == "admin@uvg.edu.gt").first():
        print("Seed ya aplicado, omitiendo.")
        db.close()
        return

    # limpia tablas en orden para respetar foreign keys
    db.query(Servicio).delete()
    db.query(Evento).delete()
    db.query(Curso).delete()
    db.query(Usuario).delete()
    db.query(Profesor).delete()
    db.query(Pago).delete()
    db.query(Lugar).delete()
    db.query(Contacto).delete()
    db.query(Carrera).delete()
    db.commit()

    # carreras
    computacion = Carrera(id=uuid.uuid4(), nombre="Ingeniería en Ciencias de la Computación", facultad="Ingeniería", duracion_semestres=9)
    mecatronica = Carrera(id=uuid.uuid4(), nombre="Ingeniería Mecatrónica", facultad="Ingeniería", duracion_semestres=9)
    administracion = Carrera(id=uuid.uuid4(), nombre="Administración de Empresas", facultad="Económicas", duracion_semestres=8)
    medicina = Carrera(id=uuid.uuid4(), nombre="Medicina", facultad="Salud", duracion_semestres=12)
    db.add_all([computacion, mecatronica, administracion, medicina])
    db.commit()

    # contactos
    contacto_registro = Contacto(id=uuid.uuid4(), nombre="Departamento de Registro", cargo="Registro Académico", email="registro@uvg.edu.gt", telefono="2364-0336", extension="1200", departamento="Registro")
    contacto_biblioteca = Contacto(id=uuid.uuid4(), nombre="Biblioteca Central", cargo="Servicios Bibliotecarios", email="biblioteca@uvg.edu.gt", telefono="2364-0336", extension="1300", departamento="Biblioteca")
    contacto_it = Contacto(id=uuid.uuid4(), nombre="Soporte Tecnológico", cargo="Soporte IT", email="soporte@uvg.edu.gt", telefono="2364-0336", extension="1400", departamento="TI")
    contacto_bienestar = Contacto(id=uuid.uuid4(), nombre="Bienestar Estudiantil", cargo="Orientación", email="bienestar@uvg.edu.gt", telefono="2364-0336", extension="1500", departamento="Bienestar")
    db.add_all([contacto_registro, contacto_biblioteca, contacto_it, contacto_bienestar])
    db.commit()

    # lugares
    biblioteca = Lugar(id=uuid.uuid4(), nombre="Biblioteca Central", descripcion="Biblioteca principal del campus con acceso a bases de datos académicas.", edificio="Edificio D", piso="1", categoria="Académico", horario_apertura="07:00", horario_cierre="21:00")
    cafeteria = Lugar(id=uuid.uuid4(), nombre="Cafetería Central", descripcion="Servicio de alimentación principal del campus.", edificio="Edificio A", piso="1", categoria="Servicios", horario_apertura="07:00", horario_cierre="18:00")
    laboratorio = Lugar(id=uuid.uuid4(), nombre="Laboratorio de Computación", descripcion="Laboratorio con 60 computadoras para uso estudiantil.", edificio="Edificio F", piso="2", categoria="Laboratorio", horario_apertura="08:00", horario_cierre="20:00")
    auditorio = Lugar(id=uuid.uuid4(), nombre="Auditorio Principal", descripcion="Auditorio con capacidad para 500 personas.", edificio="Edificio B", piso="1", categoria="Eventos", horario_apertura="08:00", horario_cierre="22:00")
    db.add_all([biblioteca, cafeteria, laboratorio, auditorio])
    db.commit()

    # pagos (sin relaciones)
    db.add_all([
        Pago(id=uuid.uuid4(), concepto="Matrícula Semestral", tipo="matrícula", monto=1850.00, moneda="GTQ", descripcion="Costo de matrícula por semestre académico.", periodo="Semestral"),
        Pago(id=uuid.uuid4(), concepto="Crédito Académico", tipo="crédito", monto=195.00, moneda="GTQ", descripcion="Costo por crédito cursado.", periodo="Por crédito"),
        Pago(id=uuid.uuid4(), concepto="Mora por Pago Tardío", tipo="mora", monto=50.00, moneda="GTQ", descripcion="Recargo aplicado por pagos después de la fecha límite.", periodo="Por evento"),
        Pago(id=uuid.uuid4(), concepto="Examen de Tesis", tipo="tesis", monto=750.00, moneda="GTQ", descripcion="Derecho de examen para sustentación de tesis de grado.", periodo="Único"),
    ])
    db.commit()

    # profesores (relacionados con carreras)
    prof_garcia = Profesor(id=uuid.uuid4(), nombre="Carlos", apellido="García", email="cgarcia@uvg.edu.gt", telefono="5555-0001", carrera_id=computacion.id, departamento="Ciencias de la Computación")
    prof_lopez = Profesor(id=uuid.uuid4(), nombre="Ana", apellido="López", email="alopez@uvg.edu.gt", telefono="5555-0002", carrera_id=mecatronica.id, departamento="Ingeniería Mecatrónica")
    prof_morales = Profesor(id=uuid.uuid4(), nombre="Roberto", apellido="Morales", email="rmorales@uvg.edu.gt", telefono="5555-0003", carrera_id=administracion.id, departamento="Administración")
    prof_chen = Profesor(id=uuid.uuid4(), nombre="Laura", apellido="Chen", email="lchen@uvg.edu.gt", telefono="5555-0004", carrera_id=computacion.id, departamento="Ciencias de la Computación")
    db.add_all([prof_garcia, prof_lopez, prof_morales, prof_chen])
    db.commit()

    # usuario admin
    db.add(Usuario(
        id=uuid.uuid4(),
        nombre="Admin",
        apellido="UVG",
        email="admin@uvg.edu.gt",
        carnet=None,
        carrera_id=None,
        rol="admin",
        password_hash=sha256("admin123"),
    ))
    db.commit()

    # cursos (relacionados con carrera y profesor)
    db.add_all([
        Curso(id=uuid.uuid4(), nombre="Algoritmos y Estructuras de Datos", codigo="CC2003", creditos=5, carrera_id=computacion.id, profesor_id=prof_garcia.id, semestre="2026-1"),
        Curso(id=uuid.uuid4(), nombre="Programación Orientada a Objetos", codigo="CC2016", creditos=5, carrera_id=computacion.id, profesor_id=prof_chen.id, semestre="2026-1"),
        Curso(id=uuid.uuid4(), nombre="Sistemas de Control", codigo="ME3010", creditos=4, carrera_id=mecatronica.id, profesor_id=prof_lopez.id, semestre="2026-1"),
        Curso(id=uuid.uuid4(), nombre="Finanzas Empresariales", codigo="AD2020", creditos=4, carrera_id=administracion.id, profesor_id=prof_morales.id, semestre="2026-1"),
    ])
    db.commit()

    # eventos (relacionados con lugares)
    db.add_all([
        Evento(id=uuid.uuid4(), titulo="Feria de Carreras UVG 2026", descripcion="Presentación de todas las carreras universitarias para estudiantes de bachillerato.", tipo="actividad", fecha_inicio=datetime(2026, 5, 15, 9, 0, tzinfo=timezone.utc), fecha_fin=datetime(2026, 5, 15, 17, 0, tzinfo=timezone.utc), lugar_id=auditorio.id),
        Evento(id=uuid.uuid4(), titulo="Hackathon UVG 2026", descripcion="Competencia de programación de 24 horas. Equipos de hasta 4 personas.", tipo="actividad", fecha_inicio=datetime(2026, 5, 22, 8, 0, tzinfo=timezone.utc), fecha_fin=datetime(2026, 5, 23, 8, 0, tzinfo=timezone.utc), lugar_id=laboratorio.id),
        Evento(id=uuid.uuid4(), titulo="Charla: Inteligencia Artificial en la industria", descripcion="Ponentes de empresas tech guatemaltecas comparten experiencias con IA.", tipo="charla", fecha_inicio=datetime(2026, 6, 3, 18, 0, tzinfo=timezone.utc), fecha_fin=datetime(2026, 6, 3, 20, 0, tzinfo=timezone.utc), lugar_id=auditorio.id),
        Evento(id=uuid.uuid4(), titulo="Hora de Beca — Presentación de Requisitos", descripcion="Información sobre requisitos y proceso para obtener beca académica.", tipo="hora_beca", fecha_inicio=datetime(2026, 6, 10, 10, 0, tzinfo=timezone.utc), fecha_fin=datetime(2026, 6, 10, 12, 0, tzinfo=timezone.utc), lugar_id=biblioteca.id),
    ])
    db.commit()

    # servicios (relacionados con contactos)
    db.add_all([
        Servicio(id=uuid.uuid4(), nombre="Registro Académico", descripcion="Gestión de inscripciones, retiros de cursos y certificaciones.", categoria="Académico", horario="Lunes a viernes de 08:00 a 16:00", contacto_id=contacto_registro.id),
        Servicio(id=uuid.uuid4(), nombre="Préstamo de Libros", descripcion="Préstamo de libros físicos y acceso a bases de datos digitales.", categoria="Biblioteca", horario="Lunes a viernes de 07:00 a 21:00", contacto_id=contacto_biblioteca.id),
        Servicio(id=uuid.uuid4(), nombre="Soporte Técnico", descripcion="Asistencia con cuentas institucionales, WiFi y equipos del campus.", categoria="Tecnología", horario="Lunes a viernes de 08:00 a 17:00", contacto_id=contacto_it.id),
        Servicio(id=uuid.uuid4(), nombre="Orientación Psicológica", descripcion="Servicio gratuito de orientación y apoyo psicológico para estudiantes.", categoria="Bienestar", horario="Lunes a viernes de 09:00 a 17:00", contacto_id=contacto_bienestar.id),
    ])
    db.commit()

    db.close()
    print("Seed completado.")
    print("  Admin: admin@uvg.edu.gt / admin123")

if __name__ == "__main__":
    run()
