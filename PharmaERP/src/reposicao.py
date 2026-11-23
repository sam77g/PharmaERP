# ARQUIVO EXCLUSIVO PARA AS REPOSIÇÕES reposicao.py 
# =========== IMPORTS ===========
from .validar import validar_estoque
from collections import deque
from .estoque import gerar_id, gerar_id_repo
from .estruturas import solicitacoes_reposicao, limpar_tela, medicamentos 
from .registros import registrar_reposicao
import tkinter as tk
from tkinter import messagebox, ttk


def menu_repo() :
    print()


# FUNÇÃO DE BUSCA 
# aceita o dicionário do medicamento OU só o nome (str); nunca imprime, nunca quebra
"""COMPLEXIDADE 
    - O(n) no pior caso
    - O(1) no melhor caso
"""
def buscar_repo(med):
    if med is None:
        return None

    # se veio dict pega o nome dele, se veio str usa direto
    nome = med["medicamento"] if isinstance(med, dict) else med
    nome = str(nome).strip().lower()   # tira espaço e ignora maiúscula/minúscula

    if not nome:    # string vazia
        return None

    # busca linear na fila comparando pelo nome 
    # Complexidade O(n)
    for repo in solicitacoes_reposicao:
        if repo["medicamento"].strip().lower() == nome:
            return repo

    return None

# FUNÇÃO DE CADASTRAR REPOSIÇÃO 
"""
    COMPLEXIDADE 
    - O(n) no pior caso
    - O(n) no melhor caso
"""
def cadastrar_repo(med) :
    # pega o ID e nome do remédio 

    # se já tem reposição pra esse remédio não duplica
    repo_existente = buscar_repo(med)
    
    if repo_existente is not None :
        return
    # DICIONÁRIO PARA CADA MEDICAMENTO
    repor = {
        "medicamento" : med["medicamento"],
        "id_repo" : gerar_id_repo(),
        "id_medicamento" : med["id"],                    # liga a reposição ao cadastro do remédio
        "criticidade" : criticidade(med["estoque"]),
        "quantidade_solicitada" : 15 - med["estoque"]    # 15 = estoque mínimo, pede só o que falta
    }
    # INSERE A PRIORIDADE
    inserir_por_prioridade(repor) 



# FUNÇÃO PARA LISTAR AS SOLITAÇÕES
"""
    COMPLEXIDADE 
    - O(n) no pior caso
    - O(n) no melhor caso
"""
def listar_repo():
    
    if not solicitacoes_reposicao:   # fila vazia
        return False
    
    return solicitacoes_reposicao
        
        
# função auxiliar 
# define o nível de acordo com o estoque atual
"""
    COMPLEXIDADE O(1)
"""
def criticidade(estoque):
    if estoque < 5:
        return "CRÍTICO"
    elif estoque < 10:
        return "ALERTA"
    return "AVISO"      # de 10 a 14
        
# FUNÇÃO PARA A REMOÇÃO DE SOLITAÇÃO
# também aceita dict ou nome, igual a buscar_repo
"""
    COMPLEXIDADE 
    - O(n) no pior caso
    - O(1) no melhor caso
"""
def cancelar_repo(med):
    nome = med["medicamento"] if isinstance(med, dict) else med
    nome = str(nome).strip().lower()
    for repo in solicitacoes_reposicao:
        if repo["medicamento"].strip().lower() == nome:
            solicitacoes_reposicao.remove(repo)   # remove pelo objeto, pode estar em qualquer posição
            return True
    return False
            
            
# ATENDE A PRIMEIRA REPOSIÇÃO DA FILA
"""
    COMPLEXIDADE 
    - O(m+1) no pior caso, m = quantidade de medicamentos cadastrados.
    - O(1) no melhor caso
"""

