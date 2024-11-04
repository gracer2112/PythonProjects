import turtle
import math

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

# Escrever "Monitoramento e Controle" em duas linhas abaixo do círculo
t.penup()
t.goto(0, -240)  # Ajustar a posição para escrever o texto abaixo do círculo
t.pendown()
t.write("Monitoramento", align="center", font=("Arial", 12, "normal"))
t.penup()
t.goto(0, -260)  # Ajustar a posição para a segunda linha
t.pendown()
t.write("e Controle", align="center", font=("Arial", 12, "normal"))

# Desenhar o círculo maior ao redor das fases cíclicas
t.penup()
t.goto(0, -200)  # Ajustar a posição inicial para o centro do círculo maior
#t.setheading(0)
t.pendown()
t.pensize(3)  # Ajustar a espessura da linha para o círculo maior
t.pencolor("black")  # Cor do círculo maior
t.circle(200)  # Desenhar o círculo maior com raio suficiente para englobar as fases

# Finalizar
turtle.done()