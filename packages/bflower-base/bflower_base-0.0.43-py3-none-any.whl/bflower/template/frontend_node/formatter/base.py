from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from bflower.template.field.base import TemplateField


class FieldFormatter(BaseModel, ABC):
    @abstractmethod
    def format(self, field: TemplateField, name: Optional[str]) -> None:
        pass
