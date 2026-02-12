import pandas as pd
import os
from sqlalchemy import create_engine

class DataLoader:

    def save_dataframe(self, df: pd.DataFrame, directory: str, filename: str):
        if not os.path.exists(directory):
            os.makedirs(directory)
        df.to_csv(os.path.join(directory, f"{filename}.csv"), index=False)
        print(f"Arquivo salvo em {directory}")

    def save_to_postgres(self, df: pd.DataFrame, table_name: str, connection_string: str):
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Tabela {table_name} criada/atualizada no Postgres")