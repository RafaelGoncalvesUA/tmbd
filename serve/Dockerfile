FROM python:3.11-slim
WORKDIR /app
COPY serve/serve.py .
COPY model .
RUN pip install flask scikit-learn pandas tensorflow
RUN pip install fasttext-wheel
CMD ["python", "serve.py"]
