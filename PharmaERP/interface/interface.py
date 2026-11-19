# JANELA PRINCIPAL
# IMPORTS

import tkinter as tk

# Cria a janela principal
janela = tk.Tk()

# Configurações da janela
janela.title("PharmaERP - Sistema de Gestão Farmacêutica")
janela.geometry("1000x650")
janela.minsize(800, 500)

# Título da aplicação
titulo = tk.Label(
    janela,
    text="PharmaERP",
    font=("Arial", 22, "bold")
)

titulo.pack(pady=20)

# Mantém a aplicação aberta
def iniciar_interface() :
    janela.mainloop()
    
iniciar_interface()