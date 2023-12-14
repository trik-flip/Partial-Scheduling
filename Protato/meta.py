from typing import Any


class Singleton(type):
    _instances: dict[Any, Any] = dict()

    def __call__(cls: Any, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TimerException(Exception):
    pass
