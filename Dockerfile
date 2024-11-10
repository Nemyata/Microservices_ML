FROM python:3.9-slim

WORKDIR /app

COPY . /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "features.py"]
CMD ["python", "metric.py"]
CMD ["python", "predictor.py"]
CMD ["python", "plot.py"]
