from jinja2 import Environment, FileSystemLoader

def render_rates(rates, template_name="rates.html"):
    """
    Генерация HTML на основе шаблона Jinja2
    :param rates: список курсов валют
    :param template_name: имя файла шаблона
    :return: сгенерированный HTML
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template.render(rates=rates)

def display_console(rates):
    """Вывод курсов в консоль"""
    print("\nТекущие курсы валют ЦБ РФ:")
    print("-" * 40)
    print(f"{'Валюта':<10}{'Курс':<15}{'Дата':<20}")
    print("-" * 40)
    for code, rate, date in rates:
        print(f"{code:<10}{rate:<15.4f}{date:<20}")
    print("-" * 40)