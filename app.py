from flask import Flask, render_template, url_for, redirect, request
from tarefa4 import extrator
from re import split as resplit
import ranking

app = Flask(__name__, static_url_path='', static_folder='', template_folder='')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/teste", methods=['GET'])
def teste():
    [dados, titulos] = extrator()

    dados_seletos = dict()    
    busca_original = request.args.get('busca').lower()
    busca = resplit('[ ,]', busca_original)

    for dk in dados.keys():
        try:
            for b in busca:
                if dk.find(b) != -1:
                    dados_seletos.update({b:dados[b]})
        except KeyError:
            pass

    # print('\nBuscando por:', busca)
    # print('\nTamanho do dicionário:', len(dados_seletos), '\nContendo:', dados_seletos)
    busca_original = busca_original.split(',')
    dados_seletos = {
        'Marca': busca_original[0].lower().strip(),
        'Tecnologia': busca_original[1].lower().strip(),
        'Tela': busca_original[2].lower().strip(),
        'Polegada': busca_original[3].lower().strip(),
        'Entrada': busca_original[4].lower().strip()
    }
    # print(dados_seletos, busca_original, busca)
    spearman, resultado1, resultado2 = ranking.processamento_consulta(['Marca', [dados_seletos['Marca']]])
    return render_template("teste.html", len = len(dados), dados = dados_seletos, bo = busca_original, spearman = spearman, resultado1 = resultado1, resultado2 = resultado2)

if __name__ == "__main__":
    app.run(debug=True)
    