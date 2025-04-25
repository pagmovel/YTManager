FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
COPY requirements.txt .
COPY src/ src/

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Configura as variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]