FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY scripts/gen.py .
COPY webapp.py .

EXPOSE 8000

CMD ["python3", "webapp.py"]
