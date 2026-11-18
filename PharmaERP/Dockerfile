# * USA A VERSÃO 3.12.3 DO PYTHON COMO IMAGEM BASE 
FROM python:3.12-slim

# DIRETÓRIO QUE O DOCKER DEVE IR
WORKDIR /src

# BAIXA APENAS O NECESSÁRIO PARA RODAR O CÓDIGO
COPY requirements.txt .

# INSTALA AS DEPENDẼNCIAS NECESSÁRIA
RUN pip install --no-cache-dir -r requirements.txt

# COPIA O CÓDIGO
COPY . . 

# RODA NO TERMINAL
CMD ["python3", "main.py"]
