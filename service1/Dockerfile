FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/* && pip install psutil requests docker

WORKDIR /app1

COPY service1.py .

EXPOSE 8199

CMD ["python", "service1.py"]
