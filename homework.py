from typing import Dict, List, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"%.3f" % self.duration} ч.; '
                f'Дистанция: {"%.3f" % self.distance} км; '
                f'Ср. скорость: {"%.3f" % self.speed} км/ч; '
                f'Потрачено ккал: {"%.3f" % self.calories}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1
                 * self.get_mean_speed() - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.coeff_calorie_2 * self.weight)
                * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    typeof: Dict[str, Type[Training]] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking}
    return typeof.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
