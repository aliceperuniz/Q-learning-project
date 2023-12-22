import connection as cn
import random as rd
import numpy as np

class QLearning:
    def __init__(self, alpha, gamma, actions):
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.matriz_resultado = np.loadtxt('C:/Users/Kylce/Downloads/resultado.txt')
        np.set_printoptions(precision=6) # para imprimir os valores com 6 casas decimais

    def Q_values(self, next_state, reward): # equação geral para a utilidade de um estado em Q-learning (Q-values)
        return reward + self.gamma * max(self.matriz_resultado[next_state])

    def best_action(self, estado): # Retorna o índice da ação com o maior valor na matriz_resultado para o estado dado.
        return np.argmax(self.matriz_resultado[estado])

    def choose_action(self, estado, epsilon):
        if rd.random() < epsilon:
            return rd.choice(self.actions), 'aleatoria' # retorna uma ação aleatória
        else:
            return self.actions[self.best_action(estado)], 'melhor acao' # retorna a ação com a maior utilidade estimada

    def executar(self):
        conexao = cn.connect(2037)
        estado_atual = 0
        epsilon = 0.1 # a probabilidade de escolher uma ação aleatória vai ser de 10%

        while True:
            if epsilon > 0.1: #vai diminuindo o epsilon ao longo do treinamento
                epsilon -= 0.0001
            print(epsilon)
            print(estado_atual)
            acao, tipo = self.choose_action(estado_atual, epsilon)  # chama o método choose_action para obter uma ação com base no estado atual e na aleatoriedade ou na melhor acao
            print(f'Ação escolhida para o estado {estado_atual}: {acao}')

            col_acao = self.actions.index(acao)

            estado, recompensa = cn.get_state_reward(conexao, acao) #obtém o próximo estado e a recompensa
            if recompensa == -100: #com o objetivo de nao prejudicar o treinamento com os bugs do jogo
                self.alpha = 0.1
            plataforma, direcao = int(estado[:7], 2),int(estado[7:], 2) # converte o estado de binário para decimal e separa entre plataf e direcao
            print(plataforma, direcao)
            next_state = int(estado,2) # atualiza próximo estado

            print(f'valor anterior dessa ação: {self.matriz_resultado[estado_atual][col_acao]}')
            # Atualiza o valor da ação na matriz_resultado usando a fórmula Q-learning:
            self.matriz_resultado[estado_atual][col_acao] += self.alpha * (self.Q_values(next_state, recompensa) - self.matriz_resultado[estado_atual][col_acao])
            print(f'valor novo dessa ação: {self.matriz_resultado[estado_atual][col_acao]}')

            estado_atual = next_state
            
            np.savetxt('resultado.txt', self.matriz_resultado, fmt="%f") # salva a matriz_resultado em um arquivo txt

# Parâmetros
alpha = 0.1
gamma = 0.99
acoes = ["left", "right", "jump"]

# Cria instância da classe QLearning
agente_qlearning = QLearning(alpha, gamma, acoes)

# Executa o agente Q-learning (loop principal)
agente_qlearning.executar()