def atender_reposicao(qtd):
    if not solicitacoes_reposicao:
        return None

    repo = solicitacoes_reposicao[0]

    if not validar_estoque(qtd) or qtd == 0:
        return False

    # Procura o medicamento pelo ID
    med = None

    for m in medicamentos:
        if m["id"] == repo["id_medicamento"]:
            med = m
            break

    # Verifica se o medicamento ainda existe
    if med is None:
        solicitacoes_reposicao.popleft()
        return False

    # Registra no histórico antes de alterar o estoque
    if not registrar_reposicao(med, qtd):
        return False

    # Remove a solicitação atendida
    solicitacoes_reposicao.popleft()

    # Atualiza o estoque
    med["estoque"] += qtd


    # Se continuar abaixo do mínimo, cria outra solicitação
    if med["estoque"] < 15:
        cadastrar_repo(med)


# ALTERA A QUANTIDADE SOLICITADA DE UMA REPOSIÇÃO
"""
    COMPLEXIDADE 
    - O(n) no pior caso
    - O(1) no melhor caso
"""
def alterar_repo(nome, qtd):
    repo = buscar_repo(nome)
    if repo is None:
        return False
    
    if not validar_estoque(qtd) :    # não aceita 0 nem negativo
        return False
    repo["quantidade_solicitada"] = qtd   # repo é a referência da fila, então já atualiza lá
    return True

# FUNÇÃO PARA ATUALIZAR A REPOSIÇAO
def atualizar_repo(med):
    repo = buscar_repo(med)

    if repo is None:
        if med["estoque"] < 15:
            cadastrar_repo(med)
        return

    if med["estoque"] >= 15:
        cancelar_repo(med)
        return

    cancelar_repo(med)
    cadastrar_repo(med)

# menor número = maior prioridade
PRIORIDADE = {"CRÍTICO": 0, "ALERTA": 1, "AVISO": 2}

# insere já na posição certa; empate vai depois dos que já estavam (FIFO)
"""
    COMPLEXIDADE 
    - O(n) no pior caso
    - O(1) no melhor caso
"""
def inserir_por_prioridade(repo):
    p = PRIORIDADE[repo["criticidade"]]
    pos = len(solicitacoes_reposicao)          # padrão: fim da fila
    for i, r in enumerate(solicitacoes_reposicao):
        if PRIORIDADE[r["criticidade"]] > p:   # primeiro com prioridade menor
            pos = i
            break
    solicitacoes_reposicao.insert(pos, repo)
    
    

# ---------- PALETA (mesma padrão do sistema) ----------
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
        "PharmaRepo.Treeview", background=BG_CARD, fieldbackground=BG_CARD,
        foreground=TEXTO, rowheight=26, borderwidth=0, font=("Helvetica", 10),
    )
    estilo.configure(
        "PharmaRepo.Treeview.Heading", background=BG, foreground=AMARELO,
        font=("Helvetica", 10, "bold"), relief="flat",
    )
    estilo.map("PharmaRepo.Treeview", background=[("selected", VERDE_ESCURO)],
            foreground=[("selected", TEXTO)])


def _tabela_repo(pai, altura=12):
    _estilizar_tabela()
    frame = tk.Frame(pai, bg=BG)
    colunas = ("id_repo", "medicamento", "criticidade", "qtd", "id_med")
    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        height=altura, style="PharmaRepo.Treeview")
    cabecalhos = {
        "id_repo": ("ID Repo", 70), 
        "medicamento": ("Medicamento", 180),
        "criticidade": ("Criticidade", 100), 
        "qtd": ("Qtd Solicitada", 90),
        "id_med": ("ID Med", 60)
    }
    for col, (titulo, largura) in cabecalhos.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=largura, anchor="center" if col != "medicamento" else "w")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    
    # Tags para colorir criticidades na tabela
    tree.tag_configure("CRÍTICO", foreground="#ff7675")
    tree.tag_configure("ALERTA", foreground="#ffeaa7")
    tree.tag_configure("AVISO", foreground="#74b9ff")
    return frame, tree


def _preencher_repo(tree, lista):
    tree.delete(*tree.get_children())
    for r in lista:
        crit = r["criticidade"]
        tree.insert("", "end", values=(
            r["id_repo"], r["medicamento"], crit, r["quantidade_solicitada"], r["id_medicamento"]
        ), tags=(crit,))


