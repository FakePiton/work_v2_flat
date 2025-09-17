import flet as ft
import threading
from flet_route import Params,Basket

from src.constants import PATH, Action
from src.services.merge_pdf import MergePDF
from src.services.validators import IsExistsDirValidator


class MergeView:
    def view(self, page:ft.Page, params:Params, basket:Basket):
        page.title = "Об’єднання файлів"

        log_output = ft.Text("", selectable=True)

        def merge_files(e):
            log_output.value = "🔄 Почато об’єднання...\n"
            page.update()


            def process():
                dir_path = page.client_storage.get(PATH.PATH_FILES_PDF.value)
                validator_dir = IsExistsDirValidator(page=page)
                if validator_dir.validate(dir_path):
                    merge_pdf = MergePDF()
                    merge_pdf.merge_report(dir_pdf=dir_path)
                    log_output.value += merge_pdf.text_info
                else:
                    log_output.value = ""
                page.update()

            threading.Thread(target=process).start()

        return ft.View(
            f"/services/{Action.MERGE_PDF.value}",
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "📂 Об’єднання файлів",
                            size=22,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Divider(),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Об’єднати",
                                    icon=ft.Icons.MERGE_TYPE,
                                    on_click=merge_files
                                ),
                                ft.ElevatedButton(
                                    "Перейти до сервісів",
                                    on_click=lambda _: page.go("/services"),
                                ),
                            ]
                        ),
                        ft.Container(
                            content=log_output,
                            padding=10,
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=8,
                        ),
                    ],
                    spacing=20,
                )
            ]
        )
