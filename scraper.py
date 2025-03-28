import requests
from bs4 import BeautifulSoup

#product url
url = "https://www.gamerhut.com.br/MLB-2778706911-jg-teenage-mutant-ninja-turtles-cowabunga-collection-switch-_JM#position=38&search_layout=grid&type=item&tracking_id=c43ce481-e766-441c-be5c-e616adc8f918"

#http request to know page content
headers = {"user-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

#verify if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Captura nome, preço e imagem
    name_tag = soup.find("h1", class_="ui-pdp-title")
    price_tag = soup.find("span", class_="andes-money-amount__fraction")
    image_tag = soup.find("img", class_="ui-pdp-image ui-pdp-gallery__figure__image")

    name = name_tag.get_text(strip=True) if name_tag else "Nome não encontrado"
    price = price_tag.get_text(strip=True) if price_tag else "Preço não encontrado"
    image_url = image_tag["src"] if image_tag else ""

    # Cria o HTML com as informações
    html_content = f"""
    <html>
    <head>
        <title>Produto</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 350px;
                width: 90%;
            }}
            img {{
                width: 100%;
                max-width: 250px;
                border-radius: 10px;
                margin-bottom: 15px;
            }}
            h1 {{
                font-size: 18px;
                color: #333;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 22px;
                color: #27ae60;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="{image_url}" alt="{name}">
            <h1>{name}</h1>
            <p>R$ {price}</p>
        </div>
    </body>
    </html>
    """

    # Salva o HTML
    with open("produto.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Arquivo 'produto.html' criado com sucesso! Abra no navegador para visualizar.")

else:
    print("Erro ao acessar a página")