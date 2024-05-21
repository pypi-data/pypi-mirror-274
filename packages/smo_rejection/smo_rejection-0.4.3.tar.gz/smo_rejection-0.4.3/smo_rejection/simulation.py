from .exception import InvalidInputError, NumIterationsNegative, NumIterationsIsZero, NumChannelsNegative, NumChannelsIsZero, AlphaIsZero, AlphaNegative, ServiceTimeNegative, MaxTimeNegative
from .models import SimulationParameters
from .processing import process_iteration

def run_simulation(T: float, num_channels: int, service_time: float, num_iterations: int, alfa: int):
    """
    Запускает симуляцию обслуживания заявок с заданными параметрами.

    Параметры:
    T (float): Общее время симуляции.
    num_channels (int): Количество каналов обслуживания (потоков).
    service_time (float): Время обслуживания одной заявки.
    num_iterations (int): Количество итераций симуляции.
    alfa (int): Параметр для расчета интервалов между заявками.

    Возвращает:
    list[SimulationResult]: Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.

    Исключения:
    MaxTimeNegative: Если `T` меньше или равно нулю.
    NumChannelsNegative: Если `num_channels` меньше или равно нулю.
    NumChannelsIsZero: Если `num_channels` равно нулю.
    ServiceTimeNegative: Если `service_time` меньше или равно нулю.
    NumIterationsNegative: Если `num_iterations` меньше нуля.
    NumIterationsIsZero: Если `num_iterations` равно нулю.
    AlphaNegative: Если `alfa` меньше нуля.
    AlphaIsZero: Если `alfa` равно нулю.

    Описание:
    Функция выполняет следующие действия:
    1. Проверяет корректность входных параметров и выбрасывает соответствующее исключение в случае некорректных значений.
    2. Создает объект `SimulationParameters` с заданными параметрами.
    3. Запускает цикл по количеству итераций, на каждой итерации вызывая функцию `process_iteration` и сохраняя ее результат.
    4. Возвращает список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.
    """
    # Проверка корректности входных параметров
    if T <= 0:
        raise MaxTimeNegative("Максимальное время симуляции должно быть положительным числом.")
    if num_channels <= 0:
        raise NumChannelsNegative("Количество каналов должно быть положительным числом.")
    if num_channels == 0:
        raise NumChannelsIsZero("Количество каналов не может быть нулевым.")
    if service_time <= 0:
        raise ServiceTimeNegative("Время обслуживания должно быть положительным числом.")
    if num_iterations < 0:
        raise NumIterationsNegative("Количество итераций не может быть отрицательным.")
    if num_iterations == 0:
        raise NumIterationsIsZero("Количество итераций не может быть нулевым.")
    if alfa < 0:
        raise AlphaNegative("Альфа не может быть отрицательной")
    if alfa == 0:
        raise AlphaIsZero("Альфа не может быть равным нулю")

    # Создание объекта SimulationParameters
    params = SimulationParameters(T=T, num_channels=num_channels, service_time=service_time, num_iterations=num_iterations, alfa=alfa)
    results = []

    # Выполнение итераций симуляции
    for iteration in range(num_iterations):
        result = process_iteration(params, iteration)
        results.append(result)

    return results