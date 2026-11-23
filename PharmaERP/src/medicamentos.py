# medicamentos.py — CRUD da LISTA de medicamentos + MENU TKINTER
# Lógica (cadastrar, listar, buscar, alterar, remover, ordenar) fica separada da interface:
# as funções de lógica recebem valores já digitados e retornam True/False (nunca usam input/print).
import math
import tkinter as tk
from tkinter import messagebox, ttk

from .validar import (
    validar_medicamento,
    validar_estoque,
    validar_nome,
    validar_preco,
    validar_categoria,
    ler_float,
    ler_int
)
from .estruturas import medicamentos
from .registros import entrada, registrar_remocao, registrar_alteracao
from .reposicao import cadastrar_repo, buscar_repo, cancelar_repo, atualizar_repo
from .estoque import gerar_id

CATEGORIAS = ["ÉTICO", "GENÉRICO", "SIMILAR"]
ESTOQUE_MINIMO = 15

# ---------- PALETA (mesma da tela principal) ----------
BG = "#121820"
BG_CARD = "#1f2937"
VERDE = "#2ecc71"
VERDE_ESCURO = "#27ae60"
AMARELO = "#f1c40f"
VERMELHO = "#c0392b"
VERMELHO_CLARO = "#e74c3c"
TEXTO = "#000000"
TEXTO_SUAVE = "#bdc3c7"


# =====================================================================
#                              LÓGICA
# =====================================================================

# CONVERSORES (texto digitado -> número, sem quebrar)
def _to_int(texto):
    try:
        return int(str(texto).strip())
    except ValueError:
        return None


def _to_float(texto):
    try:
        valor = float(str(texto).strip().replace(",", "."))
    except ValueError:
        return None
    return valor if math.isfinite(valor) else None


# CADASTRO — retorna (True, "") ou (False, "motivo")
def cadastrar_medicamento(nome, categoria, estoque, preco):
    nome = str(nome).strip()
    categoria = str(categoria).strip().upper()
    estoque = _to_int(estoque)
    preco = _to_float(preco)

    if not validar_nome(nome, medicamentos):
        return False, "Nome inválido ou já cadastrado."
    if not validar_categoria(categoria):
        return False, "Categoria inválida."
    if estoque is None or not validar_estoque(estoque):
        return False, "Estoque deve ser um número inteiro maior ou igual a 0."
    if preco is None or not validar_preco(preco):
        return False, "Preço deve ser um número maior ou igual a 0."

    medicamento = {
        "medicamento": nome,
        "categoria": categoria,
        "estoque": estoque,
        "preco": preco,
        "id": gerar_id(),
    }

    if validar_medicamento(medicamento, medicamentos) is not True:
        return False, "Dados do medicamento inválidos."

    medicamentos.append(medicamento)
    entrada(medicamento)

    # estoque abaixo do mínimo -> abre solicitação de reposição
    if medicamento["estoque"] < ESTOQUE_MINIMO:
        cadastrar_repo(medicamento)
    return True, ""


# LISTAR TODOS — retorna a lista (vazia se não houver nenhum)
def listar_medicamentos():
    return medicamentos


# BUSCA POR CATEGORIA — O(n)
def buscar_medicamento_cat(categoria_nome):
    if not isinstance(categoria_nome, str):
        return []

    categoria_nome = categoria_nome.strip().lower()
    encontrados = []
    for medicamento in medicamentos:
        if medicamento["categoria"].strip().lower() == categoria_nome:
            encontrados.append(medicamento)
    return encontrados


# BUSCA POR NOME — O(1) melhor caso / O(n) pior caso
def buscar_medicamento(nome):
    if not isinstance(nome, str) or not nome.strip():
        return None

    nome = nome.strip().lower()
    for medicamento in medicamentos:
        if medicamento["medicamento"].strip().lower() == nome:
            return medicamento
    return None


