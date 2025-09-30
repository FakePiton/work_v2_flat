import os
import time
import pandas as pd
import flet as ft

from src.services.shevchenko_js.constants import HEADERS, Case, Gender, ParamsData
from src.services.shevchenko_js.api import ShevchenkoAPI


class ShevchenkoService:
    def read(self, file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.fillna("")

        headers = df.head()

        for header in HEADERS.keys():
            if header not in headers:
                # TODO: show UI
                raise Exception(f"Header {header} not found.")
        return df

    def write(self, declension_data: list[dict], dir_path_save: str) -> str:
        df = pd.DataFrame(declension_data)
        path = os.path.join(dir_path_save, f"declension_{time.time()}.xlsx")
        df.to_excel(path, index=False)
        return path

    def declension(
        self,
        cases: list,
        file_path: str,
        dir_path_save: str,
        log_output: ft.Text,
        page: ft.Page,
    ) -> str | None:
        df = self.read(file_path)

        declension_data = []
        shevchenko_api = ShevchenkoAPI(url=f"http://localhost:3000/")

        version = shevchenko_api.get_version()
        if version is None:
            return None

        for _, row in df.iterrows():
            row_dict = row.to_dict()

            gender = Gender.masculine if row_dict.get("gender") == "Ч" else Gender.feminine
            row_dict.pop("gender")
            item = {}

            for case in cases:
                res = shevchenko_api.get_case(
                    case=Case(case),
                    payload=ParamsData(**row_dict, gender=gender),
                )

                for key, value in res.items():
                    if value:
                        item[f"{case} - {HEADERS[key]}"] = value

                log_output.value += f"{' '.join(row_dict.values())} → {case}: [трансформовано]\n"
                page.update()
            declension_data.append(item)

        return self.write(
            declension_data=declension_data,
            dir_path_save=dir_path_save,
        )
