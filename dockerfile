FROM python:3.9-slim
WORKDIR /app
COPY server.py client.py logger.py /app/
# Créer un dossier pour les logs
RUN mkdir /data 
CMD ["python", "server.py"]