from flask import Flask, render_template, request, redirect, url_for

def obter_produtos():
    with open("produtos.csv", "r") as file:
        lista_produtos = []
        for linha in file:
            nome, descricao, preco, imagem = linha.strip().split(",")
            produto = {
                "nome": nome,
                "descricao": descricao,
                "preco": float(preco),
                "imagem": imagem
            }
            lista_produtos.append(produto)

        return lista_produtos

def salvar_produto(produto):
    linha = f"\n{produto['nome']},{produto['descricao']},{produto['preco']},{produto['imagem']}"
    with open("produtos.csv", "a") as file:
        file.write(linha)

lista_produtos = [
        { "nome": "Coca-cola", "descricao": "Bom", "preco": 9.99, "imagem": "data:image/jpeg;base64,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"},
        { "nome": "Doritos", "descricao": "Suja mão", "preco": 13.00, "imagem": "https://images.app.goo.gl/3EfQYcwYgj853ccW9"},
        { "nome": "Chocolate", "descricao": "Bom!", "preco": 2.99, "imagem": "https://images.app.goo.gl/qEPTKpjWm5bsa3Md7"},
    ]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return "<h1>Contato</h1>"

@app.route("/produtos")
def produtos():
    return render_template('produtos.html', produtos=lista_produtos)

@app.route("/produtos/<nome>")
def produto(nome):
    for produto in lista_produtos:
        if produto['nome'] == nome:
            return render_template("produto.html", produto=produto)
    
    return "Produto não existe!"

# GET
@app.route("/produtos/cadastro")
def cadastro_produto():
    return render_template("cadastro-produto.html")

# POST
@app.route("/produtos", methods=['POST'])
def salvar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    imagem = request.form['imagem']
    produto = {"nome": nome, "descricao": descricao, "preco": preco, "imagem": imagem}
    lista_produtos.append(produto)

    return redirect(url_for("produtos"))

app.run(port=5001)