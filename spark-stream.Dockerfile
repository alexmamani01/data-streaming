FROM bitnami/spark:3.5.5

# Utiliza usuario root
USER root

# Instalar dependencias adicionales
RUN apt-get update && apt-get install -y \
    python3-pip \
    && pip3 install cassandra-driver \
    && apt-get clean

# Establecer la variable de entorno para ejecutar el script
ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Copia tus archivos al contenedor
COPY ./spark_stream.py /opt/spark/spark_stream.py

# Si editaste el archivo en Windows conviertelo a formato Unix
RUN sed -i 's/\r//' /opt/spark/spark_stream.py

# Dale permisos de ejecución
RUN chmod +x /opt/spark/spark_stream.py

# Comando para ejecutar el script cuando el contenedor se inicie
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0", "--master", "spark://spark-master:7077", "/opt/spark/spark_stream.py"]

# Utiliza usuario standard
USER 1001