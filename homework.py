from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.'
                                  % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUNNING_VALUE_1: ClassVar[int] = 18
    RUNNING_VALUE_2: ClassVar[int] = 20
    HOURS_IN_MIN: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUNNING_VALUE_1
                 * self.get_mean_speed()
                 - self.RUNNING_VALUE_2)
                * self.weight
                / self.M_IN_KM
                * (self.duration
                * self.HOURS_IN_MIN))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SW_VALUE_1: ClassVar[float] = 0.035
    SW_VALUE_2: ClassVar[float] = 0.029
    SW_VALUE_3: ClassVar[int] = 2
    HOURS_IN_MIN: ClassVar[int] = 60

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.SW_VALUE_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.SW_VALUE_3
                 // self.height)
                * self.SW_VALUE_2
                * self.weight)
                * (self.duration
                * self.HOURS_IN_MIN))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    SWIMMING_VALUE_1: ClassVar[float] = 1.1
    SWIMMING_VALUE_2: ClassVar[int] = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SWIMMING_VALUE_1)
                * self.SWIMMING_VALUE_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_train = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in parameters_train:
        return parameters_train[workout_type](*data)
    else:
        for i in parameters_train.keys():
            print(f'Доступны следующие виды тренировки: {i}')


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
