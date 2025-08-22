from __future__ import annotations
from typing import *
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import time


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.memory_storage = {}
        
    async def __call__(
        self,
        handler,
        event: Message | CallbackQuery,
        data: dict
    ):
        # Basit memory-based throttling
        user_id = event.from_user.id
        current_time = time.time()
        
        if user_id in self.memory_storage:
            last_request = self.memory_storage[user_id]
            if current_time - last_request < 1:  # 1 saniye throttling
                return
        
        self.memory_storage[user_id] = current_time
        return await handler(event, data)