# ALTERAR — campo: 1 = categoria, 2 = estoque, 3 = preço
def alterar_medicamento(nome, campo, novo_valor):
    medicamento = buscar_medicamento(nome)
    if medicamento is None:
        return False

    match campo:
        # ALTERAR CATEGORIA
        case 1:
            nova_categoria = str(novo_valor).strip().upper()
            if not validar_categoria(nova_categoria):
                return False
            if not registrar_alteracao(medicamento, "categoria"):
                return False
            medicamento["categoria"] = nova_categoria
            return True

        # ALTERAR ESTOQUE
        case 2:
            nova_quantidade = _to_int(novo_valor)
            if nova_quantidade is None or not validar_estoque(nova_quantidade):
                return False
            if not registrar_alteracao(medicamento, "estoque"):
                return False
            medicamento["estoque"] = nova_quantidade
            atualizar_repo(medicamento)  # cria/atualiza/cancela a reposição conforme o estoque
            return True

        # ALTERAR PREÇO
        case 3:
            novo_preco = _to_float(novo_valor)
            if novo_preco is None or not validar_preco(novo_preco):
                return False
            if not registrar_alteracao(medicamento, "preco"):
                return False
            medicamento["preco"] = novo_preco
            return True

        case _:
            return False


# REMOVER
def remover_medicamento(nome):
    medicamento = buscar_medicamento(nome)
    if medicamento is None:
        return False

    # cancela a reposição pendente antes de remover (o histórico guarda os dados)
    if buscar_repo(medicamento) is not None:
        cancelar_repo(medicamento)

    return registrar_remocao(medicamento) is True  # registra no histórico e remove da lista


# ORDENAR POR PREÇO (Bubble Sort, menor -> maior). Retorna nova lista.
def ordenar_por_preco(lista):
    v = lista.copy()
    for i in range(len(v)):
        trocou = False
        for j in range(len(v) - i - 1):
            if v[j]["preco"] > v[j + 1]["preco"]:
                v[j], v[j + 1] = v[j + 1], v[j]
                trocou = True
        if not trocou:
            break
    return v


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
        "Pharma.Treeview", background=BG_CARD, fieldbackground=BG_CARD,
        foreground=TEXTO, rowheight=26, borderwidth=0, font=("Helvetica", 10),
    )
    estilo.configure(
        "Pharma.Treeview.Heading", background=BG, foreground=AMARELO,
        font=("Helvetica", 10, "bold"), relief="flat",
    )
    estilo.map("Pharma.Treeview", background=[("selected", VERDE_ESCURO)],
            foreground=[("selected", TEXTO)])


def _tabela(pai, altura=12):
    """Cria uma Treeview com scrollbar e retorna (frame, tree)."""
    _estilizar_tabela()
    frame = tk.Frame(pai, bg=BG)
    colunas = ("id", "nome", "categoria", "estoque", "preco")
    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        height=altura, style="Pharma.Treeview")
    cabecalhos = {"id": ("ID", 50), "nome": ("Medicamento", 230),
                "categoria": ("Categoria", 110), "estoque": ("Estoque", 80),
                "preco": ("Preço (R$)", 100)}
    for col, (titulo, largura) in cabecalhos.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=largura, anchor="center" if col != "nome" else "w")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    tree.tag_configure("baixo", foreground="#ff7675")  # estoque abaixo do mínimo
    return frame, tree


def _preencher(tree, lista):
    tree.delete(*tree.get_children())
    for m in lista:
        tag = ("baixo",) if m["estoque"] < ESTOQUE_MINIMO else ()
        tree.insert("", "end", values=(
            m["id"], m["medicamento"], m["categoria"], m["estoque"], f"{m['preco']:.2f}"
        ), tags=tag)


def _janela_filha(pai, titulo, largura, altura):
    win = tk.Toplevel(pai)
    win.title(titulo)
    win.geometry(f"{largura}x{altura}")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.transient(pai)
    win.grab_set()  # modal: foco só nesta janela até fechar
    return win


def _campo(pai, rotulo, **opts):
    tk.Label(pai, text=rotulo, font=("Helvetica", 10), fg=TEXTO_SUAVE, bg=BG,
            anchor="w").pack(fill="x", padx=30, pady=(10, 2))
    entry = tk.Entry(pai, font=("Helvetica", 11), bg=BG_CARD, fg=TEXTO,
                     insertbackground=TEXTO, relief="flat", **opts)
    entry.pack(fill="x", padx=30, ipady=5)
    return entry


