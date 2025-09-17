from abc import ABC, abstractmethod
import os

import flet as ft

class BaseValidator(ABC):
    def __init__(self, page):
        self.page = page
        self.errors = []
        self.is_valid = True

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool: ...

    @abstractmethod
    def show_errors(self) -> None: ...


class BaseFletValidator(BaseValidator):
    def __init__(self, page: ft.Page):
        super().__init__(page)

    def validate(self, *args, **kwargs) -> bool: ...

    def show_errors(self) -> None:
        if self.errors:
            snackbar = ft.SnackBar(
                content=ft.Text("\n".join(self.errors)),
                bgcolor=ft.Colors.RED_400,
                behavior=ft.SnackBarBehavior.FLOATING,
                open=True
            )
            self.page.overlay.append(snackbar)
            self.page.snack_bar = snackbar
            self.page.update()



class IsExistsPathValidator(BaseFletValidator):
    def validate(self, file_path: str) -> bool:
        self.errors.clear()

        if not os.path.isfile(file_path):
            self.errors.append(f"Файл з таким шляхом [{file_path}] не знайдено")

            self.is_valid = len(self.errors) == 0
            if not self.is_valid:
                self.show_errors()
        return self.is_valid


class IsExistsDirValidator(BaseFletValidator):
    def validate(self, dir_path: str) -> bool:
        self.errors.clear()

        if not os.path.isdir(dir_path):
            self.errors.append(f"Деректорії з таким шляхом [{dir_path}] не знайдено")

            self.is_valid = len(self.errors) == 0
            if not self.is_valid:
                self.show_errors()
        return self.is_valid
