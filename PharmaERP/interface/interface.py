import tkinter as tk
from src.relatorios import menu_hist
from src.medicamentos import menu_med
from src.reposicao import  menu_repo

def iniciar_janela():
    janela = tk.Tk()
    janela.title("PharmaERP - Sistema de Controle Farmacêutico")
    janela.geometry("520x430")
    janela.resizable(True, True)
    janela.configure(bg="#121820")
    janela.eval("tk::PlaceWindow . center")
    #tela de boas vindas 
    tela_boas_vindas = tk.Frame(janela, bg="#121820")
    tela_boas_vindas.pack(fill="both", expand=True)

    tk.Label(
        tela_boas_vindas,
        text="PharmaERP",
        font=("Helvetica", 28, "bold"),
        fg="#2ecc71",
        bg="#121820"
    ).pack(pady=(55, 5))

    tk.Label(
        tela_boas_vindas,
        text="Sistema de Controle Farmacêutico",
        font=("Helvetica", 12),
        fg="#f1c40f",
        bg="#121820"
    ).pack(pady=(0, 20))

    tk.Frame(tela_boas_vindas, height=2, width=340, bg="#2c3e50").pack(pady=5)

    tk.Label(
        tela_boas_vindas,
        text="Samuel, Samoel, Marcos & Gabriel\nTDE — Estrutura de Dados",
        font=("Helvetica", 10),
        fg="#bdc3c7",
        bg="#121820",
        justify="center"
    ).pack(pady=20)

    def abrir_menu_principal():
        # Esconde a tela de boas-vindas e exibe a tela do menu
        tela_boas_vindas.pack_forget()
        tela_menu.pack(fill="both", expand=True)

    tk.Button(
        tela_boas_vindas,
        text="Entrar no Sistema",
        font=("Helvetica", 12, "bold"),
        fg="#121820",
        bg="#2ecc71",
        activebackground="#27ae60",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=28,
        pady=12,
        command=abrir_menu_principal
    ).pack(pady=15)

    # TELA 2: MENU PRINCIPAL DO SISTEMA
    
    tela_menu = tk.Frame(janela, bg="#121820")

    tk.Label(
        tela_menu,
        text="PharmaERP",
        font=("Helvetica", 22, "bold"),
        fg="#2ecc71",
        bg="#121820"
    ).pack(pady=(25, 2))

    tk.Label(
        tela_menu,
        text="Menu Principal",
        font=("Helvetica", 11),
        fg="#f1c40f",
        bg="#121820"
    ).pack(pady=(0, 18))

    estilo_botao = {
        "font": ("Helvetica", 12, "bold"),
        "width": 26,
        "pady": 10,
        "relief": "flat",
        "cursor": "hand2",
        "fg": "#ffffff",
        "bg": "#1f2937",
        "activebackground": "#2ecc71",
        "activeforeground": "#121820",
    }

    tk.Button(
        tela_menu,
        text="1. Menu Medicamentos",
        command=lambda: menu_med(janela, tela_menu), # Passa a janela principal e a tela atual
        **estilo_botao 
    ).pack(pady=6)

    tk.Button(
        tela_menu,
        text="2. Reposição",
        command=lambda: menu_repo(janela, tela_menu), # Passa a janela principal e a tela atual
        **estilo_botao
    ).pack(pady=6)

    tk.Button(
        tela_menu,
        text="3. Histórico",
        command=menu_hist, # direciona para o menu de histórico / relatórios 
        **estilo_botao
    ).pack(pady=6)

    tk.Button(
        tela_menu,
        text="0. Sair",
        font=("Helvetica", 12, "bold"),
        width=26,
        pady=10,
        relief="flat",
        cursor="hand2",
        fg="#ffffff",
        bg="#c0392b",
        activebackground="#e74c3c",
        command=janela.destroy # encerra a janela
    ).pack(pady=(16, 6))

    janela.mainloop()