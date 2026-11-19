# Arquivo principal que orquestrará o sistema
# Ele será responsável por:
#     mostrar o menu principal;
#     receber as escolhas do usuário;
#     chamar as funções dos outros arquivos;
#     controlar o fluxo geral do programa.

import pyfiglet
from colorama import Fore, Style, init
from interface import iniciar_janela



# Inicializa o colorama (necessário para compatibilidade com Windows)
init(autoreset=True)

# Gera a arte do texto
texto_art = pyfiglet.figlet_format("PharmaERP", font="rozzo")

# Imprime o título em verde brilhante
print(Fore.GREEN + Style.BRIGHT + texto_art)

# Subtítulo e descrições
print(Fore.YELLOW + "Sistema de controle farmaceutico")
print(
Fore.GREEN
    + "Samuel , Samoel , Marcos & Gabriel "
    + Fore.WHITE
    + " | "
    + Fore.MAGENTA
    + " TDE Estrutura de Dados \n"
)

# IMPORTS
import time
from relatorios import menu_hist
from medicamentos import menu_med
from reposicao import  menu_repo
from validar import ler_int
from interface import iniciar_janela

if __name__ == "__main__":
# Abre a tela gráfica primeiro e aguarda o clique em "Entrar no Sistema"
    iniciar_janela()
