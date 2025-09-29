import requests
from src.services.shevchenko_js.constants import ParamsData, Case


class ShevchenkoAPI:
    def __init__(self, url: str):
        self.url = url

    def get_case(self, case: Case, payload: ParamsData):
        url = self.url + case.name
        headers = {"Content-Type": "application/json"}
        res = requests.post(url=url,headers=headers, json=payload.to_dict())
        return res.json()

    def get_version(self) -> dict | None:
        try:
            return requests.get(self.url).json()
        except Exception:
            return None
