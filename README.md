<div align="center">

# PharmaERP — Interface Gráfica (GUI)

**Sistema de gerenciamento de medicamentos e solicitações de reposição para uma farmácia, com interface gráfica em Tkinter, desenvolvido em Python como projeto acadêmico de Estruturas de Dados.**

![Versão](https://img.shields.io/badge/vers%C3%A3o-1.4.0-2ecc71)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Interface](https://img.shields.io/badge/interface-Tkinter-orange)
![Estruturas](https://img.shields.io/badge/estruturas-Lista%20%7C%20Pilha%20%7C%20Fila-blue)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

**Versão de terminal (TUI):** [branch `PharmaERP-CLI`](https://github.com/sam77g/PharmaERP/tree/PharmaERP-CLI)

</div>

---

## Sumário

1. [Sobre o Projeto](#1-sobre-o-projeto)
2. [Objetivos](#2-objetivos)
3. [Funcionalidades](#3-funcionalidades)
4. [Interface Gráfica](#4-interface-gráfica)
5. [Estruturas de Dados](#5-estruturas-de-dados)
6. [Algoritmos](#6-algoritmos)
7. [Regras de Negócio](#7-regras-de-negócio)
8. [Arquitetura do Projeto](#8-arquitetura-do-projeto)
9. [Tecnologias e Dependências](#9-tecnologias-e-dependências)
10. [Pré-requisitos](#10-pré-requisitos)
11. [Como Executar](#11-como-executar)
12. [Fluxo do Sistema](#12-fluxo-do-sistema)
13. [Complexidade](#13-complexidade)
14. [Versionamento e Git](#14-versionamento-e-git)
15. [Status do Projeto](#15-status-do-projeto)
16. [Licença](#16-licença)

---

## 1. Sobre o Projeto

O **PharmaERP** é um sistema de gerenciamento de uma farmácia. Esta é a **versão 1.4.0 — Interface (GUI)**, que roda em uma janela gráfica construída com **Tkinter**.

O projeto foi desenvolvido como atividade acadêmica da disciplina de **Algoritmos e Estruturas de Dados**, com foco na aplicação prática de **estruturas de dados lineares**, algoritmos de busca, ordenação e manipulação de registros.

O sistema permite cadastrar e administrar medicamentos, acompanhar o estoque, gerenciar solicitações de reposição e consultar/desfazer as movimentações registradas.

O projeto demonstra, de forma prática, a utilização de:

- **Lista** para armazenamento e gerenciamento dos medicamentos;
- **Pilha** para controle do histórico e operação de desfazer;
- **Fila com prioridade** para gerenciamento das solicitações de reposição;
- **Criticidade** para atender primeiro as situações mais urgentes.

> **Observação:** os dados são mantidos somente em memória. Ao fechar a janela, todos os registros são perdidos.

### GUI × TUI

O PharmaERP possui duas versões, com a mesma lógica de negócio e apresentações diferentes:

| | **GUI (esta versão)** | **TUI** |
|---|---|---|
| Onde está | branch `main` | [branch `PharmaERP-CLI`](https://github.com/sam77g/PharmaERP/tree/PharmaERP-CLI) |
| Apresentação | Janela Tkinter (botões, formulários, tabelas) | Menus no terminal |
| Dependências externas | Nenhuma (Tkinter faz parte do Python) | `pyfiglet`, `colorama` |
| Ponto de entrada | `PharmaERP/__main__.py` | `main.py` |

---

## 2. Objetivos

- Aplicar estruturas de dados lineares em um sistema funcional;
- Implementar inserção, busca, alteração e remoção;
- Utilizar busca linear;
- Implementar manualmente um algoritmo de ordenação (Bubble Sort);
- Trabalhar com comportamento **LIFO** através de uma pilha;
- Trabalhar com **FIFO combinado com prioridade** nas solicitações de reposição;
- Praticar modularização em Python, separando **lógica** e **interface**;
- Implementar validação e tratamento de entradas;
- Construir uma interface gráfica com Tkinter, navegando entre telas;
- Demonstrar conceitos de complexidade de algoritmos.

---

## 3. Funcionalidades

### 3.1. Gerenciamento de medicamentos

O sistema permite:

- **Cadastrar** medicamentos (nome, categoria, estoque e preço);
- **Alterar** categoria, estoque ou preço de um medicamento;
- **Remover** medicamentos (com confirmação);
- **Listar** todos os medicamentos;
- **Buscar** por nome ou por categoria;
- **Ordenar** a listagem por preço (menor → maior);
- Validar os dados antes de salvar;
- Impedir nomes duplicados (sem diferenciar maiúsculas/minúsculas).

Cada medicamento é um dicionário com os campos:

```text
id
medicamento
categoria
estoque
preco
```

Categorias disponíveis:

- **ÉTICO**
- **GENÉRICO**
- **SIMILAR**

Detalhes de entrada: o preço aceita vírgula ou ponto como separador decimal; o estoque deve ser inteiro maior ou igual a 0; o preço deve ser maior ou igual a 0.

---

### 3.2. Gerenciamento de reposições

Quando o estoque de um medicamento fica **abaixo de 15 unidades**, o sistema cria automaticamente uma solicitação de reposição.

Uma solicitação possui:

```text
id_repo
medicamento
id_medicamento
criticidade
quantidade_solicitada
```

O sistema permite:

- **Listar** as solicitações pendentes, já na ordem de atendimento;
- **Atender** a primeira solicitação da fila;
- **Alterar** a quantidade solicitada de uma solicitação;
- **Cancelar** uma solicitação;
- Evitar solicitações duplicadas para o mesmo medicamento.

---

### 3.3. Criticidade e prioridade

As solicitações recebem uma classificação automática de acordo com o estoque disponível no momento em que são criadas.

| Estoque | Criticidade | Prioridade |
|---:|:---|---:|
| Menor que 5 | **CRÍTICO** | 1ª |
| 5 a 9 | **ALERTA** | 2ª |
| 10 a 14 | **AVISO** | 3ª |
| 15 ou mais | Sem reposição | — |

A fila é mantida ordenada por criticidade:

```text
CRÍTICO
   ↓
ALERTA
   ↓
AVISO
```

Em caso de empate de criticidade, vale a ordem de chegada:

```text
Primeiro a chegar
       ↓
Primeiro a ser atendido
```

---

### 3.4. Histórico e desfazer

Toda operação relevante é registrada no histórico com data e hora (`dd/mm/aaaa hh:mm`):

| Tipo | Quando é registrado |
|---|---|
| `ENTRADA` | Cadastro de um novo medicamento |
| `ALTERAÇÃO` | Alteração de categoria, estoque ou preço (guarda o valor anterior) |
| `REMOÇÃO` | Remoção de um medicamento |
| `REPOSIÇÃO` | Atendimento de uma solicitação (guarda o estoque anterior e a quantidade recebida) |

O sistema permite:

- **Visualizar** o histórico, do registro mais recente para o mais antigo;
- **Desfazer** a última ação registrada.

A operação de desfazer utiliza o princípio **LIFO — Last In, First Out**:

```text
Movimentação A
Movimentação B
Movimentação C ← última movimentação

Desfazer → Movimentação C
```

O que cada tipo faz ao ser desfeito:

| Tipo desfeito | Efeito |
|---|---|
| `ENTRADA` | Remove o medicamento cadastrado e cancela sua reposição |
| `REMOÇÃO` | Devolve o medicamento à lista e reajusta a reposição conforme o estoque |
| `ALTERAÇÃO` | Restaura o valor anterior do campo (e reajusta a reposição se o campo era o estoque) |
| `REPOSIÇÃO` | Restaura o estoque anterior ao recebimento |

---

## 4. Interface Gráfica

A interface usa **uma única janela** (`tk.Tk`) e troca de tela escondendo e mostrando **Frames** (`pack_forget()` / `pack()`), em vez de abrir várias janelas. Todas as telas seguem a mesma paleta escura.

### 4.1. Navegação

```text
Tela de boas-vindas
        │  [Entrar no Sistema]
        ▼
   Menu Principal
        │
        ├── 1. Menu Medicamentos
        │       ├── 1. Cadastrar medicamento
        │       ├── 2. Listar medicamentos
        │       ├── 3. Buscar (nome / categoria)
        │       ├── 4. Alterar medicamento
        │       ├── 5. Remover medicamento
        │       ├── 6. Ordenar por preço
        │       └── 0. Voltar
        │
        ├── 2. Reposição
        │       ├── 1. Listar solicitações de reposição
        │       ├── 2. Atender primeira reposição
        │       ├── 3. Alterar quantidade solicitada
        │       ├── 4. Cancelar solicitação
        │       └── 0. Voltar
        │
        ├── 3. Histórico
        │       ├── 1. Visualizar histórico
        │       ├── 2. Desfazer última ação
        │       └── 0. Voltar
        │
        └── 0. Sair
```

Cada submenu mostra um **contador** que se atualiza após as operações (medicamentos cadastrados, solicitações pendentes, registros no histórico).

### 4.2. Recursos de usabilidade

- **Tabelas** (`ttk.Treeview`) com rolagem para listagens;
- **Cores por significado** nas tabelas:
  - Medicamentos: vermelho para estoque abaixo de 15 unidades;
  - Reposição: vermelho = `CRÍTICO`, amarelo = `ALERTA`, azul = `AVISO`;
  - Histórico: uma cor para cada tipo (`ENTRADA`, `REPOSIÇÃO`, `ALTERAÇÃO`, `REMOÇÃO`);
- **Listas suspensas** (`Combobox`) para categoria e campo a alterar, evitando erro de digitação;
- **Caixas de diálogo** (`messagebox`) para erros, avisos, sucesso e confirmações (remover medicamento, cancelar solicitação, desfazer ação);
- **Tecla Enter** confirma a ação da tela atual;
- **Botão Voltar/Fechar/Cancelar** em todas as telas.

### 4.3. Paleta de cores

| Uso | Cor |
|---|---|
| Fundo | `#121820` |
| Cartões e botões | `#1f2937` |
| Destaque / sucesso | `#2ecc71` |
| Subtítulos e cabeçalhos de tabela | `#f1c40f` |
| Ações destrutivas / voltar | `#c0392b` |
| Texto | `#ffffff` / `#bdc3c7` |

---

## 5. Estruturas de Dados

As estruturas ficam em `src/estruturas.py` e são compartilhadas por todos os módulos.

### 5.1. Lista

A lista Python armazena os medicamentos:

```python
medicamentos = []
```

Ela permite inserção, remoção, busca, percurso, filtragem e ordenação, e representa o cadastro principal do sistema.

---

### 5.2. Pilha — LIFO

O histórico utiliza uma lista Python como pilha:

```python
historico = []
```

Novas movimentações entram com `append()` e a última é retirada com `pop()` ao desfazer.

---

### 5.3. Fila de reposição com prioridade

As solicitações utilizam `collections.deque`:

```python
from collections import deque

solicitacoes_reposicao = deque()
```

O atendimento sempre consome o elemento da frente (`popleft()`), e a inserção coloca a solicitação na posição correta de acordo com a criticidade, mantendo a ordem de chegada entre iguais.

---

## 6. Algoritmos

### 6.1. Busca Linear

Usada para localizar medicamentos por nome e solicitações de reposição pelo nome do medicamento. A comparação ignora maiúsculas/minúsculas e espaços nas pontas.

- Melhor caso: **O(1)**
- Pior caso: **O(n)**

---

### 6.2. Filtragem por Categoria

Percorre a lista de medicamentos e seleciona os que pertencem à categoria informada.

- **O(n)**

---

### 6.3. Bubble Sort

A ordenação por preço usa uma implementação manual do **Bubble Sort**, com parada antecipada: se uma passagem não realiza trocas, a lista já está ordenada. A função devolve uma **nova lista**, sem alterar a lista original.

- Melhor caso: **O(n)**
- Pior caso: **O(n²)**

---

### 6.4. Inserção por Prioridade

A prioridade é representada por:

```python
PRIORIDADE = {
    "CRÍTICO": 0,
    "ALERTA": 1,
    "AVISO": 2
}
```

A inserção percorre a fila até achar o primeiro elemento de prioridade **menos urgente** e insere a nova solicitação antes dele; se não houver, insere no fim. Assim, solicitações de mesma criticidade ficam em ordem de chegada (FIFO).

- Melhor caso: **O(1)** quando o primeiro elemento já é menos urgente ou a fila está vazia;
- Pior caso: **O(n)**.

---

## 7. Regras de Negócio

| Regra | Comportamento |
|---|---|
| Estoque mínimo | **15 unidades** |
| Estoque < 5 | **CRÍTICO** |
| Estoque de 5 a 9 | **ALERTA** |
| Estoque de 10 a 14 | **AVISO** |
| Estoque ≥ 15 | Não cria reposição |
| Quantidade solicitada padrão | `15 - estoque atual` |
| Reposição duplicada | Não permitida (uma solicitação por medicamento) |
| Empate de criticidade | Mantém ordem de chegada |
| Nome do medicamento | Único, sem diferenciar maiúsculas/minúsculas |
| Cadastro com estoque < 15 | Cria a reposição automaticamente |
| Estoque alterado para ≥ 15 | Cancela a reposição pendente |
| Estoque alterado para < 15 | Recria a solicitação com a nova criticidade e quantidade (e novo `id_repo`) |
| Medicamento removido | Cancela a reposição pendente |
| IDs | Independentes: um contador para medicamentos e outro para reposições |

### Atendimento de uma reposição

A tela de atendimento sempre trabalha com a **primeira solicitação da fila**:

1. Exibe o próximo da fila (medicamento, criticidade e quantidade sugerida);
2. O usuário informa a **quantidade realmente recebida** (inteiro maior que 0, pode diferir da sugerida);
3. O sistema localiza o medicamento pelo ID;
4. Registra a `REPOSIÇÃO` no histórico (antes de alterar o estoque);
5. Remove a solicitação atendida da fila;
6. Soma a quantidade ao estoque;
7. Se o estoque continuar abaixo de 15, cria uma nova solicitação.

---

## 8. Arquitetura do Projeto

A lógica de negócio e a interface ficam separadas **por seção dentro de cada módulo**: as funções de lógica recebem valores já digitados e retornam `True/False` ou `(ok, mensagem)`, sem `input()` nem janelas; as telas Tkinter chamam essas funções e exibem o resultado.

```text
.
├── README.md
├── .gitignore
└── PharmaERP
    ├── __main__.py
    ├── Dockerfile
    ├── .dockerignore
    ├── requirements.txt
    ├── docs
    │   ├── CONTRIBUTING.md
    │   └── LICENSE
    ├── interface
    │   ├── __init__.py
    │   └── interface.py
    └── src
        ├── __init__.py
        ├── estoque.py
        ├── estruturas.py
        ├── medicamentos.py
        ├── registros.py
        ├── relatorios.py
        ├── reposicao.py
        └── validar.py
```

### Responsabilidade dos módulos

| Arquivo | Responsabilidade |
|---|---|
| `__main__.py` | Ponto de entrada: abre a janela principal |
| `interface/interface.py` | Janela principal, tela de boas-vindas e menu principal |
| `src/estruturas.py` | Estruturas globais (`medicamentos`, `historico`, `solicitacoes_reposicao`) |
| `src/medicamentos.py` | CRUD, busca, ordenação **e** telas/menu de medicamentos |
| `src/reposicao.py` | Solicitações, criticidade, prioridade, atendimento **e** telas/menu de reposição |
| `src/relatorios.py` | Desfazer a última ação **e** telas/menu de histórico |
| `src/registros.py` | Criação dos registros do histórico (entrada, alteração, remoção, reposição) |
| `src/estoque.py` | Geradores de ID (medicamentos e reposições) |
| `src/validar.py` | Validação de nome, categoria, estoque, preço e do medicamento completo |

### Padrão de navegação

Cada menu recebe a janela principal e a tela anterior, esconde a anterior e cria o próprio Frame:

```python
menu_med(janela_principal, tela_anterior)
menu_repo(janela_principal, tela_anterior)
menu_hist(janela_principal, tela_anterior)
```

As sub-telas (cadastrar, listar, atender etc.) repetem o mesmo padrão a partir do menu que as chamou, e o botão de voltar destrói o Frame atual e reexibe o anterior.

---

## 9. Tecnologias e Dependências

### Linguagem

- **Python 3.12+**

### Biblioteca padrão utilizada

| Recurso | Finalidade |
|---|---|
| `tkinter` / `tkinter.ttk` | Interface gráfica (janelas, botões, tabelas, listas) |
| `tkinter.messagebox` | Diálogos de erro, aviso, sucesso e confirmação |
| `collections.deque` | Fila de solicitações de reposição |
| `datetime` | Data e hora das movimentações |
| `math` | Validação de números finitos |

### Bibliotecas externas

A versão GUI **não depende de bibliotecas externas**. O `requirements.txt` ainda lista `colorama` e `pyfiglet`, herdadas da versão de terminal, mas nenhuma delas é usada pela interface gráfica.

---

## 10. Pré-requisitos

- **Python 3.12 ou superior**;
- **Tkinter** instalado (já vem com o Python no Windows e no macOS; no Linux pode ser necessário instalar à parte);
- Um ambiente com interface gráfica (janelas);
- Git, caso queira clonar o projeto.

Verifique a versão do Python:

```bash
python --version
```

Caso seu sistema utilize `python3`:

```bash
python3 --version
```

Verifique se o Tkinter está disponível (deve abrir uma pequena janela):

```bash
python3 -m tkinter
```

Se aparecer `No module named 'tkinter'` no Linux (Debian/Ubuntu):

```bash
sudo apt install python3-tk
```

---

## 11. Como Executar

### 11.1. Clonar o repositório

```bash
git clone https://github.com/sam77g/PharmaERP.git
```

### 11.2. Acessar a pasta do programa

```bash
cd PharmaERP/PharmaERP
```

> O programa deve ser executado **de dentro desta pasta**, pois os imports (`interface`, `src`) são relativos a ela.

### 11.3. Executar

```bash
python __main__.py
```

Ou:

```bash
python3 __main__.py
```

Não é necessário instalar nenhuma dependência.

### 11.4. Executar com Docker (Linux com X11)

O `Dockerfile` instala o Tkinter e as bibliotecas gráficas, mas, por ser um programa com janela, o contêiner precisa enviar a tela para o servidor gráfico do computador:

```bash
cd PharmaERP/PharmaERP
docker build -t pharmaerp-gui .

xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pharmaerp-gui
```

> Em Windows e macOS é preciso um servidor X (por exemplo, VcXsrv ou XQuartz) configurado; para esses sistemas, rodar direto com Python (seção 11.3) é mais simples.

### 11.5. Exemplo de uso rápido

1. Clique em **Entrar no Sistema**;
2. Em **Menu Medicamentos → Cadastrar**, cadastre `Dipirona`, `GENÉRICO`, estoque `3`, preço `4,50` — uma reposição **CRÍTICO** é criada automaticamente;
3. Em **Reposição → Listar**, veja a solicitação na fila;
4. Em **Reposição → Atender**, informe a quantidade recebida;
5. Em **Histórico**, visualize as movimentações e use **Desfazer** para voltar atrás.

---

## 12. Fluxo do Sistema

O fluxo geral do PharmaERP:

```text
                    ┌──────────────────┐
                    │    PharmaERP     │
                    │  (janela Tkinter)│
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        Medicamentos     Reposição       Histórico
              │              │              │
              ▼              ▼              ▼
           Lista       Prioridade/FIFO     Pilha
              │              │              │
              ▼              ▼              ▼
       CRUD / Busca      Criticidade      Desfazer
       / Ordenação       / Atendimento
```

### Fluxo de reposição

```text
Cadastro/alteração do medicamento
              │
              ▼
        Estoque < 15?
         /        \
       não        sim
        │           │
        ▼           ▼
 Cancela pedido   Cria/recria pedido
 (se existir)         │
                      ▼
                Classificar por
                 criticidade
                      │
                      ▼
               Inserir na fila
                      │
                      ▼
          Listar / Alterar / Cancelar
                      │
                      ▼
                   Atender
                      │
                      ▼
            Estoque ainda < 15?
              /           \
            sim           não
             │             │
             ▼             ▼
      Novo pedido        Fim
```

### Fluxo do histórico

```text
Operação (cadastrar / alterar / remover / atender)
              │
              ▼
   Registro empilhado no histórico
              │
              ▼
     Desfazer → desempilha o topo
              │
              ▼
   Reverte o efeito na lista e na fila
```

---

## 13. Complexidade

Legenda: **n** = medicamentos cadastrados, **r** = solicitações na fila, **h** = registros no histórico.

| Operação | Estrutura / Algoritmo | Complexidade |
|---|---|---|
| Cadastrar medicamento | Verificação de nome duplicado + `append()` | O(n) |
| Buscar por nome | Busca linear | O(n) |
| Filtrar por categoria | Percurso sequencial | O(n) |
| Ordenar por preço | Bubble Sort | O(n²) |
| Listar medicamentos | Percurso para preencher a tabela | O(n) |
| Registro no histórico | Pilha `append()` | O(1) |
| Visualizar histórico | Percurso invertido | O(h) |
| Desfazer última ação | `pop()` + localizar o medicamento + ajustar a fila | O(n + r) |
| Buscar reposição | Busca linear | O(r) |
| Inserir por prioridade | Percurso + inserção | O(r) |
| Cancelar reposição | Busca + remoção | O(r) |
| Atender reposição | Localizar o medicamento + `popleft()` + nova solicitação, se necessário | O(n + r) |

> As complexidades representam o custo das operações sobre as estruturas utilizadas. Operações auxiliares, como localizar um medicamento antes de atualizar seu estoque, também influenciam o custo total.

---

## 14. Versionamento e Git

O desenvolvimento utiliza **Git** para controle de versões e organização das funcionalidades.

Branches principais:

| Branch | Conteúdo |
|---|---|
| `main` | Versão **GUI** (Tkinter) |
| `PharmaERP-CLI` | Versão **TUI** (terminal) |
| `develop` | Integração das funcionalidades |
| `Nightly` | Builds de desenvolvimento |
| `final_version` | Versão consolidada da entrega acadêmica |
| `feature/*`, `feat/*` | Uma funcionalidade por branch |
| `fix/*` | Correções |
| `refactor/*` | Refatorações (ex.: `refactor/Migrando-para-Tkinter`) |

### Histórico da versão 1.4.0 (Interface)

- Migração da interface de terminal para Tkinter;
- Menu de medicamentos gráfico, navegando por Frames da janela principal;
- Menu de reposição com fila prioritária;
- Menu de histórico com visualização e desfazer;
- Botão de voltar em todos os menus e telas;
- `Dockerfile` com Tkinter para execução em contêiner.

### Conventional Commits

| Prefixo | Utilização |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de problema |
| `docs` | Documentação |
| `refactor` | Refatoração |
| `test` | Testes |

Exemplo:

```bash
git commit -m "feat: adiciona prioridade por criticidade na fila"
```

Para informações sobre colaboração, padrões de código e organização do repositório, consulte o [`CONTRIBUTING.md`](./PharmaERP/docs/CONTRIBUTING.md).

---

## 15. Status do Projeto

**Versão 1.4.0 — Interface gráfica funcional.**

### Implementado

- [x] CRUD de medicamentos;
- [x] Validação de dados;
- [x] Busca linear por nome e por categoria;
- [x] Bubble Sort por preço;
- [x] IDs independentes para medicamentos e reposições;
- [x] Criação automática de solicitações;
- [x] Criticidade **CRÍTICO**, **ALERTA** e **AVISO**;
- [x] Fila com prioridade e FIFO em caso de empate;
- [x] Listagem, atendimento, alteração e cancelamento de solicitações;
- [x] Histórico de cadastros, alterações, remoções e reposições;
- [x] Desfazer última ação (pilha LIFO);
- [x] Interface gráfica em Tkinter com navegação por Frames;
- [x] Tabelas coloridas, listas suspensas e caixas de diálogo;
- [x] `Dockerfile` com suporte ao Tkinter.


### Fora do escopo da versão atual

- [ ] Persistência em arquivos;
- [ ] Banco de dados;
- [ ] Autenticação de usuários;
- [ ] API;
- [ ] Integração com fornecedores.

Esses recursos não fazem parte do escopo da versão acadêmica atual.

---

## 16. Licença

Este projeto está licenciado sob a **MIT License**.

Consulte o arquivo [`LICENSE`](./PharmaERP/docs/LICENSE) para obter o texto completo da licença.

---

<div align="center">

**PharmaERP — TDE Estruturas de Dados**

Desenvolvido por **Samuel, Samoel, Marcos e Gabriel**.

</div>