def _abrir_tela_frame(pai, titulo_texto):
    pai.pack_forget()
    win = tk.Frame(pai.master, bg=BG)
    win.pack(fill="both", expand=True)
    tk.Label(win, text=titulo_texto, font=("Helvetica", 16, "bold"), fg=VERDE, bg=BG).pack(pady=(18, 4))
    return win


def _campo(pai, rotulo, **opts):
    tk.Label(pai, text=rotulo, font=("Helvetica", 10), fg=TEXTO_SUAVE, bg=BG,
            anchor="w").pack(fill="x", padx=30, pady=(10, 2))
    entry = tk.Entry(pai, font=("Helvetica", 11), bg=BG_CARD, fg=TEXTO,
                     insertbackground=TEXTO, relief="flat", **opts)
    entry.pack(fill="x", padx=30, ipady=5)
    return entry


# ---------------------------- TELAS DE REPOSIÇÃO ----------------------------

def tela_listar_repo(pai):
    win = _abrir_tela_frame(pai, "Fila de Reposições Pendentes")

    frame, tree = _tabela_repo(win)
    frame.pack(fill="both", expand=True, padx=20, pady=5)
    _preencher_repo(tree, solicitacoes_reposicao)

    tk.Label(win, text="Vermelho = Crítico | Amarelo = Alerta | Azul = Aviso",
            font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG).pack(pady=4)

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    _botao(win, "Fechar", voltar, width=14).pack(pady=(2, 12))


def tela_atender_repo(pai, ao_atualizar=None):
    win = _abrir_tela_frame(pai, "Atender Primeira Reposição")

    # Exibe informações da primeira reposição da fila, se houver
    info_frame = tk.Frame(win, bg=BG_CARD)
    info_frame.pack(fill="x", padx=30, pady=10)

    if solicitacoes_reposicao:
        primeira = solicitacoes_reposicao[0]
        texto_info = (f"Próximo da Fila:\n"
                    f"• Medicamento: {primeira['medicamento']}\n"
                    f"• Criticidade: {primeira['criticidade']}\n"
                    f"• Sugerido para repor: {primeira['quantidade_solicitada']} un.")
    else:
        texto_info = "Nenhuma reposição pendente na fila no momento."

    tk.Label(info_frame, text=texto_info, font=("Helvetica", 11), fg=TEXTO, bg=BG_CARD,
            justify="left", padx=15, pady=15).pack(fill="both")

    e_qtd = _campo(win, "Quantidade real recebida (lote):")
    if solicitacoes_reposicao:
        e_qtd.focus_set()

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def atender():
        if not solicitacoes_reposicao:
            messagebox.showinfo("Aviso", "A fila de reposição está vazia.", parent=win.winfo_toplevel())
            return
        
        qtd_digitada = e_qtd.get().strip()
        try:
            qtd = int(qtd_digitada)
        except ValueError:
            messagebox.showerror("Erro", "Digite um número inteiro válido para a quantidade.", parent=win.winfo_toplevel())
            return

        resultado = atender_reposicao(qtd)
        if resultado is False:
            messagebox.showerror("Erro", "Quantidade inválida ou erro ao registrar no histórico.", parent=win.winfo_toplevel())
            return

        messagebox.showinfo("Sucesso", "Reposição atendida e estoque atualizado com sucesso!", parent=win.winfo_toplevel())
        if ao_atualizar:
            ao_atualizar()
        voltar()

    if solicitacoes_reposicao:
        win.bind("<Return>", lambda _e: atender())
        _botao(win, "Confirmar Atendimento", atender, cor=VERDE, hover=VERDE_ESCURO, fg_hover=TEXTO).pack(pady=(15, 6))
    
    _botao(win, "Voltar", voltar, cor=VERMELHO, hover=VERMELHO_CLARO).pack()


