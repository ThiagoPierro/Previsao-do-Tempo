from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

# Ocultei minha api key em um arquivo api_key.txt por segurança
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()

# Lista de cidades disponíveis
cidades = ['Florianópolis', 'Porto Alegre', 'Rio de Janeiro', 'Londrina', 'São Paulo', 'Curitiba', 'Campo Grande']

@app.route('/')
def index():
    return render_template('index.html', cidades=cidades)

@app.route('/result', methods=['POST'])
def result():
    cidade = request.form['cidade']
    # Chama a API do OpenWeatherMap para obter os dados meteorológicos
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt&exclude=minutely,hourly,daily'

    response = requests.get(url)
    data = response.json()

    # Verifica se a cidade é válida
    if data.get('main'):
        temperatura_atual = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        chance_chuva = data.get('rain', {}).get('1h', 0)  # Verifica se há informação de chuva para a próxima hora
        return render_template('result.html', cidade=cidade, temperatura_atual=temperatura_atual, temp_max=temp_max, temp_min=temp_min, chance_chuva=chance_chuva)
    else:
        mensagem = 'Erro ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.'
        return render_template('index.html', mensagem=mensagem, cidades=cidades)

if __name__ == '__main__':
    app.run(debug=True)