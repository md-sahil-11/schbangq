from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple(
            [
                (enum.value, name.replace("_", " ").capitalize())
                for name, enum in cls.__members__.items()
            ]
        )

    @classmethod
    def get_enum(cls, name):
        return cls.__members__[name]

    @classmethod
    def get_description(cls, value):
        return dict(cls.choices()).get(value)


class IntEnum(int, BaseEnum):
    pass


class CharEnum(str, BaseEnum):
    pass


class TaskTypeChoices(CharEnum):
    GENERAL = "general"
    TRAINING = "training"


class TaskPriorityChoices(CharEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskRewardChoices(IntEnum):
    P10 = 10
    P20 = 20
    P50 = 50
    P100 = 100
    P200 = 200