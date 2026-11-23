FROM python:3.12-slim

# Runtime do Tk + cliente X11 + uma fonte (a imagem slim não traz nada disso)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libtk8.6 libx11-6 fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY . .

CMD ["python", "__main__.py"]