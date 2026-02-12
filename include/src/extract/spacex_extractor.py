import requests
import json
import time
import os
from typing import List, Dict, Optional


class SpaceXExtractor:

    def __init__(self, 
                 base_url: str, 
                 version: str, 
                 timeout: int, 
                 retry_attempts: int):
        self.base_url = base_url.rstrip("/")
        self.version = version
        self.timeout = timeout
        self.retry_attempts = retry_attempts

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{self.version}{endpoint}"

    def get_data(self, endpoint: str) -> Optional[List[Dict]]:
        url = self._build_url(endpoint)
        for attempt in range(self.retry_attempts):
            try:
                print(f"Buscando dados de {url} (tentativa {attempt + 1})")
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Erro na requisição: {e}. Tentando novamente")
                time.sleep(5)

        msg = f"""
        Falha ao buscar dados de {url} após {self.retry_attempts} tentat.
        """
        print(f"Falha ao buscar dados de {url} após {self.retry_attempts} tentat")
        return None

    def save_to_json(self, data: List[Dict], directory: str, filename: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Dados salvos em {filepath}")
