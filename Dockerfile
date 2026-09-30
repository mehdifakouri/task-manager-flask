FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


ENV HTTP_PROXY=http://192.168.94.1:10808
ENV HTTPS_PROXY=http://192.168.94.1:10808
ENV NO_PROXY=localhost,127.0.0.1


RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV HTTP_PROXY=
ENV HTTPS_PROXY=

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
