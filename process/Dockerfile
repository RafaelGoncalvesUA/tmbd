FROM python:3.11-slim
WORKDIR /app
COPY consumer.py .
COPY model .
RUN pip install kafka-python-ng pandas tensorflow
CMD ["python", "consumer.py"]
