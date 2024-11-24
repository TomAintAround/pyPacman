import turtle as t
from tkinter import TclError
import functools
import random
import math
import os


DEFAULT_TURTLE_SIZE = 20
PACMAN_SIZE = 20
PACMAN_OBJECT = 2
#Fantasmas Blinky (red), Pinky (pink), Inky (cyan), and Clyde (orange)
BLINKY_OBJECT = 3
PINKY_OBJECT = 4
INKY_OBJECT = 5
CLYDE_OBJECT = 6
CORES_FANTASMAS = {
    3 : 'red',
    4 : 'pink',
    5 : 'cyan',
    6 : 'orange'
}
RAIO_JOGADOR = (PACMAN_SIZE / DEFAULT_TURTLE_SIZE) / 2
LARGURA_JANELA = 420
ALTURA_JANELA = 420
PIXEIS_MOVIMENTO = 5
TAMANHO_CELULA = 20
MAP_WIDTH = 20
DIRECOES_POSSIVEIS = [(0,5), (0,-5), (5,0), (-5, 0)]

# funcoes para calcular as novas direcoes dos fantasmas
FUNCOES_DIRECAO = {
    3 : None,
    4 : None,
    5 : None,
    6 : None
}


def floor(value, size, offset=200):
    """Floor of `value` given `size` and `offset`.

    The floor function is best understood with a diagram of the number line::

        -200  -100    0    100   200
        <--|--x--|-----|--y--|--z--|-->

    The number line shown has offset 200 denoted by the left-hand tick mark at
    -200 and size 100 denoted by the tick marks at -100, 0, 100, and 200. The
    floor of a value is the left-hand tick mark of the range where it lies. So
    for the points show above: ``floor(x)`` is -200, ``floor(y)`` is 0, and
    ``floor(z)`` is 100.

    >>> floor(10, 100)
    0.0
    >>> floor(120, 100)
    100.0
    >>> floor(-10, 100)
    -100.0
    >>> floor(-150, 100)
    -200.0
    >>> floor(50, 167)
    -33.0

    """
    return float(((value + offset) // size) * size - offset)


def goto(x,y, t):
    t.pu()
    t.goto(x,y)




def quadrado(x, y, tartaruga):
    "Draw square using path at (x, y)."
    tartaruga.up()
    tartaruga.goto(x, y)
    tartaruga.down()
    tartaruga.begin_fill()

    for count in range(4):
        tartaruga.forward(TAMANHO_CELULA)
        tartaruga.left(90)

    tartaruga.end_fill()


def offset(point):
    "Return offset of point in tiles."
    x = (floor(point[0], TAMANHO_CELULA) + 200) / TAMANHO_CELULA
    y = (180 - floor(point[1], TAMANHO_CELULA)) / TAMANHO_CELULA
    index = int(x + y * TAMANHO_CELULA)
    return index

def desenha_mundo(estado_jogo):
    ''' Função responsável por desenhar o mundo baseado numa lista que contem as posições.'''
    t.bgcolor('black')
    marcador = t.Turtle(visible=False)
    marcador.color('blue')
    tiles = estado_jogo['mapa']
    for index in range(len(tiles)):
        tile = tiles[index]
        x, y =calcula_x_y_from_index(index)
        if tile > 0:
            
            quadrado(x, y, marcador)

            if tile == 1:
                marcador.up()
                marcador.goto(x + 10, y + 10)
                marcador.dot(2, 'white')
    estado_jogo['marcador'] = marcador
                

def calcula_x_y_from_index(index):
    x = (index % TAMANHO_CELULA) * TAMANHO_CELULA - 200
    y = 180 - (index // TAMANHO_CELULA) * TAMANHO_CELULA
    return x, y

def get_elements_inital_pos_from_map(estado_jogo, element):
    x, y = calcula_x_y_from_index(estado_jogo['mapa'].index(element))
    index = estado_jogo['mapa'].index(element)
    estado_jogo['mapa'][index] = 7
    return x, y


def cria_pacman(x_pos_inicial, y_pos_inicial):
    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    pacman = t.Turtle()
    pacman.pu()
    goto(x_pos_inicial, y_pos_inicial, pacman)
    pacman.shape('circle')
    pacman.shapesize(PACMAN_SIZE / DEFAULT_TURTLE_SIZE)
    pacman.fillcolor('yellow')
    pacman.shape(os.path.join('images', 'pacman.gif'))
    return pacman

def cria_fantasmas(x_pos_inicial, y_pos_inicial, ghost_id):
    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    fantasma = t.Turtle()
    fantasma.pu()
    goto(x_pos_inicial, y_pos_inicial, fantasma)
    fantasma.shape('circle')
    fantasma.shapesize(PACMAN_SIZE / DEFAULT_TURTLE_SIZE)
    fantasma.fillcolor(CORES_FANTASMAS[ghost_id])
    fantasma.shape(os.path.join('images', '%d.gif' % ghost_id))
    return fantasma


def init_state():
    estado_jogo = {}
    estado_jogo['pacman'] = {
        'objeto' : None,
        'direcao_atual' : None
    }
    estado_jogo['fantasmas'] = {i : { 'objeto' : None, 'direcao_atual' : None} for i in range(3,7)}
    estado_jogo['mapa'] = None
    estado_jogo['score'] = 0
    estado_jogo['marcador'] = None
    estado_jogo['quadro'] = None
    return estado_jogo

def cria_janela():
    #create a window and declare a variable called window and call the screen()
    window=t.Screen()
    window.title("Pacman Game")
    #window.bgcolor("green")
    window.setup(width = LARGURA_JANELA,height = ALTURA_JANELA, startx=370,starty=0)
    window.tracer(0)
    print(os.getcwd())
    window.register_shape(os.path.join('images', 'pacman.gif'))
    for i in range(3,7):
        window.register_shape(os.path.join('images', '%d.gif' % i))
    return window

def cria_quadro_resultados():
    #Code for creating pen for scorecard update
    quadro=t.Turtle()
    quadro.speed(0)
    quadro.color("White")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(-(LARGURA_JANELA/2)+40,(ALTURA_JANELA/2)-20)
    quadro.write("Pontos: 0 ", align="center", font=('Monaco',10,"normal"))
    return quadro


def terminar_jogo(estado_jogo):
    '''
     Função responsável por terminar o jogo. 
    '''
    print("Adeus")
    estado_jogo['janela'].bye()
    

def cria_objectos(estado_jogo):
    pacman_initial_pos_x, pacman_initial_pos_y  = get_elements_inital_pos_from_map(estado_jogo, PACMAN_OBJECT)
    if estado_jogo['pacman']['objeto'] is not None:
        estado_jogo['pacman']['objeto'].ht()
        del estado_jogo['pacman']['objeto']
    estado_jogo['pacman']['objeto'] = cria_pacman(pacman_initial_pos_x+10, pacman_initial_pos_y+10)
    goto(pacman_initial_pos_x+10, pacman_initial_pos_y+10, estado_jogo['pacman']['objeto'])
    estado_jogo['pacman']['direcao_atual'] = (5,0)

    for ghost_object in range(3,7):
        f_initial_pos_x, f_initial_pos_y  = get_elements_inital_pos_from_map(estado_jogo, ghost_object)
        if estado_jogo['fantasmas'][ghost_object]['objeto'] is not None:
            estado_jogo['fantasmas'][ghost_object]['objeto'].ht()
            del estado_jogo['fantasmas'][ghost_object]['objeto']
        f = cria_fantasmas(f_initial_pos_x + 10, f_initial_pos_y + 10, ghost_object)
        estado_jogo['fantasmas'][ghost_object]['objeto'] = f
        goto(f_initial_pos_x + 10, f_initial_pos_y + 10, estado_jogo['fantasmas'][ghost_object]['objeto'])

def setup(estado_jogo, jogar, funcoes_jogadores, funcoes_fantasmas):
    janela = cria_janela()
    #Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(funcoes_jogadores['pacman_cima'], estado_jogo) ,'Up')
        janela.onkeypress(functools.partial(funcoes_jogadores['pacman_baixo'], estado_jogo) ,'Down')
        janela.onkeypress(functools.partial(funcoes_jogadores['pacman_esquerda'], estado_jogo) ,'Left')
        janela.onkeypress(functools.partial(funcoes_jogadores['pacman_direita'], estado_jogo) ,'Right')
        janela.onkeypress(functools.partial(funcoes_jogadores['guarda_jogo'], estado_jogo) ,'s')
        janela.onkeypress(functools.partial(funcoes_jogadores['carrega_jogo'], estado_jogo) ,'l')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo) ,'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    estado_jogo['janela'] = janela
    if estado_jogo['mapa'] is not None:
        desenha_mundo(estado_jogo)
        cria_objectos(estado_jogo)
        for ghost_object in range(3,7):
            FUNCOES_DIRECAO[ghost_object] = funcoes_fantasmas[ghost_object]
            estado_jogo['fantasmas'][ghost_object]['direcao_atual'] = FUNCOES_DIRECAO[ghost_object](estado_jogo)
    

    

def movimento_valido(ponto, estado_jogo):
    index = offset(ponto)
    return estado_jogo['mapa'][index] != 0


def movimenta_pacman(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() + estado_jogo['pacman']['direcao_atual'][0]
    y = estado_jogo['pacman']['objeto'].ycor() + estado_jogo['pacman']['direcao_atual'][1] 
    # origin = estado_jogo['pacman']['objeto'].pos()

    if movimento_valido((x,y), estado_jogo):
        # Calculate the direction in radians
        # theta = math.degrees(math.atan2(y - origin[1], x - origin[0]))
        goto(x,y, estado_jogo['pacman']['objeto'])
        # estado_jogo['pacman']['objeto'].setheading(theta)

def movimenta_fantasmas(estado_jogo):
    estado_fantasmas = estado_jogo['fantasmas']
    for ghost_id, ghost in estado_fantasmas.items():
        if ghost['direcao_atual'] is not None:
            x = ghost['objeto'].xcor() + ghost['direcao_atual'][0]
            y = ghost['objeto'].ycor() + ghost['direcao_atual'][1] 
    
            if movimento_valido((x,y), estado_jogo):
                goto(x,y, ghost['objeto'])
            else:
                ghost['direcao_atual'] = FUNCOES_DIRECAO[ghost_id](estado_jogo)

# Function to check collision
def ha_colisao(t1, t2, collision_distance=20):
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    return distance < collision_distance


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Pontos: {}".format(estado_jogo['score']),align="center",font=('Monaco',10,"normal"))

def movimenta_objectos(estado_jogo):
    movimenta_fantasmas(estado_jogo)
    movimenta_pacman(estado_jogo)

