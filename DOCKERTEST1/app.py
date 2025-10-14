
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return """
    <h1>¡Hola Mundo desde Flask y Docker Bryan Lozano !</h1>
    <p>Esta es una aplicacion web sencilla ejecutandose en Docker.</p>
    <p>Puerto: 5000</p>
    """
@app.route('/api/saludo')
def api_saludo():   
    return {
        'mensaje': '¡Hola Mundo!',
        'tecnologia': ('Python', 'Flask', 'Docker', 'Docker Compose'),
        'estado': 'funcionando'
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    