def _combo_categoria(pai, rotulo="Categoria"):
    tk.Label(pai, text=rotulo, font=("Helvetica", 10), fg=TEXTO_SUAVE, bg=BG,
            anchor="w").pack(fill="x", padx=30, pady=(10, 2))
    combo = ttk.Combobox(pai, values=CATEGORIAS, state="readonly", font=("Helvetica", 11))
    combo.current(0)
    combo.pack(fill="x", padx=30, ipady=3)
    return combo


def _titulo(pai, texto):
    tk.Label(pai, text=texto, font=("Helvetica", 16, "bold"), fg=VERDE, bg=BG).pack(pady=(18, 4))


# ---------------------------- TELAS (como Frames) ----------------------------

def _abrir_tela_frame(pai, titulo_texto, largura, altura):
    """Função auxiliar para ocultar a tela anterior e criar um frame estruturado para a sub-tela."""
    pai.pack_forget() # Esconde o menu de medicamentos
    
    # Cria um container/frame para a nova tela
    win = tk.Frame(pai.master, bg=BG)
    win.pack(fill="both", expand=True)
    
    _titulo(win, titulo_texto)
    return win


def tela_cadastrar(pai, ao_salvar=None):
    win = _abrir_tela_frame(pai, "Cadastrar Medicamento", 400, 440)

    e_nome = _campo(win, "Nome do medicamento")
    c_cat = _combo_categoria(win)
    e_estoque = _campo(win, "Estoque")
    e_preco = _campo(win, "Preço (R$)")
    e_nome.focus_set()

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True) # Retorna ao menu anterior

    def salvar():
        ok, erro = cadastrar_medicamento(e_nome.get(), c_cat.get(),
                                        e_estoque.get(), e_preco.get())
        if not ok:
            messagebox.showerror("Erro ao cadastrar", erro, parent=win.winfo_toplevel())
            return
        msg = "Medicamento cadastrado com sucesso!"
        if buscar_repo(e_nome.get()) is not None:
            msg += "\nEstoque abaixo do mínimo: reposição solicitada."
        messagebox.showinfo("Sucesso", msg, parent=win.winfo_toplevel())
        if ao_salvar:
            ao_salvar()
        voltar()

    win.bind("<Return>", lambda _e: salvar())
    _botao(win, "Salvar", salvar, cor=VERDE, hover=VERDE_ESCURO, fg_hover=TEXTO).pack(pady=(22, 6))
    _botao(win, "Cancelar", voltar, cor=VERMELHO, hover=VERMELHO_CLARO).pack()


def tela_listar(pai):
    win = _abrir_tela_frame(pai, "Medicamentos Cadastrados", 640, 470)

    frame, tree = _tabela(win)
    frame.pack(fill="both", expand=True, padx=20, pady=5)
    _preencher(tree, listar_medicamentos())

    tk.Label(win, text=f"Total: {len(medicamentos)}   |   Vermelho = abaixo de {ESTOQUE_MINIMO} un.",
            font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG).pack(pady=4)
            
    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    _botao(win, "Fechar", voltar, width=14).pack(pady=(2, 12))


def tela_buscar(pai):
    win = _abrir_tela_frame(pai, "Buscar Medicamento", 640, 500)

    barra = tk.Frame(win, bg=BG)
    barra.pack(fill="x", padx=20, pady=5)

    modo = tk.StringVar(value="nome")
    for texto, valor in (("Por nome", "nome"), ("Por categoria", "categoria")):
        tk.Radiobutton(barra, text=texto, variable=modo, value=valor, bg=BG, fg=TEXTO,
                    selectcolor=BG_CARD, activebackground=BG, activeforeground=VERDE,
                    font=("Helvetica", 10)).pack(side="left", padx=(0, 12))

    e_busca = tk.Entry(barra, font=("Helvetica", 11), bg=BG_CARD, fg=TEXTO,
                    insertbackground=TEXTO, relief="flat", width=18)
    e_busca.pack(side="left", ipady=4, padx=4)
    combo = ttk.Combobox(barra, values=CATEGORIAS, state="readonly", width=12,
                        font=("Helvetica", 10))
    combo.current(0)

    def trocar_modo(*_):
        if modo.get() == "nome":
            combo.pack_forget()
            e_busca.pack(side="left", ipady=4, padx=4)
        else:
            e_busca.pack_forget()
            combo.pack(side="left", ipady=3, padx=4)
    modo.trace_add("write", trocar_modo)

    frame, tree = _tabela(win, altura=10)
    frame.pack(fill="both", expand=True, padx=20, pady=5)

    def buscar():
        if modo.get() == "nome":
            if not e_busca.get().strip():
                messagebox.showwarning("Atenção", "Digite o nome do medicamento.", parent=win.winfo_toplevel())
                return
            med = buscar_medicamento(e_busca.get())
            resultado = [med] if med else []
        else:
            resultado = buscar_medicamento_cat(combo.get())
        _preencher(tree, resultado)
        if not resultado:
            messagebox.showinfo("Busca", "Nenhum medicamento encontrado.", parent=win.winfo_toplevel())

    win.bind("<Return>", lambda _e: buscar())
    _botao(barra, "Buscar", buscar, cor=VERDE, hover=VERDE_ESCURO, fg_hover=TEXTO, width=9).pack(side="left", padx=6)
    e_busca.focus_set()
    
    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    _botao(win, "Fechar", voltar, width=14).pack(pady=(2, 12))