def tela_alterar_repo(pai):
    win = _abrir_tela_frame(pai, "Alterar Quantidade Solicitada")

    e_nome = _campo(win, "Nome do medicamento")
    e_qtd = _campo(win, "Nova quantidade desejada")
    e_nome.focus_set()

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def salvar():
        nome = e_nome.get()
        if not buscar_repo(nome):
            messagebox.showerror("Erro", "Reposição não encontrada para este medicamento.", parent=win.winfo_toplevel())
            return
        
        try:
            qtd = int(e_qtd.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.", parent=win.winfo_toplevel())
            return

        if alterar_repo(nome, qtd):
            messagebox.showinfo("Sucesso", "Quantidade da reposição alterada!", parent=win.winfo_toplevel())
            voltar()
        else:
            messagebox.showerror("Erro", "Não foi possível alterar (verifique se a quantidade é maior que 0).", parent=win.winfo_toplevel())

    win.bind("<Return>", lambda _e: salvar())
    _botao(win, "Salvar Alteração", salvar, cor=VERDE, hover=VERDE_ESCURO, fg_hover=TEXTO).pack(pady=(15, 6))
    _botao(win, "Cancelar", voltar, cor=VERMELHO, hover=VERMELHO_CLARO).pack()


def tela_cancelar_repo(pai):
    win = _abrir_tela_frame(pai, "Cancelar/Remover Solicitação")

    e_nome = _campo(win, "Nome do medicamento")
    e_nome.focus_set()

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def cancelar():
        nome = e_nome.get()
        repo = buscar_repo(nome)
        if not repo:
            messagebox.showerror("Erro", "Nenhuma solicitação encontrada para este medicamento.", parent=win.winfo_toplevel())
            return

        if not messagebox.askyesno("Confirmar", f"Deseja remover a solicitação de reposição de '{repo['medicamento']}'?", parent=win.winfo_toplevel()):
            return

        if cancelar_repo(nome):
            messagebox.showinfo("Sucesso", "Solicitação cancelada com sucesso!", parent=win.winfo_toplevel())
            voltar()
        else:
            messagebox.showerror("Erro", "Erro ao cancelar solicitação.", parent=win.winfo_toplevel())

    win.bind("<Return>", lambda _e: cancelar())
    _botao(win, "Remover Solicitação", cancelar, cor=VERMELHO, hover=VERMELHO_CLARO).pack(pady=(15, 6))
    _botao(win, "Voltar", voltar).pack()


# ---------------------------- MENU DE REPOSIÇÃO ----------------------------

def menu_repo(janela_principal, tela_anterior):
    """Abre o menu de reposição como um Frame na janela principal, escondendo o menu anterior."""
    tela_anterior.pack_forget()
    
    frame_repo = tk.Frame(janela_principal, bg=BG)
    frame_repo.pack(fill="both", expand=True)

    tk.Label(
        frame_repo,
        text="Reposição",
        font=("Helvetica", 22, "bold"),
        fg=VERDE,
        bg=BG
    ).pack(pady=(25, 2))
    
    tk.Label(
        frame_repo,
        text="Gerenciamento de Fila e Suprimentos",
        font=("Helvetica", 11),
        fg=AMARELO,
        bg=BG
    ).pack(pady=(0, 14))

    contador = tk.Label(frame_repo, font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG)
    contador.pack(pady=(0, 10))

    def atualizar_contador():
        contador.config(text=f"{len(solicitacoes_reposicao)} solicitação(ões) pendente(s) na fila")
    
    atualizar_contador()

    def voltar():
        frame_repo.destroy()
        tela_anterior.pack(fill="both", expand=True)

    opcoes = [
        ("1. Listar solicitações de reposição", lambda: tela_listar_repo(frame_repo)),
        ("2. Atender primeira reposição", lambda: tela_atender_repo(frame_repo, atualizar_contador)),
        ("3. Alterar quantidade solicitada", lambda: tela_alterar_repo(frame_repo)),
        ("4. Cancelar solicitação", lambda: tela_cancelar_repo(frame_repo)),
        ("0. Voltar", voltar)
    ]
    
    for texto, comando in opcoes:
        cor_botao = VERMELHO if texto.startswith("0.") else BG_CARD
        hover_botao = VERMELHO_CLARO if texto.startswith("0.") else VERDE
        
        _botao(
            frame_repo, 
            texto, 
            comando, 
            cor=cor_botao, 
            hover=hover_botao, 
            width=32
        ).pack(pady=5)