# Usa la imagen oficial de Airflow como base
FROM apache/airflow:2.6.0-python3.9

# Utiliza usuario root
USER root

# Copia tus archivos al contenedor

COPY ./dags /opt/airflow/dags
COPY ./requirements.txt /opt/airflow/requirements.txt
COPY ./script/entrypoint.sh /opt/airflow/script/entrypoint.sh

# Si editaste el archivo en Windows conviertelo a formato Unix
RUN sed -i 's/\r//' /opt/airflow/script/entrypoint.sh

# Dale permisos de ejecución
RUN chmod +x /opt/airflow/script/entrypoint.sh

# Establece el entrypoint
ENTRYPOINT ["/bin/bash", "/opt/airflow/script/entrypoint.sh"]

# Utiliza usuario airflow
USER airflow