def tela_alterar(pai, ao_salvar=None):
    win = _abrir_tela_frame(pai, "Alterar Medicamento", 400, 440)

    e_nome = _campo(win, "Nome do medicamento")
    e_nome.focus_set()

    tk.Label(win, text="Campo a alterar", font=("Helvetica", 10), fg=TEXTO_SUAVE, bg=BG,
            anchor="w").pack(fill="x", padx=30, pady=(10, 2))
    campos = {"Categoria": 1, "Estoque": 2, "Preço": 3}
    c_campo = ttk.Combobox(win, values=list(campos), state="readonly", font=("Helvetica", 11))
    c_campo.current(0)
    c_campo.pack(fill="x", padx=30, ipady=3)

    # Rótulo e campos do novo valor criados em sequência para manter a ordem correta
    rotulo = tk.Label(win, text="Nova categoria", font=("Helvetica", 10), fg=TEXTO_SUAVE,
                    bg=BG, anchor="w")
    rotulo.pack(fill="x", padx=30, pady=(10, 2))
    
    c_valor = ttk.Combobox(win, values=CATEGORIAS, state="readonly", font=("Helvetica", 11))
    c_valor.current(0)
    c_valor.pack(fill="x", padx=30, ipady=3)
    
    e_valor = tk.Entry(win, font=("Helvetica", 11), bg=BG_CARD, fg=TEXTO,
                    insertbackground=TEXTO, relief="flat")
    # Como inicia com "Categoria", começamos com o combobox visível e escondemos o entry
    e_valor.pack_forget()

    def trocar_campo(_e=None):
        escolhido = c_campo.get()
        rotulo.config(text="Nova categoria" if escolhido == "Categoria"
                    else f"Novo valor de {escolhido.lower()}")
        
        # Reposiciona corretamente logo abaixo do rótulo e ACIMA dos botões
        if escolhido == "Categoria":
            e_valor.pack_forget()
            c_valor.pack(fill="x", padx=30, ipady=3, after=rotulo)
        else:
            c_valor.pack_forget()
            e_valor.delete(0, "end")
            e_valor.pack(fill="x", padx=30, ipady=5, after=rotulo)
            
    c_campo.bind("<<ComboboxSelected>>", trocar_campo)

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def salvar():
        nome = e_nome.get()
        if buscar_medicamento(nome) is None:
            messagebox.showerror("Erro", "Medicamento não encontrado.", parent=win.winfo_toplevel())
            return
        campo = campos[c_campo.get()]
        valor = c_valor.get() if campo == 1 else e_valor.get()
        if not alterar_medicamento(nome, campo, valor):
            messagebox.showerror("Erro", "Valor inválido.", parent=win.winfo_toplevel())
            return
        messagebox.showinfo("Sucesso", "Medicamento alterado com sucesso!", parent=win.winfo_toplevel())
        if ao_salvar:
            ao_salvar()
        voltar()

    win.bind("<Return>", lambda _e: salvar())
    
    # Criamos os botões por último para garantir que fiquem sempre embaixo de tudo
    _botao(win, "Salvar", salvar, cor=VERDE, hover=VERDE_ESCURO, fg_hover=TEXTO).pack(pady=(22, 6))
    _botao(win, "Cancelar", voltar, cor=VERMELHO, hover=VERMELHO_CLARO).pack()

