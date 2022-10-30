from flask import Flask, render_template

app = Flask(__name__)

#route
#function
#template

@app.route("/")
def login():
    return render_template ('login.html')

@app.route("/GET")
def pagWeb():
    return render_template ('pagWeb.html')

@app.route("/index")
def index():
    return render_template ('index.html')

@app.route("/GET/<param>")   #requisicao para obter n hidrometros de maior consumo
def maiorConsumo(param):
    # chamar funcao maiorConsumo
    #usar o retorno da funçao na resposta ao cliente web
    #maiorConsumo(param)
    return f'{param}'


if __name__ == "__main__":
    app.run(debug=True)