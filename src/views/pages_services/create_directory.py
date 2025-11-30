import flet as ft
import threading
import os

from flet_route import Params, Basket

from src.constants import Action, PATH
from src.services.create_directory import CreateDirectoryService
from src.services.utils import show_snackbar
from src.services.validators import IsExistsDirValidator


class CreateDirectoryView:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Створеня папок"
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
                        "Перша колонта з іменнами попок",
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
            label="Файл зі назвами папок",
            read_only=True,
        )
        name_base_dir = ft.TextField(label="Назва основної папки")

        dir_path = page.client_storage.get(PATH.PATH_DIR_CREATE_DIRECTORY.value)
        open_file_button = ft.ElevatedButton(
            text="📂 Відкрити деректорію зі створеними папками",
            icon=ft.Icons.FOLDER_OPEN,
            disabled=True,
            on_click=lambda e: os.startfile(dir_path),
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

        def create_dirs(e):
            validator_dir = IsExistsDirValidator(page=page)
            validator_dir.validate(dir_path)

            if not selected_file.value:
                show_snackbar(
                    page=page,
                    color=ft.Colors.RED_400,
                    text="❗ Спочатку виберіть файл",
                )
                return

            if not name_base_dir.value:
                show_snackbar(
                    page=page,
                    color=ft.Colors.RED_400,
                    text="❗ Спочатку вкажіть назву основної папки",
                )
                return

            log_output.value = f"📄 Файл: {selected_file.value}\n"
            log_output.value += "\n🔄 Обробка...\n"
            page.update()

            def process():
                create_dir_service = CreateDirectoryService()
                validator_dir = IsExistsDirValidator(page=page)
                if validator_dir.validate(dir_path):
                    create_dir_service.create_dirs(
                        file_path=selected_file.value,
                        path_dir=dir_path,
                        name_base_dir=name_base_dir.value,
                    )

                    log_output.value += "\n✅ Папки створені.\n"
                    open_file_button.disabled = False

                page.update()

            threading.Thread(target=process).start()

        return ft.View(
            f"/services/{Action.DECLENSION.value}",
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "Сервіс створення папок",
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
                                ),
                                name_base_dir,
                            ]
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Створити папки",
                                    icon=ft.Icons.SWAP_HORIZ,
                                    on_click=create_dirs,
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
