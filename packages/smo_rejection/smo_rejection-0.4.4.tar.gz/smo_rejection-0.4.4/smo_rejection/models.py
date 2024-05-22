from dataclasses import dataclass

@dataclass
class SimulationParameters:
    """
    Класс для хранения параметров симуляции.

    ### Атрибуты:
    * `T (float)` - Общее время симуляции.
    * `num_channels (int)` - Количество каналов обслуживания (потоков).
    * `service_time (float)` - Время обслуживания одной заявки.
    * `num_iterations (int)` - Количество итераций симуляции.
    * `alfa (int)` - Параметр для расчета интервалов между заявками.
    """
    T: float
    num_channels: int
    service_time: float
    num_iterations: int
    alfa: int

@dataclass
class SimulationResult:
    """
    Класс для хранения результатов симуляции.

    ### Атрибуты:
    * `iteration (int)` - Номер итерации симуляции.
    * `served_requests (int)` - Количество обслуженных заявок.
    * `rejected_requests (int)` - Количество отклоненных заявок.
    * `request_times (list)` - Список, содержащий информацию о каждой заявке, включая время поступления, случайное значение, интервал между заявками, занятость серверов и статус обслуживания.
    """
    iteration: int
    served_requests: int
    rejected_requests: int
    request_times: list