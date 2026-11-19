# REGISTROS SALVOS NO HISTÓRICO registros.py
"""
Esse arquivo será responsável por registrar as mudanças nos medicamentos 
"""
from datetime import datetime
from estruturas import historico,limpar_tela, medicamentos
import time
import pyfiglet
from colorama import Fore, Style, init

def DataDeModificacao() :
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M") # SALVA O DIA E HORA DE ENTRADA
    return data_formatada


# FUNÇÃO PARA SALVAR NO "CACHE" A ALTERAÇÃO 
def registrar_reposicao(med, quantidade_recebida):
    if not isinstance(med, dict):
        print(Fore.RED + "[ERROR] Os dados do medicamento devem estar em um dicionário.")
        return False

    if med not in medicamentos:
        return False

    update_repo = {
        "medicamento": med["medicamento"],
        "id_medicamento": med["id"],
        "dados": med.copy(),
        "data": DataDeModificacao(),
        "quantidade_recebida": quantidade_recebida,
        "tipo": "REPOSIÇÃO"
    }

    historico.append(update_repo)
    return True
    

# FUNÇÃO PARA REGISTRAR A REMOÇÃO/EXCLUÇÃO DE UM MEDICAMENTO 
def registrar_remocao(med) :
    
    if not isinstance(med, dict):
        print(Fore.RED+"[ERROR] Os dados do medicamento devem estar em um dicionário.")
        return False
    
    data_de_remocao = DataDeModificacao()
    
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
    return print(Fore.GREEN +f"O {med['medicamento'].upper()} foi retirado ")