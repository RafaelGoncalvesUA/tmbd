FROM tensorflow/tensorflow:2.6.0-gpu
WORKDIR /app
COPY serve.py .
COPY model .
RUN pip install flask torch pickle-mixin
CMD ["python", "serve.py"]
