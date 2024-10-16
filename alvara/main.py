import customtkinter as ctk
from tkinter import messagebox, PhotoImage, Label
from buscar_alvara import buscar_alvara
import threading
import time

# Função para executar o processo em uma thread separada
def execute_process():
    values = textbox.get("1.0", ctk.END).strip().split('\n')  # Obtém todas as linhas da caixa de texto
    values = [value for value in values if value]  # Remove linhas vazias
    if values:
        # Inicia a animação de carregamento
        show_loading_animation()
        
        # Executa sua função personalizada em uma thread separada para evitar travamento da UI
        process_thread = threading.Thread(target=run_process, args=(values,))
        process_thread.start()
    else:
        messagebox.showwarning("Erro de Entrada", "A lista está vazia. Adicione alguns valores primeiro.")

# Função para rodar o processo e esconder a animação de carregamento após a conclusão
def run_process(values):
    try:
        buscar_alvara(values)  # Chama sua função personalizada
    finally:
        # Esconde a animação de carregamento após o término do processo
        hide_loading_animation()
        messagebox.showinfo("Processo Executado", f"Busca realizada para os documentos: {values}")

# Função para adicionar valores na caixa de texto
def add_value():
    new_values = entry.get().split(',')  # Divide a entrada por vírgulas
    if new_values and new_values[0] != "":
        for value in new_values:
            textbox.insert(ctk.END, value.strip() + '\n')  # Insere cada valor com uma nova linha
        entry.delete(0, ctk.END)  # Limpa a entrada após adicionar
    else:
        messagebox.showwarning("Erro de Entrada", "Por favor, insira alguns valores para adicionar.")

# Função para mostrar a animação de carregamento
def show_loading_animation():
    loading_label.pack(pady=10)

# Função para esconder a animação de carregamento
def hide_loading_animation():
    loading_label.pack_forget()

# Configura o modo de aparência ("System" irá adaptar ao tema do sistema operacional)
ctk.set_appearance_mode("System")  # "Dark" ou "Light" para modos fixos
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Criação da janela principal
app = ctk.CTk()
app.title("Busca de Alvarás de Construção")
app.geometry("500x500")

# Criação de um frame para melhor organização
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Criação de um rótulo
label = ctk.CTkLabel(master=frame, text="Informe os documentos para busca:")
label.pack(pady=10)

# Criação de um campo de entrada
entry = ctk.CTkEntry(master=frame, placeholder_text="ex: valor1, valor2, valor3")
entry.pack(pady=10)

# Criação de um botão para adicionar
add_button = ctk.CTkButton(master=frame, text="Adicionar Valores", command=add_value)
add_button.pack(pady=10)

# Criação de uma caixa de texto para armazenar os valores
textbox = ctk.CTkTextbox(master=frame, height=200, width=400, wrap='none')  # Caixa de texto maior para melhor visibilidade
textbox.pack(pady=10)

# Criação de um rótulo de carregamento (inicialmente oculto)
loading_label = ctk.CTkLabel(master=frame, text="Processando... Por favor, aguarde.", fg_color="transparent")

# Criação de um botão para executar o processo
execute_button = ctk.CTkButton(master=frame, text="Executar Processo", command=execute_process)
execute_button.pack(pady=20)

# Executa o loop principal do aplicativo
app.mainloop()
