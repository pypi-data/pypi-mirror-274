from enum import Enum
from logging import getLogger

logger = getLogger(__name__)


class DeclaredVariable:
    def __init__(self, name: str, required: bool):
        self.name = name
        self.required = required


class Variable:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value


class Settings:
    def __init__(self):
        pass

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class LLMProvider(Enum):
    azure = "azure"
    aws = "aws"


def camel_to_snake(name):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
