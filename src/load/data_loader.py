import pandas as pd
import os


class DataLoader:
    def save_dataframe(self, df: pd.DataFrame, directory: str, filename: str):
        if df.empty:
            print(f"DataFrame para {filename} está vazio.")
            return

        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_path = os.path.join(directory, f"{filename}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Dados salvos em {csv_path}")

        try:
            parquet_path = os.path.join(directory, f"{filename}.parquet")
            df.to_parquet(parquet_path, index=False)
            print(f"Dados salvos em {parquet_path}")
        except ImportError:
            print("Biblioteca 'pyarrow' não instalada.Salvamento em Parquet.")
            print("Instale com: pip install pyarrow")
