from pacman import *
import time

def obtem_direecao(ponto1, ponto2):
    theta = math.atan2(ponto1[1] - ponto2[1], ponto1[0] - ponto2[0])
    dir_x = math.cos(theta)
    dir_y = math.sin(theta)
    return dir_x, dir_y

def pacman_cima(estado_jogo):
    estado_jogo["pacman"]["direcao_atual"] = DIRECOES_POSSIVEIS[0]

def pacman_baixo(estado_jogo):
    estado_jogo["pacman"]["direcao_atual"] = DIRECOES_POSSIVEIS[1]

def pacman_direita(estado_jogo):
    estado_jogo["pacman"]["direcao_atual"] = DIRECOES_POSSIVEIS[2]

def pacman_esquerda(estado_jogo):
    estado_jogo["pacman"]["direcao_atual"] = DIRECOES_POSSIVEIS[3]

def movimenta_pinky(estado_jogo):
    pacman = estado_jogo["pacman"]["objeto"]
    xPacman = pacman.xcor()
    yPacman = pacman.ycor()
    coordenadasPacman = (xPacman, yPacman)

    pinky = estado_jogo["fantasmas"][PINKY_OBJECT]["objeto"]
    xPinky = pinky.xcor()
    yPinky = pinky.ycor()
    coordenadasPinky = (xPinky, yPinky)

    dir_x, dir_y = obtem_direecao(coordenadasPacman, coordenadasPinky)
    direcao = [dir_x, dir_y]
    direcaoPositiva = [abs(elemento) for elemento in direcao]
    indexMinDirecaoPositiva = direcaoPositiva.index(min(direcaoPositiva))
    indexMaxDirecaoPositiva = direcaoPositiva.index(max(direcaoPositiva))
    direcao[indexMinDirecaoPositiva] = 0
    direcao[indexMaxDirecaoPositiva] = math.copysign(1, direcao[indexMaxDirecaoPositiva]) * PIXEIS_MOVIMENTO

    if not movimento_valido((xPinky + direcao[0], yPinky + direcao[1]), estado_jogo):
        direcao = [dir_x, dir_y]
        direcao[indexMinDirecaoPositiva] = math.copysign(1, direcao[indexMinDirecaoPositiva]) * PIXEIS_MOVIMENTO
        direcao[indexMaxDirecaoPositiva] = 0
    else:
        return tuple(direcao)

    if not movimento_valido((xPinky + direcao[0], yPinky + direcao[1]), estado_jogo):
        direcao = [dir_x, dir_y]
        direcao[indexMinDirecaoPositiva] = - math.copysign(1, direcao[indexMinDirecaoPositiva]) * PIXEIS_MOVIMENTO
        direcao[indexMaxDirecaoPositiva] = 0
    else:
        return tuple(direcao)

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3
    scatter_corner_index = 0
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    ghost_pos = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()

def movimenta_inky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)

def movimenta_blinky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)

def perdeu_jogo(estado_jogo):
    return False

def atualiza_pontos(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() 
    y = estado_jogo['pacman']['objeto'].ycor()
    index = offset((x,y))
    if estado_jogo['mapa'][index] == 1:
        estado_jogo['score'] += 1
        estado_jogo['mapa'][index] = 7
        x, y = calcula_x_y_from_index(index)
        estado_jogo['marcador'].goto(x + 10,y + 10)
        estado_jogo['marcador'].dot(2,'blue')
        update_board(estado_jogo)

def atualiza_mapa(estado_jogo, x, y, elemento):
    index = offset((x,y))
    while estado_jogo['mapa'][index] in [BLINKY_OBJECT, PINKY_OBJECT, INKY_OBJECT, CLYDE_OBJECT]:
        index += 1
    estado_jogo['mapa'][index] = elemento

def actualiza_posicao_pacman_fantasma(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() 
    y = estado_jogo['pacman']['objeto'].ycor()
    atualiza_mapa(estado_jogo, x, y, PACMAN_OBJECT)
    for ghost_id, ghost in estado_jogo['fantasmas'].items():
        x = ghost['objeto'].xcor()
        y = ghost['objeto'].ycor()
        atualiza_mapa(estado_jogo, x, y, ghost_id)

def guarda_jogo(estado_jogo):
    actualiza_posicao_pacman_fantasma(estado_jogo)
    str_mapa = ''
    pass

def carrega_jogo(estado_jogo, nome_ficheiro):
    with open(nome_ficheiro, 'r') as mapa:
        listaMundo = mapa.read()
        listaMundo = list(listaMundo.replace(",", "").replace(" ", "").replace("\n", ""))
        listaMundo = [int(elemento) for elemento in listaMundo]
        
        estado_jogo["mapa"] = listaMundo

if __name__ == '__main__':
    try:
        funcoes_jogador = {'pacman_cima': pacman_cima, 'pacman_baixo': pacman_baixo, 'pacman_esquerda': pacman_esquerda, 'pacman_direita': pacman_direita, 'guarda_jogo' : guarda_jogo, 'carrega_jogo' : carrega_jogo}    
        funcoes_fantasmas = {BLINKY_OBJECT : movimenta_blinky, PINKY_OBJECT : movimenta_pinky, INKY_OBJECT : movimenta_inky, CLYDE_OBJECT : movimenta_clyde}

        nome_ficheiro = input('Pretende carregar um mapa (Enter para carregar o mapa default): ')
        if nome_ficheiro == '':
            nome_ficheiro = 'mapa_inicial.txt'
        ##dicionario com as funcoes de movimento dos jogadores

        #funções de inicio do jogo
        estado_jogo = init_state()
        carrega_jogo(estado_jogo, nome_ficheiro)    
        setup(estado_jogo, True, funcoes_jogador,funcoes_fantasmas)
        
        #inicia_jogo(estado_jogo)
        while not perdeu_jogo(estado_jogo):
            if estado_jogo['mapa'] is not None:
                estado_jogo['janela'].update() #actualiza a janela
                movimenta_objectos(estado_jogo)
                atualiza_pontos(estado_jogo)
                time.sleep(0.05)
    except TclError:
        pass