# Este arquivo será responsável pelo CRUD - LISTA
# Aqui ficará as funções de adicionar, ler, deletar e atualizar os medicamentos
# ex. de funções : 
# cadastrar_medicamento()
# listar_medicamentos()
# buscar_medicamento()
# alterar_medicamento()
# remover_medicamento()
# Também terá algumas validações
from .validar import (
    validar_medicamento,
    validar_estoque,
    validar_nome,
    validar_preco,
    validar_categoria
)
from .estruturas import medicamentos
from .registros import entrada, registrar_remocao, registrar_alteracao
from .reposicao import cadastrar_repo, buscar_repo, cancelar_repo
from .estoque import gerar_id
import tkinter as tk
from tkinter import messagebox, simpledialog

def iniciar_menu_med() :
    janela_menu = Tk.Toplevel()
    janela_menu.title("PharmaERP - Menu Medicamentos")
    janela_menu.geometry("520x430")
    janela_menu.resizable(False, False)
    janela_menu.configure(bg="#121820")
    janela_menu.eval("tk::PlaceWindow . center")
    #tela de boas vindas 
    tela_boas_vindas = tk.Frame(janela, bg="#121820")
    tela_boas_vindas.pack(fill="both", expand=True)
    
    tk.Button(
        janela_menu,
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
        command=menu_med
    ).pack(pady=15)


# MENU DE MEDICAMENTOS
def menu_med(valor) :
    op = valor
    # MATCH CASE PARA O MENU
    match op : # ainda não sei o que fazer aqui
        # adicionar medicamento
        case 1 :
            # ENTRADA DE NOME
            nome_label = tk.Label(janela_menu, text="Digite o nome do medicamento:")
            nome_label.pack()
            
            nome_entry = tk.Entry(janela_menu)
            nome_entry.pack()
            
            if not validar_nome(nome, medicamentos) :
                messagebox.showerror("NOME INVÁLIDO", "Nome digitado inválido !")
                return False
            
            # ENTRADA DE ESTOQUE
            estoque_label = tk.Label(janela_menu, text="Digite o estoque:")
            estoque_label.pack()
            
            estoque_entry = tk.Entry(janela_menu)
            estoque_entry.pack()
            
            if not validar_estoque(estoque_entry) :
                messagebox.showerror("ESTOQUE INVÁLIDO", "Estoque digitado inválido !")
                return False
            
            #  ENTRADA DE PREÇO
            preco_label = tk.Label(janela_menu, text="Digite o preço :")
            preco_label.pack()
            
            preco_entry = tk.Entry(janela_menu)
            preco_entry.pack()
            
            if not validar_preco(preco_entry) :
                messagebox.showerror("PREÇO INVÁLIDO", "Preço digitado inválido !")
                return False
            
            
            # dicionário do medicamento
            medicamento = {
                "medicamento": nome,
                "categoria": categoria(),
                "estoque": estoque,
                "preco": preco, # valida e adiciona o preço
                "id": gerar_id() # gera um ID único para o medicamento 
            }
            
            # VALIDA OS DADOS DO MEDICAMENTO
            resultado = validar_medicamento(
                medicamento,
                medicamentos
            )
            
            if resultado is True:
                # CADASTRA O MEDICAMENTO
                cadastrar_medicamento(medicamento)
                # VERIFICA SE O ESTOQUE ESTÁ ABAIXO DO MÍNIMO [15]
                if medicamento["estoque"] < 15:
                    cadastrar_repo(medicamento)                    
            else:
                return False
        
        # ALTERAÇÃO DE MEDICAMENTO
        case 2 :
            if len(medicamentos) == 1 :
                nome = medicamentos[0]["medicamento"]
                alterar_medicamento(nome)
            else :
                alterar_medicamento(alt) # redireciona para a função de alteração
            
            time.sleep(1)
        
        # REMOÇÃO DE MEDICAMENTO
        case 3 :
            if len(medicamentos) == 1 :
                nome = medicamentos[0]["medicamento"]
                remover_medicamento(nome) # redireciona para a função de remoção
            else :
                rem_label = tk.Label(janela_menu, text="Digite o medicamento :")
                rem_label.pack()
                
                rem_entry = tk.Entry(janela_menu)
                rem_entry.pack()    
                
                remover_medicamento(rem_entry) # redireciona para a função de remoção
                time.sleep(1)
                
            
        # LISTA TODOS OS MEDICAMENTOS CADASTRADOS
        case 4 :
            listar_medicamentos() # chamada da função de listagem

        # BUSCA DE MEDICAMENTO
        case 5 :
            if len(medicamentos) == 1 :
                nome = medicamentos[0]["medicamento"]
                buscar_medicamento(nome) # chamada da função de busca
            else :
                buscar_medicamento(busca) # chamada da função de busca
                
            
        
        # LISTAGEM/BUSCA FILTRADA
        case 6 :
            opc_busca_categoria = categoria() # recebe o valor para filtragem
            buscar_medicamento_cat(opc_busca_categoria) # lista pela categoria
            

        # LISTAGEM ORDENADA POR PREÇO
        case 7 :
            for i in ordenar_por_preco(medicamentos): # percorre e ordena os medicamentos
                # printa no terminal
                print(f"{i['medicamento'].upper()} - R$ {i['preco']} (estoque: {i['estoque']})")
                
            
            
        # SAÍDA
        case 0 :
            break
        
        # VALOR INVÁLIDO 
        case _ :
            return False
        
    janela_menu.mainloop()

