
# Esse arquivo será responsável pelas funcionalidades que analisam os dados. relatorios.py 
# consultas e relatórios
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
            opcao = int(input(Fore.LIGHTGREEN_EX + f"Digite a opçao desejada : " + Fore.BLUE))
        except ValueError :
            print("Digite apenas números!")
            time.sleep(1)
            continue
        
        match opcao :
            case 1 :
                listar_historico()
                time.sleep(1)
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
                
            case 2 :
                desfazer_ultima()
                time.sleep(1)
                input(Fore.LIGHTGREEN_EX +"\nPressione ENTER para continuar...")
                
            case 0 :
                print(Fore.LIGHTGREEN_EX +"Voltando para o menu principal ...")
                time.sleep(0.5)
                limpar_tela()
                return

# FUNÇÃO PARA LISTAR O HISTÓRICO
def listar_historico():
    limpar_tela()

    for i in reversed(historico):
        print(Fore.GREEN + f"==================== {i['medicamento'].upper()} ({i['tipo']}) =======================\n")

        print(f"ID : {i['id_medicamento']}")
        print(f"Data : {i['data']}")

        match i["tipo"]:
            case "ALTERAÇÃO":
                campo = i["campo_alterado"]

                print(f"Campo alterado : {campo}")
                print(f"Valor anterior : {i['dados'][campo]}")

            case "ENTRADA" | "SAÍDA" | "REMOÇÃO":
                print(f"Categoria : {i['dados']['categoria']}")
                print(f"Estoque : {i['dados']['estoque']}")
                print(f"Preço : R$ {i['dados']['preco']:.2f}")
            
            case "REPOSIÇÃO":
                estoque_anterior = i["dados"]["estoque"]
                quantidade = i["quantidade_recebida"]

                print(f"Estoque anterior : {estoque_anterior}")
                print(f"Quantidade recebida : {quantidade}")
                print(f"Estoque posterior : {estoque_anterior + quantidade}")

        print("\n")
        
# FUNÇÃO PARA DESFAZER A ULTIMA AÇÃO NO HISTÓRICO
def desfazer_ultima():
    if not historico:
        print(Fore.LIGHTRED_EX +"Nada para desfazer.")
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

            # Reconstrói a solicitação de reposição, se necessário
            if med["estoque"] < 15:
                if buscar_repo(med) is None:
                    cadastrar_repo(med)
            else:
                if buscar_repo(med) is not None:
                    cancelar_repo(med)
        
    print(f"Desfeito: {mov['tipo']} de {mov['medicamento']}")

