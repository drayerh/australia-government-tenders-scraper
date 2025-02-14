# docker/Dockerfile
FROM python:3.10-slim
RUN pip install scrapy boto3 motor redis scrapy-zyte-smartproxy
COPY . /app
WORKDIR /app
CMD ["python", "orchestrator/task_manager.py"]