from flask import Flask, render_template, request

app = Flask(__name__)

#route
#function
#template

@app.route("/login", methods = ['GET', 'POST'])
def login():
    data = request.form
    print (data)
    return render_template ('login.html')

@app.route("/GET", methods = ['GET'])
def pagWeb():
    return render_template ('pagWeb.html')

@app.route("/",  methods = ['GET'])
def index():
    return render_template ('index.html')

@app.route("/GET/<param>",  methods = ['GET'])   #requisicao para obter n hidrometros de maior consumo
def maiorConsumo(param):
    # chamar funcao maiorConsumo
    #usar o retorno da funçao na resposta ao cliente web
    #maiorConsumo(param)
    return f'{param}'


if __name__ == "__main__":
    app.run(debug=True)