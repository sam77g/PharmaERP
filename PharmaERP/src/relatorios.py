
# Esse arquivo será responsável pelas funcionalidades que analisam os dados. relatorios.py 
# consultas e relatórios
from collections import deque 
from datetime import datetime
from .reposicao import cancelar_repo, cadastrar_repo, buscar_repo, atualizar_repo
from .estruturas import historico,limpar_tela, medicamentos
import tkinter as tk
from tkinter import messagebox, ttk


# ---------- PALETA (mesma da tela principal) ----------
BG = "#121820"
BG_CARD = "#1f2937"
VERDE = "#2ecc71"
VERDE_ESCURO = "#27ae60"
AMARELO = "#f1c40f"
VERMELHO = "#c0392b"
VERMELHO_CLARO = "#e74c3c"
TEXTO = "#ffffff"
TEXTO_SUAVE = "#bdc3c7"


# =====================================================================
#                              LÓGICA
# =====================================================================

def DataDeModificacao() :
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M") # SALVA O DIA E HORA DE ENTRADA
    return data_formatada


        
# FUNÇÃO PARA DESFAZER A ULTIMA AÇÃO NO HISTÓRICO
def desfazer_ultima():
    if not historico:
        return
    mov = historico[-1]
    
    match mov["tipo"] :
        case "ENTRADA" :
            medicamentos[:] = [m for m in medicamentos if m["id"] != mov["id_medicamento"]]
            cancelar_repo(mov["dados"])
        case "SAÍDA" :
            med = mov["dados"]
            medicamentos.append(med)
            if med["estoque"] < 15:
                cadastrar_repo(med)
        case "REMOÇÃO":
            med = mov["dados"]
            medicamentos.append(med)
            
            if med["estoque"] < 15 :
                if buscar_repo(med) is None :
                    cadastrar_repo(med)
            else :
                if buscar_repo(med) is not None :
                    cancelar_repo(med)
                    
        case "ALTERAÇÃO" :
            dados_antigos = mov["dados"]
            for med in medicamentos :
                if med["id"] == mov["id_medicamento"]:
                    
                    match mov["campo_alterado"] :
                        case "categoria" :
                            med["categoria"] = dados_antigos["categoria"]
                            
                        case "preco" :
                            med["preco"] = dados_antigos["preco"]
                            
                        case "estoque" :
                            med["estoque"] = dados_antigos["estoque"]
                            if med["estoque"] < 15 :
                                if buscar_repo(med) is None :
                                    cadastrar_repo(med)
                            else :
                                if buscar_repo(med) is not None :
                                    cancelar_repo(med)
                        case _ :
                            print(Fore.RED+"[ERRO] 400 ")
                    break
        case "REPOSIÇÃO":
            med = None

            # Localiza o medicamento pelo ID
            for m in medicamentos:
                if m["id"] == mov["id_medicamento"]:
                    med = m
                    break

            if med is None:
                print(Fore.RED + "Medicamento não encontrado.")
                return

            # Recupera o estoque anterior à reposição
            med["estoque"] = mov["dados"]["estoque"]

            # Atualiza a solicitação de reposição
            atualizar_repo(med)
                    
            historico.pop()        
    

# =====================================================================
#                            INTERFACE TKINTER
# =====================================================================

def _botao(pai, texto, comando, cor=BG_CARD, hover=VERDE, fg_hover=BG, width=26):
    btn = tk.Button(
        pai, text=texto, command=comando,
        font=("Helvetica", 11, "bold"), width=width, pady=7,
        relief="flat", cursor="hand2", fg=TEXTO, bg=cor,
        activebackground=hover, activeforeground=fg_hover,
    )
    return btn


def _estilizar_tabela():
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "PharmaHist.Treeview", background=BG_CARD, fieldbackground=BG_CARD,
        foreground=TEXTO, rowheight=26, borderwidth=0, font=("Helvetica", 10),
    )
    estilo.configure(
        "PharmaHist.Treeview.Heading", background=BG, foreground=AMARELO,
        font=("Helvetica", 10, "bold"), relief="flat",
    )
    estilo.map("PharmaHist.Treeview", background=[("selected", VERDE_ESCURO)],
            foreground=[("selected", TEXTO)])


def _tabela_historico(pai, altura=12):
    _estilizar_tabela()
    frame = tk.Frame(pai, bg=BG)
    colunas = ("data", "medicamento", "tipo", "detalhes")
    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        height=altura, style="PharmaHist.Treeview")
    cabecalhos = {
        "data": ("Data / Hora", 130), 
        "medicamento": ("Medicamento", 180),
        "tipo": ("Tipo de Ação", 100), 
        "detalhes": ("Detalhes da Operação", 210)
    }
    for col, (titulo, largura) in cabecalhos.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=largura, anchor="center" if col != "detalhes" and col != "medicamento" else "w")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    
    # Cores personalizadas por tipo de ação no histórico
    tree.tag_configure("ENTRADA", foreground="#2ecc71")
    tree.tag_configure("REPOSIÇÃO", foreground="#74b9ff")
    tree.tag_configure("ALTERAÇÃO", foreground="#f1c40f")
    tree.tag_configure("REMOÇÃO", foreground="#ff7675")
    tree.tag_configure("SAÍDA", foreground="#fab1a0")
    
    return frame, tree