def menu_medicamentos() :   
    print("menu medicamentos")

# FUNÇÃO PARA LIMPAR TELA
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# FUNÇÃO PARA CATEGORIAS
def categoria(valor) :
    while True:
        if ler_int(valor) :
            op = valor
            if op == 1: return "ÉTICO"
            if op == 2: return "GENÉRICO"
            if op == 3: return "SIMILAR"
        return False

# FUNÇAO DE CADASTRO DE MEDICAMENTOS
def cadastrar_medicamento(med):
    if validar_medicamento(med, medicamentos) is not True:
        return False

    medicamentos.append(med)
    entrada(med)
    return True


# FUNÇAO DE LISTAR TODOS OS MEDICAMENTOS
def listar_medicamentos() :
    
    if len(medicamentos) == 0 : 
        return False
    else :
        return medicamentos
        


# FUNÇÃO DE BUSCAR MEDICAMENTOS POR CATEGORIA
""" 
Complexidade O(n)
"""
def buscar_medicamento_cat(categoria_nome):
    # filtra todos os medicamentos da mesma categoria
    # Equivale a :
    # encontrados = [
    #     # percorre a lista de medicamentos 
    #     m for m in medicamentos 
    #     # e guarda os correspondedes em uma lista nova
    #     if m["categoria"].strip().lower() == categoria_nome.strip().lower()
    # ]
    
    if not isinstance(categoria_nome, str): # valida
        return []

    categoria_nome = categoria_nome.strip().lower()
    encontrados = []

    for medicamento in medicamentos: # busca
        if medicamento["categoria"].strip().lower() == categoria_nome: # compara
            encontrados.append(medicamento) # adiciona na lista

    return encontrados

# FUNÇÃO DE BUSCAR MEDICAMENTOS PELO NOME
# Complexidade :
# O(1) no melhor caso 
# O(n) no pior caso
def buscar_medicamento(nome):
    if not isinstance(nome, str) or not nome.strip():
        return None

    nome = nome.strip().lower()

    for medicamento in medicamentos:
        if medicamento["medicamento"].strip().lower() == nome:
            return medicamento

    return None

    
# função de alterar características do medicamento através do nome digitado
def alterar_medicamento(nome, campo, novo_valor) :
    nome = nome.strip().lower() # normalizando o nome
        
    for medicamento in medicamentos: # percorre a lista de medicamentos
        if medicamento["medicamento"].strip().lower() == nome: # verifica se o nome digitado está presente na lista
            opcao = campo
            match opcao :
                
                # ALTERAR CATEGORIA
                case 1 :
                    nova_categoria = categoria(novo_valor)
                    if validar_categoria(nova_categoria) :
                        
                        if registrar_alteracao(medicamento, "categoria") :
                            medicamento["categoria"] = nova_categoria # altera a categoria do medicamento
                            return True
                        
                    return False
                
                # ALTERAR ESTOQUE
                case 2 :
                    nova_quantidade = ler_int(novo_valor)
                    if not validar_estoque(nova_quantidade): # valida o valor digitado
                        return False
                    
                    if not registrar_alteracao(medicamento, "estoque") :
                        return False
                    
                    medicamento["estoque"] = nova_quantidade
                    
                    # Função para verificar se há reposição e atualizar ela ou não
                    atualizar_repo(medicamento)
                    
                    return True
                
                # ALTERAR PREÇO
                case 3 :
                    novo_preco = ler_float(novo_valor)
                    if not validar_preco(novo_preco):
                        return False

                    if not registrar_alteracao(medicamento, "preco"):
                        return False

                    medicamento["preco"] = novo_preco
                    return True
                
                # OPÇÃO INVÁLIDA
                case _:
                    return False
                
    return False


# FUNÇÃO PARA REMOVER UM MEDICAMENTO
def remover_medicamento(nome):
    medicamento = buscar_medicamento(nome)
    nome = nome.strip().lower() # trata o nome para as comparações
    
    if medicamento is None :
        return False
    
    
    # Registra e remove o medicamento
    if not registrar_remocao(nome) :
        return False
    
    # busca se há solicitações de reposições para o medicamento
    if buscar_repo(medicamento) is not None :
        cancelar_repo(medicamento)  # limpa o pedido de reposição pendente
        
    return True

# FUNÇÃO PARA ORDENAR POR PREÇO
## Alterar para uma ordenação própria/personalizada
def ordenar_por_preco(lista):
    """
    Ordena uma lista de dicionários pelo campo "preco" (do menor para o maior)
    usando Bubble Sort. Retorna uma nova lista, sem alterar a original.
    """
    v = lista.copy()  # cópia da lista: evita modificar a lista original

    # Cada passada do loop externo "empurra" o maior elemento restante para o final
    for i in range(len(v)):
        trocou = False  # flag para detectar se houve alguma troca nesta passada

        # Bubble Sort: compara pares de elementos vizinhos
        # O "- i" ignora os últimos i elementos, que já estão na posição correta
        # O "- 1" evita estourar o índice ao acessar v[j+1]
        for j in range(len(v) - i - 1):
            # Se o preço atual for maior que o do próximo, estão fora de ordem
            if v[j]["preco"] > v[j + 1]["preco"]:
                v[j], v[j + 1] = v[j + 1], v[j]  # troca os dois de posição
                trocou = True  # registra que houve troca

        # Se nenhuma troca ocorreu, a lista já está ordenada: encerra antecipadamente
        if not trocou:
            break

    return v  # retorna a lista ordenada
