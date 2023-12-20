import connection as cn
import random as rd
import numpy as np

class QLearning:
    def __init__(self, alpha, gamma, actions):
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.matriz_utilidade = np.loadtxt('resultado.txt')
        np.set_printoptions(precision=6)

    def utilidade_estado(self, next_state, reward):
        return reward + self.gamma * max(self.matriz_utilidade[next_state])

    def melhor_acao(self, estado):
        return np.argmax(self.matriz_utilidade[estado])

    def escolher_acao(self, estado, aleatoriedade):
        if rd.random() < aleatoriedade:
            return rd.choice(self.actions)
        else:
            return self.actions[self.melhor_acao(estado)]

    def executar(self):
        s = cn.connect(2037)
        curr_state = 0
        curr_reward = -14
        aleatoriedade = 0

        while True:
            print(curr_state)
            acao = self.escolher_acao(curr_state, aleatoriedade)
            print(f'Ação escolhida para o estado {curr_state}: {acao}')

            col_acao = self.actions.index(acao)

            estado, recompensa = cn.get_state_reward(s, acao)
            estado = int(estado[2:], 2)
            next_state = estado

            print(f'valor anterior dessa ação: {self.matriz_utilidade[curr_state][col_acao]}')
            self.matriz_utilidade[curr_state][col_acao] += self.alpha * (self.utilidade_estado(next_state, curr_reward) - self.matriz_utilidade[curr_state][col_acao])
            print(f'valor novo dessa ação: {self.matriz_utilidade[curr_state][col_acao]}')

            curr_state = next_state
            curr_reward = recompensa

            np.savetxt('resultado.txt', self.matriz_utilidade, fmt="%f")

# Parâmetros
alpha = 0.01
gamma = 0.5
acoes = ["left", "right", "jump"]

# Criar instância da classe QLearning
agente_qlearning = QLearning(alpha, gamma, acoes)

# Executar o agente Q-learning
agente_qlearning.executar()
