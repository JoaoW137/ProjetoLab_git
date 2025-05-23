import customtkinter as ctk
import tkinter as tk
from data_generatorA import gerar_dados, plotar_dados
from slidepanel import SlidePanel
import time as tm 
from working_with_files import ask_file_path
import os
import csv
import threading

#from ttkbootstrap import Style
root = ctk.CTk()

root.title("App Teste")
root.geometry("700x400")
root.minsize(width=300, height=200)
ctk.set_appearance_mode('dark')

def show_options_menu(event, selected_option):
    # Limpar botões antigos, se necessário
    for widget in scrollable_labels.winfo_children():
        if isinstance(widget, ctk.CTkButton):
            '''buttons = [w for w in root.winfo_children() if isinstance(w, ctk.CTkButton)]
            while len(buttons) >3:
                buttons[0].destroy()
                buttons.pop[0]'''
            
    # Criar botões com base na opção selecionada
    if selected_option == "Opção 1":
        print("Botao 1")
    elif selected_option == "Opção 2":
        '''button_outro = ctk.CTkButton(root, text="Outro", command=lambda: print("Outra ação executada!"))
        button_outro.pack(padx=12, pady=10)'''
    elif selected_option == "Opção 3":
        '''button_dados = ctk.CTkButton(root, text="Dados", command=lambda: print("Dados carregados!"))
        button_dados.pack(padx=12, pady=10)'''
'''
class myDragManager():
    def add_dragable_widget(self, widget):
        self.widget = widget
        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease>", self.on_drop)
        self.widget.configure(cursor="hand1")
'''

def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y
    
    if widget.winfo_parent() == str(scrollable_labels):
        widget.place(in_=root, x=widget.winfo_rootx() - root.winfo_rootx(), y=widget.winfo_rooty() - root.winfo_rooty())
def on_drag(event):

    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)

    if widget.winfo_parent() == str(scrollable_labels):
        widget.place(in_=root, x=widget.winfo_rootx() - root.winfo_rootx(), y=widget.winfo_rooty() - root.winfo_rooty())
def on_drop(event):

    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)
def create_new_label(event):
    parent_widget = event.widget.master
    x = event.widget.winfo_x() 
    y = event.widget.winfo_y() + 30
    
    new_label = ctk.CTkLabel(parent_widget, text="{new_label_name}",  fg_color="lightblue")
    new_label.place(x=x, y=y)


########################################################## creating menu ################################################################################

menu = tk.Menu(root)
root.config(menu=menu)

side_bar = SlidePanel(root, 1, 0.7)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label='New File', command=lambda:print('clicked on new file'))
file_menu.add_command(label='Select File', command=lambda: ask_file_path())
menu.add_cascade(label='File', menu=file_menu)


menu.add_command(label='Gráficos', command=lambda: plotar_dados())
menu.add_command(label='Edit', command=lambda: print("Botão de Edit"))
menu.add_command(label='Script', command=lambda: caixa_de_texto())
menu.add_command(label='Options', command= side_bar.animate)



#########################################################################################################################################################

left_nav_bar = ctk.CTkFrame(root, fg_color="#2c3e50", height=300, width=75,corner_radius=0)
left_nav_bar.pack(side="left", fill="y")

'''current_time_label = ctk.CTkLabel(left_nav_bar, text =" ")
current_time_label.grid(row=1, column=0, columnspan=2, pady=300, padx=75-(75/2), sticky="ew")
        '''

'''right_nav_bar = ctk.CTkFrame(root, fg_color="#2c3e50", height=300, width=175,corner_radius=0)
right_nav_bar.pack(side="right", fill="y")'''

under_nav_bar = ctk.CTkFrame(root, fg_color="#2c3e50", height=50, corner_radius=0)
under_nav_bar.pack(side="bottom", fill="x")

text_box1 = ctk.CTkEntry(under_nav_bar, width=100, height=15, placeholder_text="Type a number: ")
text_box1.grid(row=1, column=1,padx=2.5, pady=2.5)

text_box2 = ctk.CTkEntry(under_nav_bar, width=100, height=15, placeholder_text="Type a number: ")
text_box2.grid(row=2, column=1, pady=2.5)

text_box3 = ctk.CTkEntry(under_nav_bar, width=100, height=15, placeholder_text="Type a number: ")
text_box3.grid(row=1, column=2,padx=5, pady=2.5)

