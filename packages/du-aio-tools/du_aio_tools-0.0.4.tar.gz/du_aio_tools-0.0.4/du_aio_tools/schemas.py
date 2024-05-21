# -*- coding: utf-8 -*-
# @time: 2024/2/18 10:32
# @author: Dyz
# @file: schemas.py
# @software: PyCharm
import json

from pydantic import BaseModel


class BaseSchemas(BaseModel):
    """Base Schemas"""

    @staticmethod
    def dump(val):
        if isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        return val

    def value_dump(self) -> dict:
        """转换值，便于存储数据库"""
        return {k: self.dump(v) for k, v in self.dict().items()}
