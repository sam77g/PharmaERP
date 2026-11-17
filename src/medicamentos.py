# Este arquivo será responsável pelo CRUD - LISTA
# Aqui ficará as funções de adicionar, ler, deletar e atualizar os medicamentos
# ex. de funções : 
# cadastrar_medicamento()
# listar_medicamentos()
# buscar_medicamento()
# alterar_medicamento()
# remover_medicamento()
# Também terá algumas validações
from validar import (validar_medicamento, validar_estoque, ler_int, ler_float, validar_nome, validar_preco, validar_categoria)
from collections import deque 
from estruturas import medicamentos
from registros import entrada, retirada, registrar_remocao, registrar_alteracao
from reposicao import cadastrar_repo, buscar_repo, cancelar_repo
from estoque import gerar_id
import time
import os
import pyfiglet
from colorama import Fore, Style, init

# Inicializa o colorama (necessário para compatibilidade com Windows)
init(autoreset=True)

# FUNÇÃO PARA LIMPAR TELA
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# FUNÇÃO PARA CATEGORIAS
def categoria() :
    print("[1] - Ético ")
    print("[2] - Genérico")
    print("[3] - Similar \n")
    while True:
        op = ler_int("Digite a categoria [1, 2 ou 3] : ")
        if op == 1: return "Ético"
        if op == 2: return "Genérico"
        if op == 3: return "Similar"
        print("Opção inválida! Escolha 1, 2 ou 3.")

