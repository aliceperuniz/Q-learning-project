import random
from typing import Any
from random import choice, choices, random
import connection

conexao = connection.connect(2037)

class mapa:
    def __call__(self, w = 4, h = 4, stumble = 0) :  #trocar os 4's pelas medidas do mapa do jogo
        self.w = w # w = largura do mapa, h = altura do mapa
        self.h = h
        self.stumble = stumble  # probabilidade de "cair"
        self.reset()  # coloca o personagem na posição inicial de novo

    def reset(self) :
        self.pos = [self.h-1, 0]
        return self.pos.copy()
    
    def act(self, action): 
        if action == 0: #pra cima
            self.pos[0] -= 1
        elif action == 1: #pra direita
            self.pos[1] += 1
        elif action == 2: #pra baixo
            self.pos[0] += 1
        elif action == 3: #pra esquerda
            self.pos[1] -= 1
        else:
            print("Invalid action: " + str(action))

        #Stumble -> se o número aleatório for menor que a probabilidade de cair, adiciona-se coordenadas, para o personagem poder andar uma casa
        if random() < self.stumble:
            self.pos[0] += choice([-1, 0, 1])
            self.pos[1] += choices([-1, 0, 1])

        #Paredes -> para não sair dos limites do mapa
        self.pos[0] = min(self.h-1, max(0, self.pos[0]))
        self.pos[1] = min(self.w-1, max(0, self.pos[1]))
    
        r = 0
        final = False
        if self.pos[1] == self.w-1 and self.pos[0] == 0: #ajustar condicional para se encaixar no problema (quando chegar no destino final -> recebe recompensa)
            r = 100 # recompensa ganha
            final = True
        elif self.pos[1] == self.w-1 and self.pos[0] == 1: #ajustar condicional para se encaixar no problema (caiu no abismo -> perde recompensa)
            r = -100 # recompensa perdida
            final = True

        return self.pos.copy(), r, final  #estado atual, recompensa, e booleano que indica se chegou ao final ou não

class Qlearning:
    def __init__(self, epsilon = 0.1, alpha = 0.1, gamma = 0.9, init = 0, w = 4, h = 4, a = 4): # a = número de ações
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.w = w
        self.h = h
        self.a = a
        self.init = init
        self.reset()
    
    def reset(self):
        self.qtable = [[[self.init] * self.a for i in range(self.w)] for j in range(self.h)] 

    def printQtable(self):
        print("Pos\t|\tUp\t|\tRight\t|\tDown\t|\tLeft\t|")
        for i in range(self.h):
            for j in range(self.w):
                print(self.qtable[i][j], end = " ")
            print("%d,%d\t|\t%d\t|\t%d\t|\t%d\t|\t%d\t|" % (i, j, self.qtable[i][j][0], self.qtable[i][j][1], self.qtable[i][j][2], self.qtable[i][j][3]))

    def printPolicy(self):
        print("****" * self.w + "-")
        for i in range(self.h):
            print("|", end = "")
            for j in range(self.w):
                best = self.getBestAction([i, j])
                print(" " + " setas"[best] + " |", end = "")
            print("\n" + "****" * self.w + "-")

    def getMaxQ(self, pos): # dá o maior entre os 4 valores de cada posição
        return max(self.qtable[pos[0]][pos[1]])
    
    def getBestAction(self, pos):
        qs = self.qtable[pos[0]][pos[1]]
        m = max(qs)
        bests = [i for i, j in enumerate(qs) if j == m]  # se houver empate do melhor caminho, escolhe aleatoriamente
        return choice(bests)
    
    def getRandomAction(self, pos):
        return int(random()* self.a)
    
    def getAction(self, pos):
        if random() < self.epsilon: # taxa de exploração
            return self.getRandomAction() #ação aleatória
        else:
            return self.getBestAction(pos) #ação com maior recompensa
        
    def updateQ(self, oldpos, action, newpos, reward, final):
        if final:
            self.qtable[oldpos[0]][oldpos[1]][action] += self.alpha * (reward - self.qtable[oldpos[0]][oldpos[1]][action])
        else:
            self.qtable[oldpos[0]][oldpos[1]][action] += self.alpha * (reward + self.gamma * self.getMaxQ(newpos) - self.qtable[oldpos[0]][oldpos[1]][action])

act = ["jump", "left", "right"]

largura = int(input("Digite a largura do mapa: "))
altura = int(input("Digite a altura do mapa: "))
mapinha = mapa(w = largura, h = altura)
episodes = int(input("Digite o número de episódios: "))
q = Qlearning(w = largura, h = altura, epsilon = 0, alpha = 1, init = 100)
for i in range(episodes):
    action = mapinha.reset()
    final = False
    while not final:
        action = q.getAction(action)
        newaction, reward, final = mapinha.act(action)
        q.updateQ(action, action, newaction, reward, final)
        action = newaction
    print("Episode %d finished after %d steps") #% (i, len(path)

# while (True):
#    estado, recompensa = connection.get_state_reward(conexao, act[0])
#   print("Estado: ", estado)
#  print("Recompensa: ", recompensa)
# 
# plataforma, direcao = int(estado[:7], 2),int(estado[:7], 2)
# print("Plataforma: ", plataforma)
# print("Direcao: ", direcao)
