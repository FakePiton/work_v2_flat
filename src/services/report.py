from src.services.data_repository import PandasDataRepository


class Report:
    def __init__(self, pd_data_repository: PandasDataRepository):
        self.pd_data_repository = pd_data_repository

    def show_overdue_vacation(self) -> str:
        text = ""
        leaves = self.pd_data_repository.get_overdue_leave()

        if leaves is None:
            return text
        text = (
            f"Військовослужбовці які повинні повернутися з відпустки: \n {'-' * 40} \n"
        )

        for row in leaves.itertuples(index=True):
            text += (
                f"ПІБ: {row[2]}\n"
                f"Підрозділ: {row[3]}\n"
                f"Тип відпустки: {row[4]}\n"
                f"Запланована дата прибуття: {row[22].strftime('%d.%m.%Y')}\n"
                f"{'-' * 40}\n"
            )
        return text

    def show_overdue_vlk(self) -> str:
        text = ""
        vlk = self.pd_data_repository.get_overdue_vlk()

        if vlk is None:
            return text
        text = (
            f"Військовослужбовці які повинні повернутися з ВЛК: \n {'-' * 40} \n"
        )

        for row in vlk.itertuples(index=True):
            text += (
                f"ПІБ: {row[2]}\n"
                f"Підрозділ: {row[3]}\n"
                f"Вид: {row[4]}\n"
                f"Дата вибуття : {row[13].strftime('%d.%m.%Y')}\n"
                f"{'-' * 40}\n"
            )
        return text

    def show_overdue_daily_field_food_kits(self) -> str:
        text = ""
        dffk = self.pd_data_repository.get_overdue_daily_field_food_kits()

        if dffk is None:
            return text

        text = (
            f"Військовослужбовці які повинні бути зняті з ДПНП: \n {'-' * 40} \n"
        )
        counts = dffk["1899-12-29 00:00:00.2"].value_counts().sort_index()
        for date, count in counts.items():
            text += f"\nДата: {date.date().strftime('%d.%m.%Y')} ({count} в\с)"

        return text
