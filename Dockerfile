FROM apache/airflow:2.5.0

ENV PYTHONPATH="/opt/airflow"

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . .