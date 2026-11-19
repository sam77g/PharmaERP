# Arquivo principal que orquestrará o sistema
# Ele será responsável por:
#     mostrar o menu principal;
#     receber as escolhas do usuário;
#     chamar as funções dos outros arquivos;
#     controlar o fluxo geral do programa.

# IMPORTS
from src.medicamentos import (
    cadastrar_medicamento,
    listar_medicamentos,
    buscar_medicamento,
    alterar_medicamento,
    remover_medicamento
)

from src.reposicao import cadastrar_repo
from interface.interface import iniciar_interface
import time

if __name__ == "__main__":
    iniciar_interface()

# =========== SISTEMA PRINCIPAL ===========

while True:
    # MENU DO SISTEMA
    print( "========== SISTEMA DE CONTROLE PharmaERP ============ \n")
    print(
        "  [1] - Menu Medicamentos\n",
        " [2] - Reposição \n",
        " [3] - Histórico \n",
        " [0] - Sair \n"
    )
    print( "=================================================== \n")
    opcao = ler_int("[OPÇÃO] :  ")
    # MATCH CASE PARA A OPÇÃO DIGITADA
    match opcao:
        # MENU DE MEDICAMENTOS
        case 1:
            menu_med()

        # MENU DE REPOSIÇÃO
        case 2 :
            menu_repo()

        # MENU HISTÓRICO
        case 3 :
            menu_hist()

        # SAIR
        case 0:
            print("Até mais!")
            break

        # OPÇÃO INVÁLIDA
        case _:
            print("Opção inválida! Tente novamente.")
