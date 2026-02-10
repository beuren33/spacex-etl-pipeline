import pandas as pd
from typing import List, Dict


class SpaceXTransformer:
    def transform_launches(self, launches_data: List[Dict]) -> pd.DataFrame:
        if not launches_data:
            return pd.DataFrame()

        df = pd.DataFrame(launches_data)

        df["date_utc"] = pd.to_datetime(df["date_utc"])
        df["year"] = df["date_utc"].dt.year
        df["month"] = df["date_utc"].dt.month

        df["success"] = df["success"].fillna(False).astype(bool)

        df["rocket_id"] = df["rocket"]

        relevant_cols = [
            "id",
            "name",
            "date_utc",
            "year",
            "month",
            "success",
            "rocket_id",
        ]
        return df[relevant_cols]

    def transform_rockets(self, rockets_data: List[Dict]) -> pd.DataFrame:
        if not rockets_data:
            return pd.DataFrame()

        df = pd.DataFrame(rockets_data)

        df["mass_kg"] = df["mass"].apply(
            lambda x: x.get("kg") if isinstance(x, dict) else None
        )

        df = df.rename(columns={"id": "rocket_id", "name": "rocket_name"})

        relevant_cols = [
            "rocket_id",
            "rocket_name",
            "cost_per_launch",
            "mass_kg",
            "active"
        ]
        
        return df[relevant_cols]