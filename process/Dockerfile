FROM python:3.11-slim
WORKDIR /app
COPY process/consumer.py .
COPY model .
RUN pip install kafka-python-ng pandas tensorflow
RUN pip install fasttext-wheel
CMD ["python", "consumer.py"]
