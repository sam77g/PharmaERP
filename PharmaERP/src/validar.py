# ARQUIVO COM FUNÇÕES DE VALIDAÇÃO

import math # importando a biblioteca math

# LER FLOATS
def ler_float(msg):
    
    while True:
        try:
            # Lê o valor, substitui vírgula por ponto e converte para float
            entrada = input(msg).replace(",", ".")
            valor = float(entrada)
            
            # Verifica se o número é finito (rejeita inf, -inf e nan)
            if not math.isfinite(valor):
                return False
            else :
                return valor
            
        except ValueError:
            return False


# LER INTEIROS
def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            return False

# VALIDA O TEXTO DIGITADO
def validar_texto(valor):
    
    if not isinstance(valor, str):
        return False

    if not valor.strip():
        return False

    return True


# VALIDA O PREÇO
def validar_preco(valor):
    # verifica se o preço é int, float ou booleano 
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        return False
    
    if valor < 0:
        return False
    
    if not math.isfinite(valor):
        return False
    
    return True


# VALIDA O ESTOQUE
def validar_estoque(valor):
    # verifica o tipo do valor 
    if not isinstance(valor, int) or isinstance(valor, bool):
        return False
    if valor < 0:
        return False

    return True


# VALIDA SE O ID ESTÁ DISPONÍVEL
def validar_id(med_id, lista_medicamentos, ignorar_id=None):

    if not isinstance(med_id, int) or isinstance(med_id, bool) :
        return False

    if med_id <= 0:
        return False

    for medicamento in lista_medicamentos:
        
        if medicamento["id"] == ignorar_id:
            continue
        
        if medicamento["id"] == med_id:
            return False

    return True


# VALIDA SE O NOME ESTÁ DISPONÍVEL
def validar_nome(med_nome, lista_medicamentos, ignorar_id=None):
    if not validar_texto(med_nome):
        return False
    for medicamento in lista_medicamentos:
        # Ignora o próprio medicamento durante uma alteração
        if medicamento["id"] == ignorar_id:
            continue
        if medicamento["medicamento"].strip().lower() == med_nome.strip().lower():
            return False
    return True


# VALIDA O DICIONÁRIO DE MEDICAMENTO
def validar_medicamento(medicamento, lista_medicamentos, ignorar_id=None) : 
    # Verifica se é um dicionário
    if not isinstance(medicamento, dict):
        return False
    
    # Verifica os campos obrigatórios
    campos_obrigatorios = [
        "medicamento",
        "categoria",
        "estoque",
        "preco",
        "id"
    ]

    # PERCORRE O ARRAY PARA VERIFICAR SE HÁ ALGUM CAMPO VAZIO
    for campo in campos_obrigatorios: 
        if campo not in medicamento :
            return False
        
    # Valida o nome
    if not validar_texto(medicamento["medicamento"]):
        return False
    if not validar_nome(medicamento["medicamento"], lista_medicamentos, ignorar_id) :
        return False
    # Valida a categoria
    if not validar_categoria(medicamento["categoria"]) :
        return False
    # Valida o estoque
    if not validar_estoque(medicamento["estoque"]):
        return False
    # Valida o preço
    if not validar_preco(medicamento["preco"]):
        return False
    if not validar_id(medicamento["id"], lista_medicamentos, ignorar_id ) :
        return False
    return True

# FUNÇÃO PARA VALIDAR A CATEGORIA
def validar_categoria(categoria):
    categorias_validas = [
        "ÉTICO",
        "GENÉRICO",
        "SIMILAR"
    ]

    if not validar_texto(categoria):
        return False
    
    categoria_limpa = categoria.strip()
    
    if categoria_limpa.upper() not in categorias_validas :
        return False
    
    return True

