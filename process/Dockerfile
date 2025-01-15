FROM tensorflow/tensorflow:2.6.0-gpu
WORKDIR /app
COPY . .
COPY model .
RUN pip install kafka-python-ng pandas
CMD ["python", "consumer.py"]
