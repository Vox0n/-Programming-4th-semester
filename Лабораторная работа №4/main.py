from model import CurrencyRates
from controller import DBManager
from view import render_rates, display_console
import argparse


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Приложение для получения курсов валют ЦБ РФ")
    parser.add_argument("-c", "--currencies", nargs="+",
                        default=["USD", "EUR", "GBP", "CNY"],
                        help="Список валют для отслеживания (коды из 3 букв)")
    parser.add_argument("-o", "--output", choices=["console", "html"],
                        default="html",
                        help="Способ вывода результатов")
    args = parser.parse_args()

    try:
        # Инициализация компонентов
        currency_model = CurrencyRates()
        db_manager = DBManager()

        # Установка списка валют
        currency_model.currencies = args.currencies
        db_manager.save_tracked_currencies(args.currencies)

        # Получение и сохранение курсов
        rates = currency_model.fetch_rates()
        if rates:
            db_manager.save_rates(rates)
            latest_rates = db_manager.get_latest_rates()

            # Вывод результатов
            if args.output == "console":
                display_console(latest_rates)
            else:
                html_content = render_rates(latest_rates)
                with open("currency_rates.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("HTML-отчет сохранен в файл currency_rates.html")
        else:
            print("Не удалось получить курсы валют. Попробуйте позже.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()