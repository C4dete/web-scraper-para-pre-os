from flask import Flask, render_template, request, redirect, jsonify
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

DATA_FILE = "products.json"

# Função para carregar produtos salvos
def load_products():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar produtos no JSON
def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)

# Página inicial (Lista de produtos)
@app.route("/")
def index():
    products = load_products()
    return render_template("index.html", products=products)

# Rota para adicionar um novo produto
@app.route("/add", methods=["POST"])
def add_product():
    url = request.form["url"]
    price_class = request.form["price_class"]
    image_class = request.form["image_class"]

    # Faz a requisição à página
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Pega o nome, preço e imagem do produto
        name_tag = soup.find("h1", class_="ui-pdp-title")
        price_tag = soup.find("span", class_=price_class)
        image_tag = soup.find("img", class_=image_class)

        name = name_tag.get_text(strip=True) if name_tag else "Nome não encontrado"
        price = price_tag.get_text(strip=True) if price_tag else "Preço não encontrado"
        image_url = image_tag["src"] if image_tag else ""

        # Adiciona o produto à lista
        products = load_products()
        products.append({"name": name, "price": price, "image": image_url})
        save_products(products)

    return redirect("/")

# Rota para excluir um produto
@app.route("/delete/<int:index>", methods=["POST"])
def delete_product(index):
    products = load_products()
    if 0 <= index < len(products):
        del products[index]
        save_products(products)
    return jsonify({"message": "Produto removido com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
