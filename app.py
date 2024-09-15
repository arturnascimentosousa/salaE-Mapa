from flask import Flask, render_template_string
import random
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# Lista de alunos
total_alunos = [
    "Ana Bia", "Stalberg", "Beatriz", "Bianca", "Nascimento", "Boca",
    "Sophie", "Laura", "Lívia", "Cassuriaga", "Evelyn", "João",
    "Joaquim", "Daichi", "Schettini", "Rapha", "Roger", "Heitor",
    "Xavier", "Teotonio", "Vicente", "Geovanna", "Ryan", "Albano"
]

app = Flask(__name__)
mesas = []

# Função para distribuir os alunos nas mesas
def distribuir_alunos():
    global mesas
    alunos = total_alunos.copy()
    random.shuffle(alunos)
    mesas = [[] for _ in range(6)]  # Agora serão 6 mesas

    for i in range(4):  # Agora são 4 alunos por mesa
        for mesa in mesas:
            if alunos:
                mesa.append(alunos.pop())

def schedule_task():
    timezone = pytz.timezone('America/Sao_Paulo')
    scheduler = BackgroundScheduler()
    scheduler.add_job(distribuir_alunos, 'cron', hour=6, minute=0, timezone=timezone)
    scheduler.start()

# Rota principal que exibe as mesas
@app.route('/')
def show_mesas():
    html_template = '''
    <html>
        <head>
            <title>Distribuição de Alunos</title>
        </head>
        <body>
            <h1>Distribuição de Alunos nas Mesas</h1>
            {% for i, mesa in enumerate(mesas, 1) %}
                <h2>Mesa {{ i }}:</h2>
                <p>{{ ', '.join(mesa) }}</p>
            {% endfor %}
            <img src="{{ url_for('static', filename='mapademesa.png') }}" alt="" height="300px">
        </body>
    </html>
    '''
    return render_template_string(html_template, mesas=mesas, enumerate=enumerate)

if __name__ == '__main__':
    distribuir_alunos()  # Inicializa as mesas na primeira execução
    schedule_task()  # Agenda a tarefa para rodar todos os dias às 6 da manhã
    app.run(host='0.0.0.0', port=5000)
    print("oieee rodei")
