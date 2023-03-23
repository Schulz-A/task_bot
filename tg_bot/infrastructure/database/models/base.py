from typing import Dict, Any

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def get_attributes(self) -> Dict[Any, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __str__(self):
        attributes = ' | '.join(f'{k}={v}' for k, v in self.get_attributes().items())
        return f'{self.__class__.__qualname__}({attributes})'

    def __repr__(self):
        attributes = ' | '.join(f'{k}={v}' for k, v in self.get_attributes().items())
        return f'{self.__class__.__qualname__}({attributes})'