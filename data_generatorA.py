import csv
import random
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os

# Nome do arquivo CSV
FILE_NAME = "dados.csv"


def verificar_dados():
    """Verifica se o arquivo CSV existe e retorna o próximo valor de tempo."""
    if not os.path.exists(FILE_NAME):  # Verifica se o arquivo existe
        return 0
    try:
        dados = pd.read_csv(FILE_NAME)
        if not dados.empty and len(dados) > 0:  # Verifica se há pelo menos uma linha
            return int(dados.iloc[-1, 0]) + 1  # Retorna o último tempo + 1
    except (pd.errors.EmptyDataError, IndexError):
        return 0  # Se o arquivo estiver vazio ou ilegível, começa do zero
    except Exception as e:
        print(f"Erro ao ler os dados: {e}")
    
    return 0

def gerar_dados():
    """Gera dados aleatórios e os salva em um arquivo CSV continuamente."""
    tempo = verificar_dados()
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        while True:
            valor = random.uniform(0, 100)  # Gera um número aleatório entre 0 e 100
            writer.writerow([tempo, valor])
            file.flush()  # Garante que os dados sejam gravados imediatamente
            print(f"Gerado: Tempo={tempo}, Valor={valor:.2f}")
            tempo += 1
            time.sleep(1)  # Gera um novo dado a cada 1 segundo

def plotar_dados():
    """Lê os dados do arquivo CSV e os plota em tempo real."""
    fig, ax = plt.subplots()
    
    def update(frame):
        try:
            df = pd.read_csv(FILE_NAME)
            if len(df) > 0:  # Garante que há dados para plotar
                ax.clear()
                ax.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o', linestyle='-', color='b')
                ax.set_title("Dados em Tempo Real")
                ax.set_xlabel("Tempo")
                ax.set_ylabel("Valor")
        except Exception as e:
            print(f"Erro ao ler dados: {e}")
    
    ani = animation.FuncAnimation(fig, update, interval=1000)  # Atualiza a cada 1s
    plt.show()

# Executa o gerador de dados em uma thread separada
threading.Thread(target=gerar_dados, daemon=True).start()

# Inicia o plot dos dados
plotar_dados()
