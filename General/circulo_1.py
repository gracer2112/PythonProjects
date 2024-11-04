# app.py
# from flask import Flask, send_file, render_template
from PIL import Image, ImageDraw, ImageFont

# app = Flask(__name__)

def gerar_imagem():
    # Criar uma imagem branca
    largura, altura = 600, 600
    imagem = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(imagem)

    # Definir cores e textos
    texts = ["Diagnóstico", "Planejamento", "Análise", "Realização", "Preparação", "Go-live"]
    colors = ["red", "blue", "green", "orange", "purple", "black"]
    font = ImageFont.truetype("arial.ttf", 20)

    # Desenhar meio círculos e textos
    raio = 50
    for i, (text, color) in enumerate(zip(texts, colors)):
        x = 100 + i * 80
        y = 100 if i % 2 == 0 else 200
        draw.arc([x, y, x + 2 * raio, y + raio], 0, 180, fill=color, width=5)
        draw.text((x + raio, y + 20), text, fill=color, font=font, anchor="mm")

    # Desenhar círculo maior
    draw.ellipse([200, 300, 400, 500], outline="black", width=3)

    # Salvar a imagem
    imagem.save("turtle_output.png")

# @app.route('/')
# def index():
gerar_imagem()
#     return render_template('index.html')

# @app.route('/image')
# def get_image():
#     return send_file('static/turtle_output.png', mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)