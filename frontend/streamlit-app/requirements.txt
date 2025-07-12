# requirements.txt
streamlit==1.28.2
pandas==2.1.3
numpy==1.25.2
plotly==5.17.0
openpyxl==3.1.2

# .streamlit/config.toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
maxUploadSize = 50

[client]
showErrorDetails = true

# Dockerfile (optional for containerized deployment)
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# .gitignore additions for Streamlit
.streamlit/secrets.toml
__pycache__/
*.pyc
.DS_Store