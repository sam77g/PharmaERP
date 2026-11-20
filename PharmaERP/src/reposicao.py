# ARQUIVO EXCLUSIVO PARA AS REPOSIÇÕES reposicao.py 
# =========== IMPORTS ===========
from .validar import validar_estoque
from collections import deque
from .estoque import gerar_id, gerar_id_repo
from .estruturas import solicitacoes_reposicao, limpar_tela, medicamentos 
from .registros import registrar_reposicao
import time


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