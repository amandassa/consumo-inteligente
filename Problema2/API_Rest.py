from flask import Flask, render_template, request
import json

app = Flask(__name__)

#Pagina inicial
@app.route("/",  methods = ['GET'])
def index():
    return render_template ('index.html')

#Página de login
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #Recebimento de dados:
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    #Verificação de ADM's:
    with open('C:/Users/danrl/Desktop/MI-Redes/MI-Redes/Problema2/adm.json') as adm:
        listaAdm = json.load(adm)
        cont = 0
        for c in listaAdm: 
            cont += 1
            if usuario == c['nome'] and senha == c ['senha']:
                return render_template ('indexLogado.html')
    #Verificação de usuarios:
    with open('C:/Users/danrl/Desktop/MI-Redes/MI-Redes/Problema2/usuarios.json') as usuarios:
        listaUsers = json.load(usuarios)
        cont = 0
        for c in listaUsers: 
            cont += 1
            if usuario == c['nome'] and senha == c ['senha']:
                return 'Olá Usuario!'
    #Caso contrário:
    return render_template ('login.html')

#Pagina incial depois de logado
@app.route("/GET/", methods = ['GET'])
def pagWeb():
    return render_template ('indexLogado.html')

#Pagina para verificação de hidrometros
@app.route("/GET/Hidrometros", methods = ['GET', 'POST'])
def hidrometros():
    #Recebe a quantidade de hidrometros:
    hidrometro = request.form.get('hidrometro')

    #FALTA A PARTE DE MOSTRAR OS HIDROMETROS: 
    # ---------------------------------------
    # ---------------------------------------
    
    return render_template ('hidrometros.html')


@app.route("/GET/<param>",  methods = ['GET'])   #requisicao para obter n hidrometros de maior consumo
def maiorConsumo(param):
    # chamar funcao maiorConsumo
    #usar o retorno da funçao na resposta ao cliente web
    #maiorConsumo(param)
    return f'{param}'


if __name__ == "__main__":
    app.run(debug=True)