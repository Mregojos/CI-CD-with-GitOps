# Dockerfile
FROM python:slim
WORKDIR /app
COPY . .
VOLUME /app
RUN pip install -U -r requirements.txt -q
CMD ["streamlit", "run", "Main.py"]
