FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV MPLBACKEND=Agg

RUN pip install --no-cache-dir pandas matplotlib seaborn azure-storage-blob

CMD ["python", "data_analysis.py"]