def tela_remover(pai, ao_salvar=None):
    win = _abrir_tela_frame(pai, "Remover Medicamento", 400, 280)

    e_nome = _campo(win, "Nome do medicamento")
    e_nome.focus_set()

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    def remover():
        nome = e_nome.get()
        med = buscar_medicamento(nome)
        if med is None:
            messagebox.showerror("Erro", "Medicamento não encontrado.", parent=win.winfo_toplevel())
            return
        if not messagebox.askyesno(
            "Confirmar remoção",
            f"Remover '{med['medicamento']}' do sistema?\n(Reposição pendente também será cancelada.)",
            parent=win.winfo_toplevel(),
        ):
            return
        if remover_medicamento(nome):
            messagebox.showinfo("Sucesso", "Medicamento removido!", parent=win.winfo_toplevel())
            if ao_salvar:
                ao_salvar()
            voltar()
        else:
            messagebox.showerror("Erro", "Não foi possível remover.", parent=win.winfo_toplevel())

    win.bind("<Return>", lambda _e: remover())
    _botao(win, "Remover", remover, cor=VERMELHO, hover=VERMELHO_CLARO).pack(pady=(22, 6))
    _botao(win, "Cancelar", voltar).pack()


def tela_ordenar(pai):
    win = _abrir_tela_frame(pai, "Medicamentos por Preço (menor → maior)", 640, 470)

    frame, tree = _tabela(win)
    frame.pack(fill="both", expand=True, padx=20, pady=5)
    _preencher(tree, ordenar_por_preco(medicamentos))

    def voltar():
        win.destroy()
        pai.pack(fill="both", expand=True)

    _botao(win, "Fechar", voltar, width=14).pack(pady=(8, 12))



# ---------------------------- MENU ----------------------------

def menu_med(janela_principal, tela_anterior):
    """Abre o menu de medicamentos como um Frame, escondendo a tela anterior."""
    tela_anterior.pack_forget()
    
    frame_med = tk.Frame(janela_principal, bg=BG)
    frame_med.pack(fill="both", expand=True)

    tk.Label(
        frame_med,
        text="Medicamentos",
        font=("Helvetica", 22, "bold"),
        fg=VERDE,
        bg=BG
    ).pack(pady=(25, 2))
    
    tk.Label(
        frame_med,
        text="Menu de Medicamentos",
        font=("Helvetica", 11),
        fg=AMARELO,
        bg=BG
    ).pack(pady=(0, 14))

    contador = tk.Label(frame_med, font=("Helvetica", 9), fg=TEXTO_SUAVE, bg=BG)
    contador.pack(pady=(0, 10))

    def atualizar_contador():
        contador.config(text=f"{len(medicamentos)} medicamento(s) cadastrado(s)")
    
    atualizar_contador()

    def voltar():
        frame_med.destroy()
        tela_anterior.pack(fill="both", expand=True)

    opcoes = [
        ("1. Cadastrar medicamento", lambda: tela_cadastrar(frame_med, atualizar_contador)),
        ("2. Listar medicamentos", lambda: tela_listar(frame_med)),
        ("3. Buscar (nome / categoria)", lambda: tela_buscar(frame_med)),
        ("4. Alterar medicamento", lambda: tela_alterar(frame_med, atualizar_contador)),
        ("5. Remover medicamento", lambda: tela_remover(frame_med, atualizar_contador)),
        ("6. Ordenar por preço", lambda: tela_ordenar(frame_med)),
        ("0. Voltar", voltar)
    ]
    
    for texto, comando in opcoes:
        # Se for a opção de voltar ("0."), coloca a cor vermelha; senão, usa a cor padrão do card
        cor_botao = VERMELHO if texto.startswith("0.") else BG_CARD
        hover_botao = VERMELHO_CLARO if texto.startswith("0.") else VERDE
        
        _botao(
            frame_med, 
            texto, 
            comando, 
            cor=cor_botao, 
            hover=hover_botao, 
            width=30
        ).pack(pady=5)