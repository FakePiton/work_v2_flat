import flet as ft
from flet_route import Params, Basket
from src.constants import PATH

class SettingsView:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Налаштування"
        page.scroll = "auto"

        path_excel = ft.TextField(
            label="Шлях до файлу Excel",
            hint_text="C:/templates/template.xlsx",
            value=page.client_storage.get(PATH.PATH_EXCEL.value),
        )
        path_server_order = ft.TextField(
            label="Шлях на сервер до папки з наказами",
            hint_text="C:/output/",
            value=page.client_storage.get(PATH.PATH_SERVER_ORDER.value),
        )
        path_files_pdf = ft.TextField(
            label="Шлях до файлів PDF",
            hint_text="C:/output/",
            value=page.client_storage.get(PATH.PATH_FILES_PDF.value),
        )
        path_dir_declension = ft.TextField(
            label="Шлях до деректорії здерігання файлів відмінків",
            hint_text="C:/output/",
            value=page.client_storage.get(PATH.PATH_DIR_DECLENSION.value),
        )

        def save_settings(e):
            page.client_storage.set(PATH.PATH_EXCEL.value, path_excel.value)
            page.client_storage.set(PATH.PATH_SERVER_ORDER.value, path_server_order.value)
            page.client_storage.set(PATH.PATH_FILES_PDF.value, path_files_pdf.value)
            page.client_storage.set(PATH.PATH_DIR_DECLENSION.value, path_dir_declension.value)

            snackbar = ft.SnackBar(
                content=ft.Text("Налаштування збережено"),
                bgcolor=ft.Colors.GREEN_400,
                behavior=ft.SnackBarBehavior.FLOATING,
                open=True
            )

            page.overlay.append(snackbar)
            page.snack_bar = snackbar
            page.update()

        return ft.View(
            "/settings",
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "📁 Налаштування шляхів",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),
                        path_excel,
                        path_server_order,
                        path_files_pdf,
                        path_dir_declension,
                        ft.ElevatedButton(
                            "Зберегти",
                            icon=ft.Icons.SAVE,
                            on_click=save_settings,
                        ),
                        ft.ElevatedButton(
                            "Перейти на головну",
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    spacing=20,
                )
            ]
        )
