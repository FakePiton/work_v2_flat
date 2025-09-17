import threading
import time

import flet as ft
from flet_route import Params,Basket

from src.constants import PATH
from src.services.data_repository import get_pandas_data_repository
from src.services.validators import IsExistsPathValidator


class IndexView:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Головна"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = "auto"


        sync_not = "Синхронізація не виконана"
        sync_in_proces = "Синхронізація триває..."
        sync_done = "Синхронізація успішна"

        sync_start_pain = {"text": sync_not, "color": ft.Colors.RED_400}
        if hasattr(page, "pandas_data_repository"):
            sync_start_pain = {"text": sync_done, "color": ft.Colors.GREEN_400}

        sync_status = ft.Text(sync_start_pain["text"], color=sync_start_pain["color"])

        sync_indicator = ft.ProgressRing(width=30, height=30, visible=False)

        def sync_now(e):
            sync_status.value = sync_in_proces
            sync_status.color = ft.Colors.BLUE_400
            sync_indicator.visible = True
            page.update()

            def perform_sync():
                file_path = page.client_storage.get(PATH.PATH_EXCEL.value)
                validator_path = IsExistsPathValidator(page=page)
                if validator_path.validate(file_path):
                    page.pandas_data_repository = get_pandas_data_repository(file_path=file_path)
                    sync_status.value = sync_done
                    sync_status.color = ft.Colors.GREEN_400
                    sync_indicator.visible = False
                    page.update()
                else:
                    sync_indicator.visible = False
                    sync_status.value = sync_not
                    sync_status.color = ft.Colors.RED_400
                    page.update()

            threading.Thread(target=perform_sync).start()

        nav_panel = ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(
                        "Сервіси",
                        icon=ft.Icons.BUILD,
                        on_click=lambda _: page.go(f"/services"),
                    ),
                    ft.ElevatedButton(
                        "Налаштування",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda _: page.go(f"/settings"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10
        )

        sync_panel = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SYNC, color=ft.Colors.BLUE_400),
                    sync_indicator,
                    sync_status,
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        tooltip="Оновити",
                        on_click=sync_now
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8
        )

        header = ft.Text("👋 Ласкаво просимо!", size=28, weight=ft.FontWeight.BOLD)

        return ft.View(
            "/",
            controls=[
                ft.Column(
                    [
                        header,
                        nav_panel,
                        ft.Divider(),
                        sync_panel,
                    ],
                    spacing=25,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )
