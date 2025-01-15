FROM python:3.11-slim
WORKDIR /app
COPY process/consumer.py .
COPY model .
RUN pip install kafka-python-ng pandas tensorflow
CMD ["python", "consumer.py"]
