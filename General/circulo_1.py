import turtle

# Configuração da tela
screen = turtle.Screen()
screen.title("Desenhando Meios Círculos Conectados com Texto")

# Criação do objeto turtle
t = turtle.Turtle()
t.pensize(5)  # Define a espessura da linha para 5 unidades

# Lista de textos para cada meio círculo
texts = ["Diagnóstico", "Planejamento", "Análise", "Realização", "Preparação", "Go-live"]

# Lista de cores para alternar
colors = ["red", "blue", "green", "orange","purple","black"]

# Função para desenhar um meio círculo e escrever texto
def desenhar_meio_circulo(cor, texto, direcao, frente, recuo):
    t.pencolor(cor)
    t.setheading(direcao)
    t.circle(50, 180)
    t.penup()
    t.setheading(0)
    t.forward(frente)

    # Destacar fundo da fase "Preparação"
    # if texto == "Preparação":
    #     t.fillcolor("lightgray")  # Cor de fundo para destaque
    #     t.begin_fill()
    #     t.setheading(90)
    #     t.forward(10)  # Ajusta posição para desenhar o retângulo
    #     t.setheading(180)
    #     t.forward(50)
    #     t.setheading(0)
    #     t.forward(100)
    #     t.setheading(-90)
    #     t.forward(20)
    #     t.setheading(180)
    #     t.forward(100)
    #     t.setheading(90)
    #     t.forward(10)
    #     t.end_fill()
    #     t.setheading(0)
    #     t.backward(50)  # Retorna à posição central para o texto

    t.write(texto, align="center", font=("Arial", 10, "normal"))
    t.backward(recuo)
    t.pendown()

# Mover a tartaruga para a posição inicial mais à esquerda
t.penup()
t.goto(-200, 0)
t.pendown()

# Desenhar e escrever texto para cada meio círculo
for i in range(3):
    # Desenhar meio círculo para cima
    desenhar_meio_circulo(colors[2 * i % len(colors)], texts[2 * i], 90,50,50)
    
    # Mover a tartaruga para a posição inicial do próximo meio círculo
    t.penup()
    t.goto(t.xcor() + 100, t.ycor())
    t.pendown()

    # Desenhar meio círculo para baixo
    desenhar_meio_circulo(colors[(2 * i + 1) % len(colors)], texts[2 * i + 1], -90,-50,-50)
    
    # Preparar para o próximo par de meios círculos
    t.penup()
    t.goto(t.xcor() + 100, t.ycor())
    t.pendown()

# Ocultar a tartaruga
t.hideturtle()

# Finalizar
turtle.done()