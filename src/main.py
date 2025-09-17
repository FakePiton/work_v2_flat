import flet as ft
from flet_route import Routing, path

from src.constants import Action

from src.views.index import IndexView
from src.views.services import ServicesView
from src.views.settings import SettingsView
from src.views.pages_services.merge import MergeView
from src.views.pages_services.order import OrderView
from src.views.pages_services.report_message import ReportMessageView


def main(page: ft.Page):
    app_routes = [
        path(url="/", clear=True, view=IndexView().view),
        path(url="/settings", clear=False, view=SettingsView().view),
        path(url="/services", clear=False, view=ServicesView().view),
        path(url=f"/services/{Action.MERGE_PDF.value}", clear=False, view=MergeView().view),
        path(url=f"/services/{Action.CREATE_TEMPLATE_ORDER.value}", clear=False, view=OrderView().view),
        path(url=f"/services/{Action.REPORT_MESSAGE.value}", clear=False, view=ReportMessageView().view),
    ]

    Routing(
        page=page,
        app_routes=app_routes,
    )
    page.go(page.route)

ft.app(main, assets_dir="assets")
