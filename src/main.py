from datetime import datetime

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import (
    get_the_best_cashback_categories,
    individual_transaction_finder,
    investment_bank,
    mobile_phone_finder,
    simple_finder,
)
from src.utils import data_with_normalized_spacebars
from src.views import page_events_json, page_main_json


def pages(date: datetime, transactions: pd.DataFrame, range_type: str = "M") -> None:
    """
    Принимает дату в формате DD.MM.YYYY, данные транзакций, диапазон данных("W", "M", "Y", "ALL")
    и генерирует данные в JSON формате для главной страницы и старицы событий
    """

    page_main_json(date, transactions)
    page_events_json(date, transactions, range_type)


def services(date: datetime, transactions: pd.DataFrame, limit: int, search_string: str) -> None:
    """
    Принимает данные транзакций, год и месяц для обработки
    и генерирует JSON файлы для сервисов
    """

    get_the_best_cashback_categories(transactions, date)
    investment_bank(date, transactions, limit)
    simple_finder(transactions, search_string)
    mobile_phone_finder(transactions)
    individual_transaction_finder(transactions)


def reports(transactions: pd.DataFrame, category: str) -> None:
    """
    Принимает данные о транзакции и категорию для подсчета трат и генерирует отчёты
    """

    spending_by_category(transactions, category)
    spending_by_weekday(transactions)
    spending_by_workday(transactions)


if __name__ == "__main__":
    data = data_with_normalized_spacebars()

    pages(date=datetime.today(), transactions=data, range_type="M")
    services(date=datetime.today(), transactions=data, limit=100, search_string="Оплата")
    reports(transactions=data, category="Переводы")
