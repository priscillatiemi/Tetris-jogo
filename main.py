import pygame
import random

formatos_cor = [(255, 219, 88),(255, 0, 0),(0, 0, 255),(0, 128, 0),(153, 51, 153),(255, 140, 0),(255, 0, 127)]

class Figuras:
    x = 0
    y = 0

    figuras = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figuras) - 1)
        self.cor = random.randint(1, len(formatos_cor) - 1)
        self.rotacao = 0

    def imagem(self):
        return self.figuras[self.type][self.rotacao]

    def rotacionar(self):
        self.rotacao = (self.rotacao + 1) % len(self.figuras[self.type])


class Tetris:
    nivel = 2
    score = 0
    estado = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figura = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.estado = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def nova_figura(self):
        self.figura = Figuras(3,0)


    def intersection(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figura.imagem():
                    if i+self.figura.y > self.height - 1 or \
                        j+self.figura.x > self.width - 1 or\
                        j+self.figura.x < 0 or \
                        self.field[i+self.figura.y][j+self.figura.x]>0:
                        intersection = True
        return intersection
    def quebra_linha(self):
        linha = 0
        for i in range(1, self.height):
            zero = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zero += 1
            if zero == 0:
                linha += 1
                for k in range(i,1,-1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k-1][j]
        self.score += linha **2

    def go_space(self):
        while not self.intersection():
            self.figura.y +=1
        self.figura.y -= 1
        self.freeze()

    def go_down(self):
        self.figura.y +=1
        if self.intersection():
            self.figura.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figura.imagem():
                    self.field[i+self.figura.y][j+self.figura.x] = self.figura.cor
        self.quebra_linha()
        self.nova_figura()
        if self.intersection():
            self.estado = "gameover"

    def go_side(self, dx):
        old_x = self.figura.x
        self.figura.x +=dx
        if self.intersection():
            self.figura.x = old_x

    def rotacionar(self):
        old_rotation = self.figura.rotacao
        self.figura.rotacionar()
        if self.intersection():
            self.figura.rotacao = old_rotation

pygame.init()

preto = (0,0,0)
branco = (255, 255, 255)
cinza = (128,128,128)
rosa = (255, 203, 219)
tamanho = (400,500)
screen = pygame.display.set_mode(tamanho)

pygame.display.set_caption("Tetris")

fechar_jogo = False
tempo = pygame.time.Clock()
fps = 25
jogo = Tetris(20,10)
count = 0

pressionar_baixo = False

while not fechar_jogo:
    if jogo.figura is None:
        jogo.nova_figura()
    count +=1
    if count > 100000:
        count = 0

    if count % (fps // jogo.nivel // 2) == 0 or pressionar_baixo:
        if jogo.estado == "start":
            jogo.go_down()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fechar_jogo = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jogo.rotacionar()
            if event.key == pygame.K_DOWN:
                pressionar_baixo = True
            if event.key == pygame.K_LEFT:
                jogo.go_side(-1)
            if event.key == pygame.K_RIGHT:
                jogo.go_side(1)
            if event.key == pygame.K_SPACE:
                jogo.go_space()
            if event.key == pygame.K_ESCAPE:
                jogo.__init__(20,10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressionar_baixo = False
    screen.fill(rosa)

    for i in range(jogo.height):
        for j in range(jogo.width):
            pygame.draw.rect(screen, cinza, [jogo.x + jogo.zoom * j, jogo.y + jogo.zoom * i, jogo.zoom, jogo.zoom], 1)
            if jogo.field[i][j] > 0:
                pygame.draw.rect(screen,formatos_cor[jogo.field[i][j]],
                                 [jogo.x + jogo.zoom*j + 1, jogo.y + jogo.zoom * i + 1, jogo.zoom - 2, jogo.zoom - 1])


    if jogo.figura is not None:
        for i in range(4):
            for j in range(4):
                p = i*4+j
                if p in jogo.figura.imagem():
                  pygame.draw.rect(screen, formatos_cor[jogo.figura.cor],
                                   [jogo.x + jogo.zoom *(j+jogo.figura.x)+1,
                                    jogo.y+jogo.zoom*(i+jogo.figura.y)+1,
                                    jogo.zoom -2, jogo.zoom-2])

    fonte = pygame.font.SysFont('Calibri',25,True, False)
    fonte2 = pygame.font.SysFont('Calibri', 65, True, False)
    texto = fonte.render("Score: "+str(jogo.score) , True, preto)
    texto3 = fonte.render("Aperte ESC para reiniciar",True, preto)
    comandos = fonte.render("Rodar: ↑", True, preto)
    texto_game_over = fonte2.render("Game Over!", True,(255, 0, 0))
    texto_game_over2 = fonte2.render("Aperte ESC",True,preto)

    screen.blit(texto,[1,1])
    screen.blit(texto3, (0,35))
    screen.blit(comandos,(0,65))
    if jogo.estado == "gameover":
        screen.blit(texto_game_over,[20,200])
        screen.blit(texto_game_over2,[25,265])

    pygame.display.flip()
    tempo.tick(fps)
pygame.quit()
