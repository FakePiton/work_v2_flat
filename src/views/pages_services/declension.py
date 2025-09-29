import flet as ft
import threading
import os

from flet_route import Params,Basket

from src.constants import Action, PATH
from src.services.shevchenko_js.constants import Case
from src.services.shevchenko_js.service import ShevchenkoService
from src.services.utils import show_snackbar
from src.services.validators import IsExistsDirValidator


class DeclensionView:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Відмінювання слів"
        page.scroll = "auto"

        file_requirements = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "📘 Вимоги до вхідного файлу",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "• Формат: XLSX",
                        selectable=True,
                    ),
                    ft.Text(
                        "• Зголовки: familyName (Фамілія), patronymicName (Побатькові), givenName (Ім'я), gender (Стаць)",
                        selectable=True,
                    ),
                ],
                spacing=8,
            ),
            padding=8,
            bgcolor=ft.Colors.GREY_200,
            border_radius=10,
        )

        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        selected_file = ft.TextField(
            label="Файл зі словами",
            read_only=True,
        )
        path_file = ""

        open_file_button = ft.ElevatedButton(
            text="📂 Відкрити згенерований файл",
            icon=ft.Icons.FOLDER_OPEN,
            disabled=True,
            on_click=lambda e: os.startfile(path_file)
        )

        case_checkboxes = [ft.Checkbox(label=case.value, value=False) for case in Case]

        case_selector = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "🎯 Виберіть цільові відмінки",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    *case_checkboxes
                ],
                spacing=8,
            ),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
        )

        log_output = ft.Text("", selectable=True)
        log_container = ft.Container(
            content=ft.Column([log_output], scroll="auto"),
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            padding=10,
            border_radius=8,
        )

        def pick_file(e):
            def on_result(e):
                if e.files:
                    selected_file.value = e.files[0].path
                    page.update()

            file_picker.on_result = on_result
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["xlsx"],
            )

        def transform_words(e):
            if not selected_file.value:
                show_snackbar(
                    page=page,
                    color=ft.Colors.RED_400,
                    text="❗ Спочатку виберіть файл",
                )
                return

            selected_cases = [cb.label for cb in case_checkboxes if cb.value]
            if not selected_cases:
                show_snackbar(
                    page=page,
                    color=ft.Colors.RED_400,
                    text="❗ Виберіть хоча б один цільовий відмінок",
                )
                return

            log_output.value = f"📄 Файл: {selected_file.value}\n"
            log_output.value += "🔁 Вибрані відмінки:\n"
            for case in selected_cases:
                log_output.value += f"• {case}\n"
            log_output.value += "\n🔄 Обробка...\n"
            page.update()

            def process():
                global path_file

                shevchenko_service = ShevchenkoService()
                dir_path = page.client_storage.get(PATH.PATH_DIR_DECLENSION.value)

                validator_dir = IsExistsDirValidator(page=page)
                if validator_dir.validate(dir_path):
                    path_file = shevchenko_service.declension(
                        cases=selected_cases,
                        file_path=selected_file.value,
                        dir_path_save=dir_path,
                        log_output=log_output,
                        page=page,
                    )
                    if path_file is None:
                        show_snackbar(
                            page=page,
                            color=ft.Colors.RED_400,
                            text="❗ Проблеми з сервісом shevchenko.js перевірте роботу docker"
                        )
                        log_output.value = ""
                    else:
                        log_output.value += "\n✅ Новий файл збережено.\n"
                        open_file_button.disabled = False

                else:
                    log_output.value = ""
                page.update()

            threading.Thread(target=process).start()

        return ft.View(
            f"/services/{Action.DECLENSION.value}",
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "🧠 Сервіс відмінювання слів",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(),
                        file_requirements,
                        ft.Row(
                            [
                                selected_file,
                                ft.IconButton(
                                    icon=ft.Icons.UPLOAD_FILE,
                                    tooltip="Вибрати файл",
                                    on_click=pick_file,
                                )
                            ]
                        ),
                        case_selector,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Трансформувати",
                                    icon=ft.Icons.SWAP_HORIZ,
                                    on_click=transform_words,
                                ),
                                ft.ElevatedButton(
                                    "Перейти до сервісів",
                                    on_click=lambda _: page.go("/services"),
                                ),
                                open_file_button,
                            ]
                        ),

                        log_container
                    ],
                    spacing=20,
                    expand=True,
                    scroll="auto",
                )
            ]
        )
