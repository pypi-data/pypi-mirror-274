class InvalidInputError(Exception):
    """Исключение для недопустимых входных значений."""
    pass

class SimulationError(Exception):
    """Исключение для ошибок во время симуляции."""
    pass

class NumIterationsNegative(Exception):
    """Исключение выбрасывается, если количество итераций отрицательное."""
    pass

class NumIterationsIsZero(Exception):
    """Исключение выбрасывается, если количество итераций равно нулю."""
    pass

class NumChannelsNegative(Exception):
    """Исключение выбрасывается, если количество каналов отрицательное."""
    pass

class NumChannelsIsZero(Exception):
    """Исключение выбрасывается, если количество каналов равно нулю."""
    pass

class AlphaIsZero(Exception):
    """Исключение выбрасывается, если параметр alpha равен нулю."""
    pass

class AlphaNegative(Exception):
    """Исключение выбрасывается, если параметр alpha отрицательный."""
    pass

class ServiceTimeNegative(Exception):
    """Исключение выбрасывается, если время обслуживания отрицательное."""
    pass

class MaxTimeNegative(Exception):
    """Исключение выбрасывается, если максимальное время симуляции отрицательное."""
    pass
