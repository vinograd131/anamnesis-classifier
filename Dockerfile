FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/label_mapping.json ./data/label_mapping.json
COPY scripts/ ./scripts/

CMD ["python", "scripts/export_mapping.py"]
