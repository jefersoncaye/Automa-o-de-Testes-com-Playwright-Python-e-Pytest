import uuid
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-fixa-para-desenvolvimento"

PRODUTOS_ORIGINAIS = [
    {"id": 1, "nome": "Camiseta Estampada", "preco": 49.90, "estoque": 10, "categoria": "roupas", "imagem": "/static/img/produto-1.svg"},
    {"id": 2, "nome": "Calca Jeans", "preco": 129.90, "estoque": 5, "categoria": "roupas", "imagem": "/static/img/produto-2.svg"},
    {"id": 3, "nome": "Fone de Ouvido Bluetooth", "preco": 199.90, "estoque": 0, "categoria": "eletronicos", "imagem": "/static/img/produto-3.svg"},
    {"id": 4, "nome": "Mochila Executiva", "preco": 89.90, "estoque": 3, "categoria": "acessorios", "imagem": "/static/img/produto-4.svg"},
    {"id": 5, "nome": "Smartwatch", "preco": 349.90, "estoque": 8, "categoria": "eletronicos", "imagem": "/static/img/produto-5.svg"},
    {"id": 6, "nome": "Oculos de Sol", "preco": 79.90, "estoque": 15, "categoria": "acessorios", "imagem": "/static/img/produto-6.svg"},
]

# Estado em memória, resetavel via /api/reset
produtos = {p["id"]: dict(p) for p in PRODUTOS_ORIGINAIS}
carrinhos = {}  # id_sessao -> {produto_id_str: quantidade}


def obter_id_sessao():
    if "id_sessao" not in session:
        session["id_sessao"] = str(uuid.uuid4())
    return session["id_sessao"]


def requer_login(f):
    @wraps(f)
    def decorado(*args, **kwargs):
        if not session.get("autenticado"):
            return jsonify({"erro": "nao autenticado"}), 401
        return f(*args, **kwargs)
    return decorado


@app.route("/")
def home():
    if session.get("autenticado"):
        return render_template("produtos.html")
    return render_template("login.html")


@app.route("/login")
def pagina_login():
    return render_template("login.html")


@app.route("/produtos")
def pagina_produtos():
    if not session.get("autenticado"):
        return redirect(url_for("pagina_login"))
    return render_template("produtos.html")


@app.route("/carrinho")
def pagina_carrinho():
    if not session.get("autenticado"):
        return redirect(url_for("pagina_login"))
    return render_template("carrinho.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip()
    senha = (dados.get("senha") or "").strip()

    if email == "cliente@loja.com" and senha == "senha123":
        session["autenticado"] = True
        obter_id_sessao()
        return jsonify({"sucesso": True, "sessao_valida": True}), 200

    return jsonify({"sucesso": False, "erro": "credenciais invalidas"}), 401


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"sucesso": True}), 200


@app.route("/api/produtos", methods=["GET"])
@requer_login
def api_produtos():
    categoria = request.args.get("categoria")
    lista = list(produtos.values())
    if categoria:
        lista = [p for p in lista if p["categoria"] == categoria]
    return jsonify(lista), 200


@app.route("/api/carrinho", methods=["GET"])
@requer_login
def api_carrinho_listar():
    id_sessao = obter_id_sessao()
    carrinho = carrinhos.get(id_sessao, {})

    itens = []
    subtotal = 0.0
    for produto_id_str, quantidade in carrinho.items():
        produto = produtos.get(int(produto_id_str))
        if not produto:
            continue
        subtotal_item = round(produto["preco"] * quantidade, 2)
        subtotal += subtotal_item
        itens.append({
            "produto_id": int(produto_id_str),
            "nome": produto["nome"],
            "preco": produto["preco"],
            "quantidade": quantidade,
            "subtotal": subtotal_item,
        })

    return jsonify({
        "itens": itens,
        "quantidade_total": sum(carrinho.values()),
        "subtotal": round(subtotal, 2),
    }), 200


@app.route("/api/carrinho", methods=["POST"])
@requer_login
def api_carrinho_adicionar():
    dados = request.get_json(silent=True) or {}
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade", 1)

    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        return jsonify({"erro": "produto_id ou quantidade invalidos"}), 400

    produto = produtos.get(produto_id)
    if not produto:
        return jsonify({"erro": "produto nao encontrado"}), 404

    if produto["estoque"] <= 0:
        return jsonify({"erro": "sem estoque"}), 409

    id_sessao = obter_id_sessao()
    carrinho = carrinhos.setdefault(id_sessao, {})
    produto_id_str = str(produto_id)
    carrinho[produto_id_str] = carrinho.get(produto_id_str, 0) + quantidade

    return jsonify({"sucesso": True, "produto_id": produto_id, "quantidade_carrinho": carrinho[produto_id_str]}), 200


@app.route("/api/carrinho/<int:produto_id>", methods=["DELETE"])
@requer_login
def api_carrinho_remover(produto_id):
    id_sessao = obter_id_sessao()
    carrinho = carrinhos.get(id_sessao, {})
    produto_id_str = str(produto_id)

    if produto_id_str not in carrinho:
        return jsonify({"erro": "produto nao esta no carrinho"}), 404

    del carrinho[produto_id_str]
    return jsonify({"sucesso": True}), 200


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global produtos
    produtos = {p["id"]: dict(p) for p in PRODUTOS_ORIGINAIS}
    carrinhos.clear()
    return jsonify({"sucesso": True, "mensagem": "estado resetado"}), 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
