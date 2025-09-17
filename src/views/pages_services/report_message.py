import flet as ft
import threading
from datetime import date

from flet_route import Params,Basket
from src.constants import Action
from src.services.report_order_message import ReportOrderMessage
from src.services.utils import show_snackbar


class ReportMessageView:
    def view(self, page:ft.Page, params:Params, basket:Basket):
        page.title = "Генерація звіту"
        page.scroll = "auto"

        today = date.today()
        selected_date = ft.TextField(
            label="Дата звіту",
            read_only=True,
            value=today.strftime("%d.%m.%Y"),
        )

        report_text = ft.Text("", selectable=True)
        report_container = ft.Container(
            content=ft.Column([report_text], scroll="auto"),
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            padding=10,
            border_radius=8
        )

        def on_date_selected(e):
            selected_date.value = e.control.value.strftime("%d.%m.%Y")
            page.update()

        date_picker = ft.DatePicker(
            on_change=on_date_selected,
            value=today,
            first_date=date(2020, 1, 1),
            last_date=date(2030, 12, 31),
            confirm_text="OK",
            cancel_text="Скасувати"
        )

        button_date_picker = ft.ElevatedButton(
            "Дата",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(date_picker),
        )


        def generate_report(e):
            report_text.value = f"🔄 Генерація звіту за {selected_date.value}...\n"
            page.update()

            def process():
                page.pandas_data_repository.clear_errors()

                report_message = ReportOrderMessage(
                    sheets=page.pandas_data_repository.sheets,
                    pd_data_repository=page.pandas_data_repository,
                )
                report_text.value += report_message.get_report(order_date=date_picker.value)
                page.update()

                warning = page.pandas_data_repository.errors
                if warning:
                    show_snackbar(page=page, text=warning, color=ft.Colors.YELLOW)

                page.pandas_data_repository.clear_errors()

            threading.Thread(target=process).start()

        return ft.View(
            f"/services/{Action.REPORT_MESSAGE.value}",
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "📊 Генерація звіту",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(),
                        ft.Row(
                            [
                                selected_date,
                                button_date_picker,
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Сформувати звіт",
                                    icon=ft.Icons.ASSIGNMENT,
                                    on_click=generate_report
                                ),
                                ft.ElevatedButton(
                                    "Перейти до сервісів",
                                    on_click=lambda _: page.go("/services"),
                                ),
                            ]
                        ),
                        ft.Row(
                            [report_container],
                            expand=True,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                )
            ]
        )
