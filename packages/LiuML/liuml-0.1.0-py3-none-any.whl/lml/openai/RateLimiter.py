#!/usr/bin/python3
# -*- coding: utf-8 -*-
import asyncio
import time
from functools import wraps


class FunctionDecorator(object):
    """
    Converts rate limiter into a function decorator.
    """

    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter

    def __call__(self, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            async with self.rate_limiter.limit(**kwargs):
                return await func(*args, **kwargs)

        # Return either an async or normal wrapper, depending on the type of the wrapped function
        return async_wrapper


class ContextManager(object):
    """
    Converts rate limiter into context manager.
    """

    def __init__(self, num_tokens, rate_limiter):
        self.num_tokens = num_tokens
        self.rate_limiter = rate_limiter

    async def __aenter__(self):
        await self.rate_limiter.wait_for_capacity(self.num_tokens)

    async def __aexit__(self, *exc):
        return False


class Bucket(object):
    def __init__(self, rate_limit):
        # Per-second rate limit
        self._rate_per_sec = rate_limit / 60

        # Capacity of the bucket
        self._capacity = rate_limit / 60

        # Last time the bucket capacity was checked
        self._last_checked = time.time()

    def _has_capacity(self, amount):
        current_time = time.time()
        time_passed = current_time - self._last_checked

        self._last_checked = current_time
        self._capacity += time_passed * self._rate_per_sec
        self._capacity = min(self._capacity, 60 * self._rate_per_sec)

        if self._rate_per_sec < 1 and amount <= 1:
            return True

        if self._capacity < amount:
            return False

        self._capacity -= amount
        return True

    async def wait_for_capacity(self, amount):
        while not self._has_capacity(amount):
            await asyncio.sleep(1 / self._rate_per_sec)


class AsyncRateLimiter(object):
    def __init__(self, request_limit, token_limit, token_counter):
        # Rate limits
        self.request_limit = request_limit
        self.token_limit = token_limit

        # Token counter
        self.token_counter = token_counter

        # Buckets
        self._request_bucket = Bucket(request_limit)
        self._token_bucket = Bucket(token_limit)

    async def wait_for_capacity(self, num_tokens):
        await asyncio.gather(
            self._token_bucket.wait_for_capacity(num_tokens),
            self._request_bucket.wait_for_capacity(1)
        )

    def limit(self, **kwargs):
        num_tokens = self.token_counter(**kwargs)
        return ContextManager(num_tokens, self)

    def is_limited(self):
        return FunctionDecorator(self)
