import random
import math

def round_value(number: float) -> float:
    """
    Округляет заданное число до 4 знаков после запятой.

    ### Параметры:
    * `number (float)` - Число, которое нужно округлить.

    ### Возвращаемое значение:
    * `float` - Округленное число с 4 знаками после запятой.
    """
    return round(number, 4)

def generate_random_number():
    """
    Генерирует случайное число в диапазоне (0, 1] с округлением до 4 знаков после запятой.

    ### Возвращаемое значение:
    * `float` - Случайное число в диапазоне (0, 1] с 4 знаками после запятой.
    """
    while True:
        number = round_value(random.random())
        if number > 0:
            return number

def calculate_time(alfa: int, number: float) -> float:
    """
    Возвращает время между двумя последовательными заявками.

    ### Параметры:
    * `alfa (int)` - Параметр для расчета интервалов между заявками.
    * `number (float)` - Случайное число, использованное для расчета интервала.

    ### Возвращаемое значение:
    * `float` - Время между двумя последовательными заявками с 4 знаками после запятой.
    """
    return round_value(-1/alfa * math.log(number))

def calculate_mean_served_requests(results):
    """
    Вычисляет среднее количество обслуженных заявок по результатам симуляции.

    ### Параметры:
    * `results (list[SimulationResult])` - Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.

    ### Возвращаемое значение:
    * `float` - Среднее количество обслуженных заявок с 4 знаками после запятой.
    """
    total_served_requests = [result.served_requests for result in results]
    return round_value(sum(total_served_requests) / len(total_served_requests))