text_box4 = ctk.CTkEntry(under_nav_bar, width=100, height=15, placeholder_text="Type a number: ")
text_box4.grid(row=2, column=2, pady=2.5)

current_state_event = ctk.CTkLabel(under_nav_bar,  width=100, height=15, text ="Stopped")
current_state_event.grid(row=1, column=3, pady=2.5)
####################################### Pegando os valores das caixas de entrada ########################################


FILE_NAME_PARAMETROS = "parametros.csv"

state_event = threading.Event()

def get_entry():
    try:
        value1 = float(text_box1.get())
        value2 = float(text_box2.get())
        value3 = float(text_box3.get())
        value4 = float(text_box4.get())
        values = [value1, value2, value3, value4]
        
        # Read existing data
        if os.path.exists(FILE_NAME_PARAMETROS):
            with open(FILE_NAME_PARAMETROS, mode='r', newline='') as file:
                rows = list(csv.reader(file))
        else:
            pass

        # Replace last row
        if len(rows) == 1:
            rows[-1] = values
        else:
            rows.append(values)

        # Write all rows back to the file
        with open(FILE_NAME_PARAMETROS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        if not state_event.is_set():
            state_event.set()
            thread = threading.Thread(target=gerar_dados, args=(values, state_event), daemon=True)
            thread.start()
            current_state_event_func(state_event=state_event)
    except ValueError:
        print("Please enter valid numbers in all fields.")

    
def stop_sequence_func():
    state_event.clear()
    current_state_event_func(state_event=state_event)


run_sequence = ctk.CTkButton(left_nav_bar, width=70, height= 7.5, text="Run", command=lambda: get_entry())
run_sequence.grid(row=0, column=0,padx=5, pady=10)

stop_sequence = ctk.CTkButton(left_nav_bar, width=70, height= 7.5, text="Stop", command=lambda: stop_sequence_func())
stop_sequence.grid(row=0, column=1,padx=5, pady=10)

#############################

scrollable_labels = ctk.CTkScrollableFrame(side_bar, width=150, height=200)
scrollable_labels.pack(pady=40, padx=10, expand=True)
#System_commands = ctk.CTkLabel(scrollable_labels, text='System Commands').pack(pady=10)
#System_commands.bind("<Button 1>", show_options_menu)

#########################################################################################################################
#################################Criando Labels para o Frame com scroll##################################################
#########################################################################################################################

Beep = ctk.CTkButton(scrollable_labels, text='Beep')
Beep.pack(pady=10)
Beep.bind("<Button 1>", drag_start)
Beep.bind("<B1-Motion>", on_drag)

Bridge_setup = ctk.CTkLabel(scrollable_labels, text='Bridge Setup')
Bridge_setup.pack(pady=10)
Bridge_setup.bind("<Double 1>", create_new_label)

Chain_sequence = ctk.CTkButton(scrollable_labels, text='Chain Sequence')
Chain_sequence.pack(pady=10)

Chamber_operations = ctk.CTkLabel(scrollable_labels, text='Chamber Operations')
Chamber_operations.pack(pady=10)

Digital_input = ctk.CTkLabel(scrollable_labels, text='Digital input')
Digital_input.pack(pady=10)

Driver_output = ctk.CTkLabel(scrollable_labels, text='Driver output')
Driver_output.pack(pady=10)

External_Select = ctk.CTkLabel(scrollable_labels, text='External Select')
External_Select.pack(pady=10)


def ajustar_scrollable_labels(event=None):
    scrollable_labels_height = side_bar.winfo_height()
    
    scrollable_labels.configure(width=150, height=scrollable_labels_height-20)

def current_state_event_func(state_event):
    current_state_event.configure(text="Running") if state_event.is_set()  else  current_state_event.configure(text="Stopped")
'''
def current_time(event=None):
        time_label = tm.strftime('%H:%M:%S')
        current_time_label.configure(text=f'{time_label}')
        
        root.after(1000, current_time)
        
current_time()
'''

root.update_idletasks()
root.bind("<Configure>", ajustar_scrollable_labels)
ajustar_scrollable_labels()

def caixa_de_texto():
    janela_texto = ctk.CTkToplevel(root)
    janela_texto.title("Janela de Script")
    janela_texto.geometry("600x400")
    textbox = ctk.CTkTextbox(janela_texto)
    textbox.pack(fill="both", expand=True)


# Loop principal
root.mainloop()
