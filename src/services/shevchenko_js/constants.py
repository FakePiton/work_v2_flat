from enum import Enum
from dataclasses import dataclass


HEADERS = {
    "familyName": "Фамілія",
    "patronymicName": "По-батькові",
    "givenName": "Ім'я",
    "gender": "Стать",
}

class Gender(Enum):
    masculine = "masculine"
    feminine = "feminine"


@dataclass
class ParamsData:
    gender: Gender
    givenName: str | None
    patronymicName: str | None
    familyName: str | None

    def to_dict(self):
        return {
            "gender": self.gender.value,
            "givenName": self.givenName,
            "patronymicName": self.patronymicName,
            "familyName": self.familyName,
        }


class Case(Enum):
    ablative = "Орудний"
    accusative = "Знахідний"
    dative = "Давальний"
    genitive = "Родовий"
    locative = "Місцевий"
    nominative = "Називний"
    vocative = "Кличний"

