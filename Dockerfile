FROM quay.io/astronomer/astro-runtime:12.1.1

ENV PYTHONPATH="/opt/airflow"

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . .