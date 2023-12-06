import connection

conexao = connection.connect()

act = ["jump", "left", "right"]

while (True):
    estado, recompensa = connection.get_state_reward(conexao, act[0])
    print("Estado: ", estado)
    print("Recompensa: ", recompensa)
    
    plataforma, direcao = int(estado[:7], 2),int(estado[:7], 2)
    print("Plataforma: ", plataforma)
    print("Direcao: ", direcao)
