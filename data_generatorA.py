import csv
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
import matplotlib


matplotlib.use("TkAgg")

FILE_NAME_DADOS = "dados.csv"

state_event = threading.Event()

def verificar_dados():
    if not os.path.exists(FILE_NAME_DADOS):
        return 0
    try:
        dados = pd.read_csv(FILE_NAME_DADOS)
        if not dados.empty:
            return int(dados.iloc[-1, 0]) + 1
    except:
        return 0
    return 0

def gerar_dados(params_lock, state_event):

    tempo = verificar_dados()
    if os.path.exists(FILE_NAME_DADOS):
        try:
            dados = pd.read_csv(FILE_NAME_DADOS)
            if dados.empty:
                valor_acumulado = params_lock[0]
            else:
                valor_acumulado = float(dados.iloc[-1, 1])
        except Exception as e:
            print("Erro ao ler o último valor do CSV", e)
            valor_acumulado = params_lock[0]
    else:
        valor_acumulado = params_lock[0]

    with open(FILE_NAME_DADOS, "a", newline="") as file:
        writer = csv.writer(file)
        state_event.set()

        while state_event.is_set():
            valor_acumulado += params_lock[1]  # Acumula o incremento a cada passo
            writer.writerow([tempo, valor_acumulado])
            file.flush()

            print(f"Gerado: Tempo={tempo}, Valor={valor_acumulado:.2f}")
            tempo += 1
            time.sleep(1)


def plotar_dados():
    fig, ax = plt.subplots()
    linha, = ax.plot([], [], marker='o', linestyle='-', color='b')

    def update(frame):
        try:
            df = pd.read_csv(FILE_NAME_DADOS)
            if len(df) > 0:
                #df = df.tail(50)
                linha.set_data(df.iloc[:, 0], df.iloc[:, 1])
                ax.relim()
                ax.autoscale_view()
        except Exception as e:
            print(f"Erro ao ler dados: {e}")

    ani = animation.FuncAnimation(fig, update, interval=1000)

    ax.set_title("Dados")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valor")
    ax.grid(True)

    # Zoom with keyboard
    def on_key(event):
        scale_factor = 0.8 if event.key == 'z' else 1.25 if event.key == 'x' else 1
        if scale_factor != 1:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            x_center = (xlim[0] + xlim[1]) / 2
            y_center = (ylim[0] + ylim[1]) / 2
            x_range = (xlim[1] - xlim[0]) * scale_factor / 2
            y_range = (ylim[1] - ylim[0]) * scale_factor / 2

            ax.set_xlim([x_center - x_range, x_center + x_range])
            ax.set_ylim([y_center - y_range, y_center + y_range])
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("key_press_event", on_key)

    plt.show()

threading.Thread(target=gerar_dados, daemon=True).start()
