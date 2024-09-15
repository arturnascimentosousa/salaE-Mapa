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
    scheduler.add_job(distribuir_alunos, 'cron', hour=16, minute=10, timezone=timezone)
    scheduler.start()

# Rota principal que exibe as mesas
@app.route('/')
def show_mesas():
    html_template = '''
    <html>
        <head>
            <title>Distribuição de Alunos</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    color: #333;
                    text-align: center;
                }
                h1 {
                    color: #4CAF50;
                    margin-top: 20px;
                }
                h2 {
                    color: #2E8B57;
                    margin-bottom: 10px;
                }
                p {
                    font-size: 18px;
                    color: #555;
                }
                .mesas-container {
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 20px;
                    margin-top: 20px;
                }
                .linha {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .mesa {
                    border: 2px solid #4CAF50;
                    padding: 10px;
                    border-radius: 8px;
                    width: 200px;
                    background-color: #fff;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                }
                img {
                    margin-top: 20px;
                }

                .container{
                    display:flex;
                }
            </style>
        </head>
        <body>
            <h1>Distribuição de Alunos nas Mesas</h1>
            <div class="container">
                <div class="mesas-container">
                    <div class="linha">
                        {% for i, mesa in enumerate(mesas[:3], 1) %}
                            <div class="mesa">
                                <h2>Mesa {{ i }}:</h2>
                                <p>{{ ', '.join(mesa) }}</p>
                            </div>
                        {% endfor %}
                    </div>
                    <div class="linha">
                        {% for i, mesa in enumerate(mesas[3:], 4) %}
                            <div class="mesa">
                                <h2>Mesa {{ i }}:</h2>
                                <p>{{ ', '.join(mesa) }}</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
                 <img src="{{ url_for('static', filename='mapadesala2E.svg') }}" alt="Mapa da Sala" height="300px">
            </div>
        </body>
    </html>
    '''
    return render_template_string(html_template, mesas=mesas, enumerate=enumerate)

if __name__ == '__main__':
    distribuir_alunos()  # Inicializa as mesas na primeira execução
    schedule_task()  # Agenda a tarefa para rodar todos os dias às 6 da manhã
    app.run(host='0.0.0.0', port=5000)
