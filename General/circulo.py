import turtle

# Configuração da tela
screen = turtle.Screen()
screen.title("Desenhando Meios Círculos Conectados")

# Criação do objeto turtle
t = turtle.Turtle()

# Ajustar a espessura da linha
t.pensize(5)  # Define a espessura da linha para 5 unidades

# Mover a tartaruga para a posição inicial mais à esquerda
t.penup()
t.goto(-200, 0)  # Mover para a posição inicial desejada
t.pendown()

# Lista de textos para cada meio círculo
texts = ["Diagnóstico", "Planejamento", "Análise", "Realização", "Preparação", "Go-live"]



# Desenhar o primeiro meio círculo (para cima)
t.pencolor("red")  # Define a cor da linha para vermelho
t.setheading(90)  # Aponta para cima
t.circle(50, 180)  # Meio círculo com raio de 50, 180 graus

# Escrever texto no meio do primeiro meio círculo
t.penup()
t.setheading(0)  # Aponta para a direita
t.forward(50)  # Move para o centro do meio círculo
t.write(texts[0], align="center", font=("Arial", 10, "normal"))
t.backward(50)  # Retorna à borda do meio círculo
t.pendown()

# Mover a tartaruga para a posição inicial do segundo meio círculo
t.penup()
# Desenhar o segundo meio círculo (para baixo)
t.pencolor("blue")  # Define a cor da linha para azul
t.setheading(-90)  # Aponta para baixo
t.goto(t.xcor()+100, t.ycor())  # Mantém a posição horizontal
t.pendown()

t.circle(50, 180)  # Meio círculo invertido com raio de 50, 180 graus

# Escrever texto no meio do segundo meio círculo
t.penup()
t.setheading(0)  # Aponta para a direita
t.forward(-50)  # Move para o centro do meio círculo
t.write(texts[1], align="center", font=("Arial", 10, "normal"))
t.backward(-50)  # Retorna à borda do meio círculo
t.pendown()

colors = ["green", "orange"]  # Lista de cores para alternar
# Repetir o padrão mais duas vezes
for i in range(2):
    # Mover a tartaruga para a posição inicial do próximo meio círculo
    t.penup()
    t.pencolor(colors[i % len(colors)])  # Alterna a cor

    t.setheading(90)  # Aponta para cima
    t.goto(t.xcor() + 100, t.ycor())  # Move para a direita pelo diâmetro do círculo
    t.pendown()

    # Desenhar o próximo meio círculo (para cima)
    t.circle(50, 180)

    # Escrever texto no meio do meio círculo (para cima)
    t.penup()
    t.setheading(0)  # Aponta para a direita
    t.forward(50)  # Move para o centro do meio círculo
    t.write(texts[2 * (i+1)], align="center", font=("Arial", 10, "normal"))
    t.backward(50)  # Retorna à borda do meio círculo
    t.pendown()

    # Mover a tartaruga para a posição inicial do próximo meio círculo
    t.penup()
    t.pencolor(colors[(i + 1) % len(colors)])  # Alterna a cor
    t.setheading(-90)  # Aponta para baixo
    t.goto(t.xcor() + 100, t.ycor())  # Move para a direita pelo diâmetro do círculo
    t.pendown()

    # Desenhar o próximo meio círculo (para baixo)
    t.circle(50, 180)

    # Escrever texto no meio do meio círculo (para baixo)
    t.penup()
    t.setheading(0)  # Aponta para a direita
    t.forward(-50)  # Move para o centro do meio círculo
    t.write(texts[2 * i + 3], align="center", font=("Arial", 10, "normal"))
    t.backward(-50)  # Retorna à borda do meio círculo
    t.pendown()

# Ocultar a tartaruga
t.hideturtle()

# Finalizar
turtle.done()