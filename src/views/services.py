import flet as ft
from flet_route import Params,Basket
from src.constants import Action


class ServicesView:
    def view(self, page:ft.Page, params:Params, basket:Basket):
        page.title = "Сервіси"
        is_pd_data_repository = bool(hasattr(page, "pandas_data_repository"))

        services = [
            {
                "name": "Створити шаблон наказу",
                "description": (
                    "Створює шаблон наказу на сьогоднішній день та визначає в/с які "
                    "повинні були повернутися з відпусток, ВЛК"
                ),
                "action": Action.CREATE_TEMPLATE_ORDER.value,
                "button_disabled": False if is_pd_data_repository else True,
            },
            {
                "name": "Звіт",
                "description": "Видає звіт по вибраному наказу",
                "action": Action.REPORT_MESSAGE.value,
                "button_disabled": False if is_pd_data_repository else True,
            },
            {
                "name": "Обєднати PDF",
                "description": "Обєднує PDF файли в один PDF файл",
                "action": Action.MERGE_PDF.value,
                "button_disabled": False,
            },
        ]

        service_list = ft.ListView(expand=True, spacing=10)

        for service in services:
            service_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    service["name"],
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(service["description"], size=14),
                                ft.ElevatedButton(
                                    f"Перейти",
                                    key=service['action'],
                                    on_click=lambda e: page.go(f"/services/{e.control.key}"),
                                    disabled=service["button_disabled"],
                                ),
                            ]
                        ),
                        padding=10,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=8
                    )
                )
            )

        return ft.View(
            "/services",
            controls=[
                service_list,
                ft.ElevatedButton(
                    "Перейти на головну",
                    on_click=lambda _: page.go("/"),
                ),
            ]
        )