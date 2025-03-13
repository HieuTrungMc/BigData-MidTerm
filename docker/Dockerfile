FROM python:3.10-slim

WORKDIR /app

COPY docker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../crawlers /app/crawlers

COPY . .

EXPOSE 3000

WORKDIR /app/crawlers

ENV PYTHONPATH="${PYTHONPATH}:/app/crawlers"

CMD ["python", "main.py"]