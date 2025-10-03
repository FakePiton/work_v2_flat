import flet as ft
import threading

from flet_route import Params,Basket

from src.constants import Action, PATH
from src.services.order import NewOrder
from src.services.report import Report
from src.services.validators import IsExistsDirValidator


class OrderView:
    def view(self, page:ft.Page, params:Params, basket:Basket):
        page.title = "Створення шаблону замовлення"
        page.scroll = "auto"

        include_create_template = ft.Checkbox(label="Створити шаблон", value=True)
        include_overdue_vacation = ft.Checkbox(
            label="Додати звіт по простроченим відпустках",
            value=True,
        )
        include_overdue_vlk = ft.Checkbox(
            label="Додати звіт по простроченим ВЛК",
            value=True,
        )
        include_overdue_daily_field_food_kits= ft.Checkbox(
            label="Додати звіт по простроченим ДПНП",
            value=True,
        )

        checkbox_group = ft.Container(
            content=ft.Column(
                [
                    ft.Text("⚙️ Параметри", size=18, weight=ft.FontWeight.BOLD),
                    include_create_template,
                    include_overdue_vacation,
                    include_overdue_vlk,
                    include_overdue_daily_field_food_kits,
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
        )

        info_text = ft.Text("", selectable=True)
        info_container = ft.Container(
            content=ft.Column([info_text], scroll="auto"),
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            padding=10,
            border_radius=8
        )

        def create_template(e):
            new_order = NewOrder(pd_data_repository=page.pandas_data_repository)
            report = Report(pd_data_repository=page.pandas_data_repository)

            if include_create_template.value:
                info_text.value = "🔄 Створення шаблону...\n"
                page.update()

            def process():
                page.pandas_data_repository.clear_errors()

                result = ""

                if include_create_template.value:
                    dir_server_path = page.client_storage.get(PATH.PATH_SERVER_ORDER.value)
                    validator_dir = IsExistsDirValidator(page=page)
                    if validator_dir.validate(dir_server_path):
                        new_order.create_template(path_dir_server=dir_server_path)
                        result += new_order.text_info + "\n\n"
                    else:
                        info_text.value = "Помилка створення шаблону!"
                    page.update()

                if include_overdue_vacation.value:
                    result += report.show_overdue_vacation() + "\n\n"

                if include_overdue_vlk.value:
                    result += report.show_overdue_vlk() + "\n\n"

                if include_overdue_daily_field_food_kits.value:
                    result += report.show_overdue_daily_field_food_kits() + "\n\n"

                info_text.value = result
                page.update()

            threading.Thread(target=process).start()

        return ft.View(
            f"/services/{Action.CREATE_TEMPLATE_ORDER.value}",
            controls=[
                ft.Column(
                    [
                        ft.Text(

                            "📝 Створення шаблону замовлення", size=24,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Divider(),
                        checkbox_group,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Створити шаблон",
                                    icon=ft.Icons.DESCRIPTION,
                                    on_click=create_template,
                                ),
                                ft.ElevatedButton(
                                    "Перейти до сервісів",
                                    on_click=lambda _: page.go("/services"),
                                ),
                            ]
                        ),

                        info_container
                    ],
                    spacing=20,
                    expand=True,
                )
            ]
        )
