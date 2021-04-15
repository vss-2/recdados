from flask import Flask, render_template, url_for, redirect, request
from tarefa4 import extrator
app = Flask(__name__, static_url_path='', static_folder='', template_folder='')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/teste", methods=['GET'])
def teste():
    dados = extrator()
    # dados = dict({'Olá': 21})
    busca = request.args.get('busca')
    return render_template("teste.html", len = len(dados), dados = dados)

if __name__ == "__main__":
    app.run(debug=True)
    