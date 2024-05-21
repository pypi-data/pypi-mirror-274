from .models import SimulationParameters, SimulationResult
from .utils import generate_random_number, calculate_time

def process_iteration(params: SimulationParameters, iteration: int) -> SimulationResult:
    """
    Выполняет одну итерацию симуляции обслуживания заявок.

    Параметры:
    params (SimulationParameters): Параметры симуляции.
    iteration (int): Номер текущей итерации.

    Возвращает:
    SimulationResult: Объект, содержащий результаты текущей итерации симуляции.

    Описание:
    Функция моделирует процесс поступления и обслуживания заявок в системе с несколькими каналами обслуживания (потоками).
    На каждом шаге времени генерируется случайное значение, на основе которого рассчитывается интервал времени до следующей заявки.
    Если в момент поступления заявки есть свободный канал обслуживания, заявка обслуживается, иначе она отклоняется.
    Функция отслеживает время занятости каждого канала обслуживания и статистику обслуженных и отклоненных заявок.
    Результаты итерации сохраняются в объекте `SimulationResult`, который возвращается функцией.
    """
    T = params.T
    num_channels = params.num_channels
    service_time = params.service_time
    alfa = params.alfa

    # Инициализация переменных
    request_times = []
    service_end_times = [0] * num_channels
    served_requests = 0
    rejected_requests = 0
    request_time = 0

    while request_time < T:
        # Генерация случайного числа и расчет интервала времени до следующей заявки
        rand_value = generate_random_number()
        inter_arrival_time = calculate_time(alfa, rand_value)
        request_time += inter_arrival_time

        # Если время превышает общее время симуляции, завершить цикл
        if request_time > T:
            break

        # Найти свободный канал обслуживания
        available_server = service_end_times.index(min(service_end_times))
        if service_end_times[available_server] <= request_time:
            # Если канал свободен, обслужить заявку
            service_end_times[available_server] = request_time + service_time
            served_requests += 1
            serviced = 1
            rejected = 0
        else:
            # Иначе, отклонить заявку
            rejected_requests += 1
            serviced = 0
            rejected = 1

        # Сформировать словарь с информацией о текущей заявке
        entry = {
            'index': len(request_times) + 1,
            'rand_value': round(rand_value, 4),
            'iba': round(inter_arrival_time, 4),
            'app_time': round(request_time, 4),
            'Обслужено': serviced,
            'Отказов': rejected,
        }

        # Добавить информацию о времени окончания обслуживания на каждом канале
        for i in range(num_channels):
            key = f'server_{i + 1}'
            if serviced == 1 and available_server == i:
                entry[key] = round(service_end_times[i], 4)
            else:
                entry[key] = ''

        # Добавить информацию о текущей заявке в список
        request_times.append(entry)

    # Создать и вернуть объект SimulationResult с результатами итерации
    return SimulationResult(iteration=iteration + 1, served_requests=served_requests, rejected_requests=rejected_requests, request_times=request_times)