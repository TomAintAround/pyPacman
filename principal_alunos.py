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

def aproximar(posicaoPacman, posicaoFantasma):
    direcao = list(obtem_direecao(posicaoPacman, posicaoFantasma))

    if abs(direcao[0]) > abs(direcao[1]):
        direcao[0] = PIXEIS_MOVIMENTO if direcao[0] > 0 else -PIXEIS_MOVIMENTO
        direcao[1] = 0
    else:
        direcao[0] = 0
        direcao[1] = PIXEIS_MOVIMENTO if direcao[0] > 0 else -PIXEIS_MOVIMENTO
    
    if movimento_valido((posicaoFantasma[0] + direcao[0], posicaoFantasma[1] + direcao[1]), estado_jogo):
        return direcao
    
    melhorDirecao = random.choice(DIRECOES_POSSIVEIS)
    menorDistancia = TAMANHO_CELULA ** 2 # não nenhuma distnância maior que esta
    for novaDirecao in DIRECOES_POSSIVEIS:
        novaPosicao = (posicaoFantasma[0] + novaDirecao[0], posicaoFantasma[1] + novaDirecao[1])
        if movimento_valido(novaPosicao, estado_jogo):
            distancia = calculate_distance(novaPosicao, posicaoPacman)
            if distancia < menorDistancia:
                menorDistancia = distancia
                melhorDirecao = novaDirecao
    return melhorDirecao

def movimenta_pinky(estado_jogo):
    pacman = estado_jogo["pacman"]["objeto"]
    pinky = estado_jogo["fantasmas"][PINKY_OBJECT]["objeto"]
    return aproximar(pacman.pos(), pinky.pos())

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3
    scatter_corner_index = (0, 0)
    posicaoPacman = estado_jogo['pacman']['objeto'].pos()
    posicaoClyde = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()

    distancia = calculate_distance(posicaoPacman, posicaoClyde)
    if distancia > scatter_distance_threshold:
        return aproximar(posicaoPacman, posicaoClyde)
    else:
        return aproximar(scatter_corner_index, posicaoClyde)

def movimenta_inky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)

def movimenta_blinky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)

def perdeu_jogo(estado_jogo):
    objetoPacman = estado_jogo["pacman"]["objeto"]

    for ghost_id in range(3, 7):
        objetoGhost = estado_jogo["fantasmas"][ghost_id]["objeto"]
        if ha_colisao(objetoPacman, objetoGhost):
            terminar_jogo(estado_jogo)
            return True
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
    with open("save.txt", "w") as guardaJogo:
        for i in range(0, len(estado_jogo["mapa"]), TAMANHO_CELULA):
            linha = estado_jogo["mapa"][i:i + TAMANHO_CELULA]
            str_mapa += str(linha).replace("[", "").replace("]", "").replace(" ", "") + ",\n"
        guardaJogo.write(str_mapa)

def carrega_jogo(estado_jogo, nome_ficheiro = "mapa_inicial.txt"):
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
        estado_jogo["marcador"].penup()
        
        #inicia_jogo(estado_jogo)
        while not perdeu_jogo(estado_jogo):
            if estado_jogo['mapa'] is not None:
                estado_jogo['janela'].update() #actualiza a janela
                movimenta_objectos(estado_jogo)
                atualiza_pontos(estado_jogo)
                time.sleep(0.05)
    except TclError:
        pass