# consultas e relatórios
# Esse arquivo será responsável pelas funcionalidades que analisam os dados.
from collections import deque 
from datetime import datetime
from reposicao import cancelar_repo, cadastrar_repo, buscar_repo
from estruturas import historico,limpar_tela, medicamentos
import time
import pyfiglet
from colorama import Fore, Style, init

# Inicializa o colorama (necessário para compatibilidade com Windows)
init(autoreset=True)

def DataDeModificacao() :
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M") # SALVA O DIA E HORA DE ENTRADA
    return data_formatada

# MENU
def menu_hist() :
    while True:
        limpar_tela()
        print(Fore.YELLOW  +"========================================= ")
        print(Fore.GREEN  +"             MENU DE HISTÓRICO            ")
        print(Fore.YELLOW  +"========================================= ")
        print(
                " [1] - Listar Histórico \n",
                "[2] - Desfazer / Voltar histórico \n"
                " [0] - Voltar \n"
            )
        try :
            opcao = int(input(Fore.LIGHTGREEN_EX + f"Digite a opçao desejada : "))
        except ValueError :
            print("Digite apenas números!")
            time.sleep(1)
            continue
        
        match opcao :
            case 1 :
                listar_historico()
                time.sleep(1)
                input("\nPressione ENTER para continuar...")
                
            case 2 :
                desfazer_ultima()
                time.sleep(1)
                input("\nPressione ENTER para continuar...")
                
            case 0 :
                print("Voltando para o menu principal ...")
                time.sleep(0.5)
                limpar_tela()
                return

# FUNÇÃO DE REGISTRO DE ENTRADA NO ESTOQUE
def entrada(med) :
    data_formatada = DataDeModificacao()
    
    entry_med = {
        "medicamento" : med["medicamento"],
        "id_medicamento" : med["id"],
        "categoria" : med["categoria"],
        "dados": med.copy(),
        "data" : data_formatada, # saída: dd/mm/2026 hr:min
        "tipo" : "ENTRADA"
    }
    
    historico.append(entry_med) # ENTRADA NO TOPO DA PILHA
    return print(f" \n O {med["medicamento"]} foi adicionado ao sistema !")

# FUNÇAO DE REGISTRO DE SAÍDA NO ESTOQUE
def retirada(med):
    
    data_formatada = DataDeModificacao()
    out_med = {
        "medicamento": med["medicamento"],
        "id_medicamento": med["id"],
        "categoria": med["categoria"],
        "dados": med.copy(),
        "tipo": "SAÍDA",
        "data": data_formatada
    }
    historico.append(out_med)  # registra a saída (antes era historico.pop())
    return print(f"O {med['medicamento'].upper()} foi retirado ")

# FUNÇÃO PARA LISTAR O HISTÓRICO
def listar_historico() :
    limpar_tela() # limpa a tela do terminal
    for i in reversed(historico) : 
        print(f"==================== {i['medicamento'].upper()} ({i['tipo']}) =======================\n")
        print(f"ID : {i['id_medicamento']} \n")
        print(f"Data : {i['data']} \n")
        print(f"Categoria : {i['dados']['categoria']}")
        if i['tipo'] == "ALTERAÇÃO" :
            print(f"Campo alterado : {i['campo_alterado']} \n")
            print(f"Valor anterior : {i['dados'][i['campo_alterado']]} \n")
        
# FUNÇÃO PARA DESFAZER A ULTIMA AÇÃO NO HISTÓRICO
def desfazer_ultima():
    if not historico:
        print("Nada para desfazer.")
        return
    mov = historico.pop()
    
    match mov["tipo"] :
        case "ENTRADA" :
            medicamentos[:] = [m for m in medicamentos if m["id"] != mov["id_medicamento"]]
            cancelar_repo(mov["dados"])
        case "SAÍDA" :
            med = mov["dados"]
            medicamentos.append(med)
            if med["estoque"] < 15:
                cadastrar_repo(med)
        case "REMOÇÃO" :
            med = mov["dados"]
            medicamentos.append(med)
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
        
    print(f"Desfeito: {mov['tipo']} de {mov['medicamento']}")

# FUNÇÃO PARA REGISTRAR A REMOÇÃO/EXCLUÇÃO DE UM MEDICAMENTO 
def registrar_remocao(med) :
    data_de_remocao = DataDeModificacao()
    
    if not isinstance(med, dict):
        print(Fore.RED+"[ERROR] Os dados do medicamento devem estar em um dicionário.")
        return False
    
    if med in medicamentos :
        remove_med = {
            "medicamento" : med["medicamento"],
            "id_medicamento" : med["id"],
            "categoria" : med["categoria"],
            "dados": med.copy(),
            "data" : data_de_remocao, # saída: dd/mm/2026 hr:min
            "tipo" : "REMOÇÃO"
        }
        historico.append(remove_med) # registra a remoção no histórico
        medicamentos.remove(med)
        return True
    
    else :
        print(Fore.RED + "[ERRO] Medicamento não encontrado para remoção ! ")
        return False

# FUNÇÃO PARA SALVAR NO "CACHE" A ALTERAÇÃO 
def registrar_alteracao(med, tipo) :
    
    if not isinstance(med, dict):
        print(Fore.RED+"[ERROR] Os dados do medicamento devem estar em um dicionário.")
        return False
    
    if med in medicamentos :
        update_med = {
            "medicamento" : med["medicamento"],
            "id_medicamento" : med["id"],
            "campo_alterado": tipo,
            "dados": med.copy(),
            "data" : DataDeModificacao(), # saída: dd/mm/2026 hr:min
            "tipo" : "ALTERAÇÃO"
        }

        historico.append(update_med) # registra a alteração no histórico
        return True