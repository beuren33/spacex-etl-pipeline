from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd

DB_CONN_STRING = "postgresql://airflow:airflow@postgres:5432/airflow"

@dag(
    dag_id='spacex_etl_pipeline_v2',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['spacex']
)
def spacex_etl():

    @task
    def extract_data():
        import yaml
        import logging
        import sys
        from include.src.extract.spacex_extractor import SpaceXExtractor
        
        sys.path.insert(0, '/usr/local/airflow/include')

        config_path = '/usr/local/airflow/include/config/config.yaml'

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
       
        logging.info(f"Dicionário de endpoints encontrado: {config['api'].get('endpoints')}")
        
        extractor = SpaceXExtractor(
            base_url=config['api']['base_url'],
            version=config['api']['version'],
            timeout=config['api'].get('timeout', 30),
            retry_attempts=config['api'].get('retry_attempts', 3)
        )
        
        
        endpoints = config['api'].get('endpoints', {})
        l_path = endpoints.get('launches', 'launches')
        r_path = endpoints.get('rockets', 'rockets')
        
        launches = extractor.get_data(l_path)
        rockets = extractor.get_data(r_path)
        
        return {"launches": launches, "rockets": rockets}

    @task
    def transform_data(raw_data):
        import sys
        from include.src.transform.spacex_transform import SpaceXTransformer
        
        sys.path.insert(0, '/usr/local/airflow/include')
        transformer = SpaceXTransformer()
        launches_df = transformer.transform_launches(raw_data['launches'])
        rockets_df = transformer.transform_rockets(raw_data['rockets'])
        
        final_df = transformer.transform_launches(raw_data['launches']) 
        
        for col in final_df.select_dtypes(include=['datetime64', 'datetimetz']).columns:
            final_df[col] = final_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return final_df.to_dict(orient='records')

    @task
    def load_data(clean_data_dict):
        from include.src.load.data_loader import DataLoader
        import pandas as pd
        import sys
        sys.path.insert(0, '/usr/local/airflow/include')
        
        df = pd.DataFrame(clean_data_dict)
        loader = DataLoader()
        
        loader.save_to_postgres(
            df=df,
            table_name='launches_analytics',
            connection_string=DB_CONN_STRING
        )

    raw = extract_data()
    clean = transform_data(raw)
    load_data(clean)

dag_instance = spacex_etl()