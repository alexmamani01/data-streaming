from datetime import datetime
from airflow import    DAG
from airflow.operators.python import PythonOperator
import uuid

default_arg={
    "owner": "airscholar",
    "start_date": datetime(2025, 3, 25, 23, 40)
}

def get_data2():
    import json
    import requests

    url="https://randomuser.me/api/"
    response= requests.get(url)
    res=response.json()
    res=res.get('results',[])[0]
    return res
    
def format_data2(res):
    data = {}
    data['id'] = uuid.uuid4()
    data['gender'] = res.get("gender", '')  
    data['first_name'] = res.get('name', {}).get('first', '')
    data['last_name'] = res.get('name', {}).get('last', '')
    location = res.get('location', {})
    data['address'] = f"{location.get('street', {}).get('number', '')} {location.get('street', {}).get('name', '')}, {location.get('city', '')}, {location.get('state', '')}, {location.get('country', '')}"
    data['post_code'] = location.get('postcode', '')
    data['email'] = res.get('email', '') 
    data['username'] = res.get('login', {}).get('username', '')
    data['dob'] = res.get('dob', {}).get('date', '')  
    data['registered_date'] = res.get('registered', {}).get('date', '')
    data['phone'] = res.get('phone', '')
    data['picture'] = res.get('picture', {}).get('medium', '')
    return data

def stream_data2():
    import json
    from kafka import KafkaProducer
    import time
    import logging

    
    #para enviar la informacion al broker de kafka
    producer=KafkaProducer(bootstrap_servers= ['broker:29092'], max_block_ms=5000)
    curr_time= time.time()
    while True:
        if time.time()>curr_time + 60:
            break
        try: 
            res=get_data2()
            res=format_data2(res)
            producer.send('usuarios', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error('Error: {e}')

            continue

    

with DAG(
    dag_id="usuarios_creados",
    default_args=default_arg,
    schedule= '@daily',
    catchup=False) as dag:

    #task1
    streaming_task=PythonOperator (
        task_id="stream_data_from_api2",
        python_callable=stream_data2
    )