# MENU DE MEDICAMENTOS
def menu_med() :
    while True:
        limpar_tela()
        print(Fore.YELLOW  + "========================================= ")
        print(Fore.GREEN  +"          MENU DE MEDICAMENTOS            ")
        print(Fore.YELLOW  + "========================================= \n")
        print(" [1] - Adicionar medicamento \n",
            "[2] - Alterar medicamento \n",
            "[3] - Remover medicamento \n",
            "[4] - Listar medicamentos \n",
            "[5] - Buscar medicamento \n",
            "[6] - Listar por categoria \n",
            "[7] - Listar / ordenar por preço \n"
            " [0] - Voltar \n")
        
        # VERIFICA O VALOR DIGITADO
        op_med = ler_int(Fore.LIGHTGREEN_EX + "Digite sua ação :  ") # verifica se realmente é int

        
        print("----------------------------------------")
        
        # MATCH CASE PARA O MENU
        match op_med :
            # adicionar medicamento
            case 1 :
                nome = input("Digite o nome do medicamento: ").strip().lower()
                while validar_nome(nome, medicamentos) == False :
                    print(Fore.RED + "Digite um nome válido ! \n")
                    nome = input("Digite o nome do medicamento: ").strip().lower()
                    
                estoque = ler_int("Digite o estoque : ")
                
                
                # dicionário do medicamento
                medicamento = {
                    "medicamento": nome,
                    "categoria": categoria(),
                    "estoque": estoque,
                    "preco": ler_float("Digite o preço: "), # valida e adiciona o preço
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
                        
                        print("\nEstoque menor que o estoque mínimo!")
                        print(
                            f"Criando pedido de reposição para "
                            f"{medicamento['medicamento'].upper()}!\n"
                        )
                        cadastrar_repo(medicamento)
                    input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
                else:
                    print(Fore.RED + f"\n [ERROR] : {resultado}")
            
            # ALTERAÇÃO DE MEDICAMENTO
            case 2 :
                if len(medicamentos) == 1 :
                    nome = medicamentos[0]["medicamento"]
                    alterar_medicamento(nome)
                else :
                    alt = input("Digite o medicamento: ") # salva o nome do medicamento
                    alterar_medicamento(alt) # redireciona para a função de alteração
                
                time.sleep(1)
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
            
            # REMOÇÃO DE MEDICAMENTO
            case 3 :
                if len(medicamentos) == 1 :
                    nome = medicamentos[0]["medicamento"]
                    remover_medicamento(nome) # redireciona para a função de remoção
                else :
                    rem = input("Digite o medicamento a ser removido: ") # salva o nome do medicamento
                    remover_medicamento(rem) # redireciona para a função de remoção
                    time.sleep(1)
                    
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
                
            # LISTA TODOS OS MEDICAMENTOS CADASTRADOS
            case 4 :
                listar_medicamentos() # chamada da função de listagem
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")            
            # BUSCA DE MEDICAMENTO
            case 5 :
                if len(medicamentos) == 1 :
                    nome = medicamentos[0]["medicamento"]
                    buscar_medicamento(nome) # chamada da função de busca
                else :
                    busca = input("Digite o medicamento: ") # salva o nome do medicamento
                    buscar_medicamento(busca) # chamada da função de busca
                    
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
            
            # LISTAGEM/BUSCA FILTRADA
            case 6 :
                opc_busca_categoria = categoria() # recebe o valor para filtragem
                buscar_medicamento_cat(opc_busca_categoria) # lista pela categoria
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")

            # LISTAGEM ORDENADA POR PREÇO
            case 7 :
                for i in ordenar_por_preco(medicamentos): # percorre e ordena os medicamentos
                    # printa no terminal
                    print(f"{i['medicamento'].upper()} - R$ {i['preco']} (estoque: {i['estoque']})")
                    
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
                
            # SAÍDA
            case 0 :
                print(Fore.LIGHTYELLOW_EX +" -- SAINDO DE MEDICAMENTOS --")
                time.sleep(0.5)
                limpar_tela()
                break
            
            # VALOR INVÁLIDO 
            case _ :
                print(Fore.RED + " \n [ERROR] VALOR INVÁLIDO !")
                
                    

# FUNÇAO DE CADASTRO DE MEDICAMENTOS
def cadastrar_medicamento(med) :
    medicamentos.append(med) # adiciona o medicamento a lista
    entrada(med) # REGISTRA A ENTRADA
    print(Fore.GREEN + " \n [SUCESS] : Medicamento cadastrado com sucesso ")


# FUNÇAO DE LISTAR TODOS OS MEDICAMENTOS
def listar_medicamentos() :
    
    if len(medicamentos) == 0 : 
        print(Fore.RED +" NENHUM MEDICAMENTO CADASTRADO ! ")
    else :
        for i in medicamentos :
            print(Fore.GREEN + f"==================== {i["medicamento"].upper()} ======================= \n")
            print(f"quantidade : {i['estoque']} " )  
            print(f"preço : {i["preco"]} ")
            print(f"categoria : {i['categoria']} \n")
        


# FUNÇÃO DE BUSCAR MEDICAMENTOS POR CATEGORIA
""" 
Complexidade 
- O(n) no pior caso
- O(1) no melhor caso
"""
def buscar_medicamento_cat(categoria_nome):
    # filtra todos os medicamentos da mesma categoria
    # Equivale a :
    # encontrados = []
    # for m in medicamentos:
    #     if m["categoria"].strip().lower() == categoria_nome.strip().lower():
    #         encontrados.append(m)
    encontrados = [
        # percorre a lista de medicamentos 
        m for m in medicamentos 
        # e guarda os correspondedes em uma lista nova
        if m["categoria"].strip().lower() == categoria_nome.strip().lower()
    ]

    # Se não houver nenhum medicamento com a categoria correspondente
    if not encontrados:
        print(Fore.RED + f"Nenhum medicamento cadastrado na categoria {categoria_nome}.")
        return []
    
    # Printa os medicamentos com a categoria desejada
    print(Fore.LIGHTGREEN_EX + f"=========== CATEGORIA: {categoria_nome.upper()} ({len(encontrados)}) ===========\n")
    for i in encontrados: # percorre os encontrados
        print(Fore.GREEN + f"==================== {i['medicamento'].upper()} ======================= \n")
        print(f"quantidade : {i['estoque']} ")
        print(f"preço : {i['preco']} ")
        print(f"ID : {i['id']} \n")

    return encontrados

# FUNÇÃO DE BUSCAR MEDICAMENTOS PELO NOME
# Complexidade :
# O(1) no melhor caso 
# O(n) no pior caso
def buscar_medicamento(nome):
    
    nome = nome.strip().lower
    
    if len(medicamentos) == 0 :
        print(Fore.RED + " LISTA VAZIA, IMPOSSÍVEL BUSCAR ! \n")
    elif nome == '' :
        print(Fore.RED + " NOME VAZIO ! ")
    else : 
        for i in medicamentos :
            if i["medicamento"].strip().lower == nome: # compara os nomes 
                print(Fore.GREEN + f"==================== {i['medicamento'].upper()} ======================= \n")
                print(f"quantidade : {i['estoque']} " )  
                print(f"preço : {i['preco']} ")
                print(f"ID : {i['id']} \n")
                return i
        return print(Fore.RED + "MEDICAMENTO NÃO ENCONTRADO ! ")

    
# função de alterar características do medicamento através do nome digitado
def alterar_medicamento(nome) :
    nome = nome.strip().lower() # normalizando o nome
        
    for medicamento in medicamentos: # percorre a lista de medicamentos
        if medicamento["medicamento"].strip().lower() == nome: # verifica se o nome digitado está presente na lista
            print(f" ----- ALTERAR {nome.upper()} ----- ")
            print(" [1] - Categoria \n",
                "[2] - Estoque / Quantidade \n",
                "[3] - Preço ")
            opcao = ler_int("O que você deseja alterar ? ")
            match opcao :
                case 1 :
                    print("-- Escolha a nova categoria --")
                    nova_categoria = categoria()
                    if validar_categoria(nova_categoria) :
                        registrar_alteracao(medicamento, "categoria")
                        medicamento["categoria"] = nova_categoria # altera a categoria do medicamento
                        time.sleep(0.5)
                        return print(Fore.GREEN + " [SUCESS] Categoria alterada com sucesso") # printa para o usuário 
                    return print(Fore.RED + "[ERROR] ao alterar a categoria ! ")
                
                case 2 :
                    nova_quantidade = ler_int("Digite a nova quantidade : ")
                    if not validar_estoque(nova_quantidade): # valida o valor digitado
                        return print(Fore.RED + "[ERROR] Quantidade inválida!")
                    else :
                        registrar_alteracao(medicamento, "estoque")
                        medicamento["estoque"] = nova_quantidade
                    
                    # caso esteja abaixo da quantidade mínima
                    if nova_quantidade < 15 :
                        print(Fore.RED +"---- Quantidade abaixo do estoque mínimo ! ---")
                        if buscar_repo(medicamento) is None : # caso já exista um pedido de reposição 
                            cadastrar_repo(medicamento) # cria um novo pedido de reposição
                            time.sleep(0.5) # espera 0.5 segundos
                    elif buscar_repo(medicamento) is not None: # caso a quantidade for maior e ele estiver para repor
                        cancelar_repo(medicamento) # retira do pedidos de reposição
                        time.sleep(0.5)
                    
                    return print(Fore.GREEN +"[SUCESS] Quantidade alterada com sucesso") # printa para o usuário 
                
                case 3 :
                    
                    novo_preco = ler_float(" Digite o novo preço : ")
                    if validar_preco(novo_preco) :
                        registrar_alteracao(medicamento, "preco")
                        medicamento["preco"] = novo_preco # altera o preço do medicamento
                    else :
                        return print(Fore.RED +"\n [ERROR] PREÇO INVÁLIDO !  ")
                    time.sleep(0.3)
                    
                    return print(Fore.GREEN +"\n [SUCESS] PREÇO ALTERADO COM SUCESSO ! ") # printa para o usuário 0
                case _:
                    return print(Fore.RED + "[ERROR] Opção inválida!")
                
    return print(Fore.RED + " [ERROR] MEDICAMENTO NÃO ENCONTRADO !")

# FUNÇÃO PARA REMOVER UM MEDICAMENTO PELO NOME
def remover_medicamento(nome):
    nome = nome.strip().lower() # trata o nome para as comparações
    # percorre e encontra o medicamento com o nome
    for medicamento in medicamentos:
        if medicamento["medicamento"].strip().lower() == nome:
                
            if registrar_remocao(medicamento) : # remove o medicamento 
                
                if buscar_repo(medicamento) is not None:
                    cancelar_repo(medicamento)  # limpa o pedido de reposição pendente
                    
                return print(Fore.GREEN +f"[SUCESS] {nome.upper()} REMOVIDO !")  
        
            return  # achou e removeu: sai da função
        
    return print(Fore.RED +" [ERROR] Medicamento não encontrado !")  # só chega aqui se o for terminar sem achar

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
