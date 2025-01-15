FROM python:3.11-slim
WORKDIR /app
COPY serve.py .
COPY model .
RUN pip install flask scikit-learn pandas tensorflow
CMD ["python", "serve.py"]
