# * USA A VERSÃO 3.12.3 DO PYTHON COMO IMAGEM BASE 
FROM python:3.12-slim
# INSTALA O TKINTER E DEPENDÊNCIAS GRÁFICAS DO LINUX
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# DIRETÓRIO QUE O DOCKER DEVE IR
WORKDIR /src

# BAIXA APENAS O NECESSÁRIO PARA RODAR O CÓDIGO
COPY requirements.txt .

# INSTALA AS DEPENDẼNCIAS NECESSÁRIA
RUN pip install --no-cache-dir -r requirements.txt

# COPIA O CÓDIGO
COPY . . 

# RODA NO TERMINAL
CMD ["python3", "__main__.py"]