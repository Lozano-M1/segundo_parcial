from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_PATH = 'database/consultas.db'

def init_db():
    """Inicializa la base de datos con algunas tablas de ejemplo"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id_users INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            fecha_registro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Crear tabla de productos de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            suscripcion_hd varchar,
            monto_usd   decimal,
            estado      text not null,
            pagado      text not null
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suscripciones (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            plan   TEXT NOT NULL,
            fecha_inicio DATE DEFAULT CURRENT_DATE,
            fecha_fin DATE DEFAULT CURRENT_DATE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estadopago (
            id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
            finalizado TEXT NOT NULL,
            rechazado TEXT DEFAULT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS busqueda (
            id_busqueda INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_titulo       text,
            tipo                text,
            generos             text,
            ano_estreno         int
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles (
            id_perfiles  INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario           varchar,
            programas         text,
            edad              int,
            idioma            varchar,
            historial         text
        )
    ''')
    
    # Insertar datos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM Users')
    if cursor.fetchone()[0] == 0:
        usuarios_ejemplo = [
           ("lozano", "lozano@example.com", 1234567890),
           ("gomez", "gomez@example.com", 987654321),
           ("martinez", "martinez@example.com", 1122334455),
           ("fernandez", "fernandez@example.com", 1234567890),
           ("sanchez", "sanchez@example.com", 987654321),
           ("ramirez", "ramirez@example.com", 1122334455),
           ("torres", "torres@example.com", 1234567890),
           ("flores", "flores@example.com", 987654321),
           ("rivera", "rivera@example.com", 1122334455),
           ("gonzalez", "gonzalez@example.com", 1234567890),
           ("lopez", "lopez@example.com", 987654321),
           ("diaz", "diaz@example.com", 1122334455),
           ("morales", "morales@example.com", 1234567890),
           ("castro", "castro@example.com", 987654321),
           ("ruiz", "ruiz@example.com", 1122334455),
           ("mendoza", "mendoza@example.com", 1234567890),
           ("vargas", "vargas@example.com", 987654321),
           ("ramos", "ramos@example.com", 1122334455),
           ("jimenez", "jimenez@example.com", 1234567890),
           ("silva", "silva@example.com", 987654321),
           ("navarro", "navarro@example.com", 1122334455),
           ("mejia", "mejia@example.com", 1234567890),
           ("cortez", "cortez@example.com", 987654321),
           ("soto", "soto@example.com", 1122334455),
           ("mora", "mora@example.com", 1234567890)
        ]
        cursor.executemany('INSERT INTO Users (username, email, contraseña) VALUES (?, ?, ?)', usuarios_ejemplo)
        

        pagos_ejemplo = [
            ("sub_hd_001", 9.99, "completado", "si"),
            ("sub_hd_002", 14.99, "pendiente", "no"),
            ("sub_hd_003", 19.99, "completado", "si"),
            ("sub_hd_004", 29.99, "fallido", "no"),
            ("sub_hd_005", 39.99, "completado", "si"),
            ("sub_hd_006", 49.99, "pendiente", "no"),
            ("sub_hd_007", 59.99, "completado", "si"),
            ("sub_hd_008", 69.99, "fallido", "no"),
            ("sub_hd_009", 79.99, "completado", "si"),
            ("sub_hd_010", 89.99, "pendiente", "no"),
            ("sub_hd_011", 99.99, "completado", "si"),
            ("sub_hd_012", 109.99, "fallido", "no"),
            ("sub_hd_013", 119.99, "completado", "si"),
            ("sub_hd_014", 129.99, "pendiente", "no"),
            ("sub_hd_015", 139.99, "completado", "si"),
            ("sub_hd_016", 149.99, "fallido", "no"),
            ("sub_hd_017", 159.99, "completado", "si"),
            ("sub_hd_018", 169.99, "pendiente", "no"),
            ("sub_hd_019", 179.99, "completado", "si"),
            ("sub_hd_020", 189.99, "fallido", "no"),
            ("sub_hd_021", 199.99, "completado", "si"),
            ("sub_hd_022", 209.99, "pendiente", "no"),
            ("sub_hd_023", 219.99, "completado", "si"),
            ("sub_hd_024", 229.99, "fallido", "no"),
            ("sub_hd_025", 239.99, "completado", "si"),
            ("sub_hd_026", 249.99, "pendiente", "no"),
            ("sub_hd_027", 259.99, "completado", "si"),
            ("sub_hd_028", 269.99, "fallido", "no"),
            ("sub_hd_029", 279.99, "completado", "si"),
            ("sub_hd_030", 289.99, "pendiente", "no")
        ]
        cursor.executemany('INSERT INTO pagos (suscripcion_hd, monto_usd, estado, pagado) VALUES (?, ?, ?, ?)', pagos_ejemplo)
        
       #  cursor.executemany('INSERT INTO ventas (usuario_id, producto_id, cantidad) VALUES (?, ?, ?)', ventas_ejemplo)
    
        estadopago_ejemplo = [
            ("si", None),
            ("no", None),
            ("sp", None)
        ]
        cursor.executemany('INSERT INTO estadopago (finalizado, rechazado) VALUES (?, ?)', estadopago_ejemplo)

        suscripciones_ejemplo = [
           ("lozano", "Basico", 20230101, 20231231),
           ("gomez", "Estandar", 20230201, 20240201),
           ("martinez", "Premium", 20230301, 20240301),
           ("fernandez", "Familiar", 20230401, 20240401),
           ("sanchez", "Estudiante", 20230501, 20240501),
           ("ramirez", "Anual", 20230601, 20240601),
           ("torres", "Mensual", 20230701, 20240701),
           ("flores", "Trimestral", 20230801, 20240801),
           ("rivera", "Semestral", 20230901, 20240901),
           ("gonzalez", "VIP", 20231001, 20241001),
           ("lopez", "Corporativo", 20231101, 20241101),
           ("diaz", "Individual", 20231201, 20241201),
           ("morales", "Duo", 20240101, 20250101),
           ("castro", "Grupo", 20240201, 20250201),
           ("ruiz", "Pro", 20240301, 20250301),
           ("mendoza", "Lite", 20240401, 20250401),
           ("vargas", "Plus", 20240501, 20250501),
           ("ramos", "Max", 20240601, 20250601),
           ("jimenez", "Ultra", 20240701, 20250701),
           ("silva", "Mega", 20240801, 20250801),
           ("navarro", "VIP", 20240901, 20250901),
           ("mejia", "Corporativo", 20241001, 20251001),
           ("cortez", "Individual", 20241101, 20251101),
           ("soto", "Duo", 20241201, 20251201),
           ("mora", "Grupo", 20240101, 20250101)
        ]
        cursor.executemany('INSERT INTO suscripciones (usuario, plan, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?)', suscripciones_ejemplo)


        busqueda_ejemplo = [
           ("avatar","pelicula" ,"ciencia ficcion", 2020),
           ("guerra mundial z", "pelicula", "accion", 2010),
           ("minions", "pelicula", "comedia", 2015),
           ("stranger things", "serie", "ciencia ficcion", 2016),
           ("la casa de papel", "serie", "accion", 2017),
           ("friends", "serie", "comedia", 1994),
           ("the witcher", "serie", "fantasia", 2019),
           ("inception", "pelicula", "ciencia ficcion", 2010),
           ("the office", "serie", "comedia", 2005),
           ("breaking bad", "serie", "drama", 2008),
           ("the mandalorian", "serie", "ciencia ficcion", 2019),
           ("joker", "pelicula", "drama", 2019),
           ("the crown", "serie", "drama", 2016),
           ("black mirror", "serie", "ciencia ficcion", 2011),
           ("la reina del sur", "serie", "drama", 2011),
           ("game of thrones", "serie", "fantasia", 2011),
           ("parasite", "pelicula", "drama", 2019),
           ("avengers: endgame", "pelicula", "accion", 2019),
           ("stranger things 4", "serie", "ciencia ficcion", 2022),
           ("the batman", "pelicula", "accion", 2022),  
           ("rapido y furioso 9", "pelicula", "accion", 2021),  
           ("capitan america: civil war", "pelicula", "accion", 2016),
           ("deadpool", "pelicula", "accion", 2016),        
           ("black widow", "pelicula", "accion", 2021),       
           ("wanda vision", "serie", "ciencia ficcion", 2021),  
           ("loki", "serie", "ciencia ficcion", 2021),  
           ("reverse", "pelicula", "ciencia ficcion", 2023),  
           ("the last of us", "serie", "drama", 2023)   
        ]
        cursor.executemany('INSERT INTO busqueda (nombre_titulo, tipo, generos, ano_estreno) VALUES (?, ?, ?, ?)', busqueda_ejemplo)

        perfiles_ejemplo = [
           ("lozano", "sistemas", "25", "español", "ninguno"),
           ("martinez", "medicina", "30", "inglés", "ninguno"),
           ("gomez", "derecho", "28", "francés", "ninguno"),
           ("fernandez", "ingeniería", "22", "alemán", "ninguno"),
           ("ruiz", "arquitectura", "27", "italiano", "ninguno"),
           ("sanchez", "economía", "29", "portugués", "ninguno"),
           ("diaz", "psicología", "24", "chino", "ninguno"),
           ("torres", "biología", "26", "japonés", "ninguno"),
           ("ramirez", "historia", "31", "ruso", "ninguno"),
           ("vargas", "filosofía", "23", "árabe", "ninguno"),
           ("castro", "educación", "28", "holandés", "ninguno"),
           ("flores", "comunicación", "25", "hindi", "ninguno"),
           ("rivera", "marketing", "27", "bengalí", "ninguno"),
           ("mendoza", "sociología", "30", "sueco", "ninguno"),
           ("ortiz", "antropología", "27", "noruego", "ninguno"),
           ("gutierrez", "geografía", "25", "danés", "ninguno"),
           ("silva", "literatura", "29", "finlandés", "ninguno"),
           ("navarro", "artes", "24", "húngaro", "ninguno"),
           ("rodriguez", "música", "26", "checo", "ninguno"),
           ("alvarez", "teatro", "31", "griego", "ninguno"),
           ("jimenez", "diseño", "22", "turco", "ninguno"),
           ("morales", "fotografía", "28", "coreano", "ninguno"),
           ("pena", "periodismo", "30", "vietnamita", "ninguno"),
           ("cortez", "publicidad", "27", "tailandés", "ninguno"),
           ("soto", "marketing", "25", "hebreo", "ninguno"),
           ("fuentes", "finanzas", "29", "polaco", "ninguno")
        ]

        cursor.executemany('INSERT INTO perfiles (usuario, programas, edad, idioma, historial) VALUES (?, ?, ?, ?, ?)', perfiles_ejemplo)

    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y retorna los resultados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Determinar si es una consulta SELECT o una operación de modificación
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
            columns = [description[0] for description in cursor.description]
        else:
            conn.commit()
            results = {"affected_rows": cursor.rowcount, "message": "Query executed successfully"}
            columns = []
        
        conn.close()
        return {"success": True, "data": results, "columns": columns}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    """Página principal con el formulario para consultas SQL"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_sql():
    """Endpoint para ejecutar consultas SQL"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
    
    result = execute_query(query)
    return jsonify(result)

@app.route('/schema')
def get_schema():
    """Endpoint para obtener el esquema de la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema[table_name] = [{"name": col[1], "type": col[2], "nullable": not col[3], "primary_key": bool(col[5])} for col in columns]
        
        conn.close()
        return jsonify({"success": True, "schema": schema})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/examples')
def get_examples():
    """Endpoint que retorna consultas SQL de ejemplo"""
    examples = [
        {
            "title": "Listar todos los usuarios",
            "query": "SELECT * FROM usuarios;"
        },
        {
            "title": "Productos con precio mayor a 100",
            "query": "SELECT * FROM productos WHERE precio > 100;"
        },
        {
            "title": "Contar usuarios por edad",
            "query": "SELECT edad, COUNT(*) as cantidad FROM usuarios GROUP BY edad ORDER BY edad;"
        },
        {
            "title": "Ventas con información de usuarios y productos",
            "query": """SELECT 
                v.id as venta_id,
                u.nombre as usuario,
                p.nombre as producto,
                v.cantidad,
                v.fecha_venta
            FROM ventas v
            JOIN usuarios u ON v.usuario_id = u.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC;"""
        },
        {
            "title": "Insertar nuevo usuario",
            "query": "INSERT INTO usuarios (nombre, email, edad) VALUES ('Nuevo Usuario', 'nuevo@email.com', 25);"
        },
        {
            "title": "Actualizar precio de producto",
            "query": "UPDATE productos SET precio = 899.99 WHERE nombre = 'Laptop';"
        }
    ]
    return jsonify({"examples": examples})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)