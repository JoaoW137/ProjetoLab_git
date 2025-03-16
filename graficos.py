import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
import time

def janela_grafico(root):
    janela_grafico = ctk.CTkToplevel(root)
    janela_grafico.title("Gráfico em Tempo Real")
    janela_grafico.geometry("600x400")
    
    # Configuração do gráfico
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Gráfico Senoidal em Tempo Real")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Amplitude")
    line, = ax.plot([], [], 'b-')

    # Criação do canvas para o gráfico
    canvas = FigureCanvasTkAgg(fig, master=janela_grafico)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill='both', expand=True)

    # Função para atualizar o gráfico em tempo real
    def update_graph():
        x_data = []
        y_data = []
        while running:
            # Adiciona um ponto ao gráfico
            x_data.append(len(x_data))
            y_data.append(np.sin(len(x_data) * 0.1))
            
            # Atualiza o gráfico
            line.set_data(x_data, y_data)
            ax.set_xlim(0, len(x_data))
            ax.set_ylim(-1.5, 1.5)
            canvas.draw()
            time.sleep(1)  # Taxa de atualização (1 Hz)

    # Inicia o gráfico em uma thread separada
    global running
    running = True
    thread = threading.Thread(target=update_graph)
    thread.start()

    # Fecha o gráfico com segurança
    def on_closing():
        global running
        running = False
        janela_grafico.withdraw()

    janela_grafico.protocol("WM_DELETE_WINDOW", on_closing)

def move_options():
    return None