def _preencher_historico(tree, lista):
    tree.delete(*tree.get_children())
    # Exibe do mais recente para o mais antigo (invertido)
    for i in reversed(lista):
        tipo = i["tipo"]
        
        # Monta um resumo descritivo dos detalhes baseado no tipo
        detalhe = ""
        if tipo == "ALTERAÇÃO":
            campo = i.get("campo_alterado", "")
            anterior = i.get("dados", {}).get(campo, "")
            detalhe = f"Campo '{campo}' alterado (ant.: {anterior})"
        elif tipo in ("ENTRADA", "SAÍDA", "REMOÇÃO"):
            est = i.get("dados", {}).get("estoque", "")
            preco = i.get("dados", {}).get("preco", 0.0)
            detalhe = f"Estoque: {est} | Preço: R$ {preco:.2f}"
        elif tipo == "REPOSIÇÃO":
            est_ant = i.get("dados", {}).get("estoque", "")
            qtd_rec = i.get("quantidade_recebida", "")
            detalhe = f"Estoque ant: {est_ant} | Recebido: {qtd_rec}"

        tree.insert("", "end", values=(
            i["data"], i["medicamento"], tipo, detalhe
        ), tags=(tipo,))


def _abrir_tela_frame(pai, titulo_texto):
    pai.pack_forget()
    win = tk.Frame(pai.master, bg=BG)
    win.pack(fill="both", expand=True)
    tk.Label(win, text=titulo_texto, font=("Helvetica", 16, "bold"), fg=VERDE, bg=BG).pack(pady=(18, 4))
    return win


# ---------------------------- TELAS DE HISTÓRICO ----------------------------

def tela_listar_historico(pai):
    win = _abrir_tela_frame(pai, "Histórico de Movimentações")

    frame, tree = _tabela_historico(win)
    frame.pack(fill="both", expand=True, padx=20, pady=5)
    _preencher_historico(tree, historico)

    tk.Label(win, text=f"Total de registros no histórico: {len(historico)}",
            font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG).pack(pady=4)

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    _botao(win, "Fechar", voltar, width=14).pack(pady=(2, 12))


def tela_desfazer_acao(pai, ao_atualizar=None):
    win = _abrir_tela_frame(pai, "Desfazer Última Ação")

    info_frame = tk.Frame(win, bg=BG_CARD)
    info_frame.pack(fill="x", padx=30, pady=15)

    if historico:
        ult = historico[-1]
        texto_info = (f"Última ação registrada:\n"
                    f"• Tipo: {ult['tipo']}\n"
                    f"• Medicamento: {ult['medicamento']}\n"
                    f"• Data/Hora: {ult['data']}")
    else:
        texto_info = "O histórico está vazio. Nenhuma ação para desfazer."

    tk.Label(info_frame, text=texto_info, font=("Helvetica", 11), fg=TEXTO, bg=BG_CARD,
            justify="left", padx=15, pady=15).pack(fill="both")

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def confirmar_desfazer():
        if not historico:
            messagebox.showinfo("Aviso", "Não há nenhuma ação para desfazer.", parent=win.winfo_toplevel())
            return

        if not messagebox.askyesno("Confirmar", "Deseja realmente desfazer a última ação realizada?", parent=win.winfo_toplevel()):
            return

        # Executa a função lógica de desfazer
        ult_tipo = historico[-1]['tipo']
        ult_med = historico[-1]['medicamento']
        
        desfazer_ultima()
        
        messagebox.showinfo("Sucesso", f"Ação de '{ult_tipo}' em '{ult_med}' foi desfeita com sucesso!", parent=win.winfo_toplevel())
        
        if ao_atualizar:
            ao_atualizar()
        voltar()

    if historico:
        _botao(win, "Desfazer Última Ação", confirmar_desfazer, cor=VERMELHO, hover=VERMELHO_CLARO, fg_hover=TEXTO).pack(pady=(10, 6))

    _botao(win, "Voltar", voltar).pack()


# ---------------------------- MENU DE HISTÓRICO ----------------------------

def menu_hist(janela_principal, tela_anterior):
    """Abre o menu de histórico como um Frame na janela principal, escondendo o anterior."""
    tela_anterior.pack_forget()
    
    frame_hist = tk.Frame(janela_principal, bg=BG)
    frame_hist.pack(fill="both", expand=True)

    tk.Label(
        frame_hist,
        text="Histórico",
        font=("Helvetica", 22, "bold"),
        fg=VERDE,
        bg=BG
    ).pack(pady=(25, 2))
    
    tk.Label(
        frame_hist,
        text="Auditoria e Rastreabilidade do Sistema",
        font=("Helvetica", 11),
        fg=AMARELO,
        bg=BG
    ).pack(pady=(0, 14))

    contador = tk.Label(frame_hist, font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG)
    contador.pack(pady=(0, 10))

    def atualizar_contador():
        contador.config(text=f"{len(historico)} registro(s) gravado(s) no histórico")
    
    atualizar_contador()

    def voltar():
        frame_hist.destroy()
        tela_anterior.pack(fill="both", expand=True)

    opcoes = [
        ("1. Visualizar histórico", lambda: tela_listar_historico(frame_hist)),
        ("2. Desfazer última ação", lambda: tela_desfazer_acao(frame_hist, atualizar_contador)),
        ("0. Voltar", voltar)
    ]
    
    for texto, comando in opcoes:
        cor_botao = VERMELHO if texto.startswith("0.") else BG_CARD
        hover_botao = VERMELHO_CLARO if texto.startswith("0.") else VERDE
        
        _botao(
            frame_hist, 
            texto, 
            comando, 
            cor=cor_botao, 
            hover=hover_botao, 
            width=32
        ).pack(pady=5)