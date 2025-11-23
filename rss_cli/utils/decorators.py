import os
import time
import functools
import logging
from collections import deque
from typing import Callable, Type

logger = logging.getLogger(__name__)

### Connection
def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            result = time.perf_counter() - start
            logger.info("[timer] %s execution time: %.2fs", func.__name__, result)
    return wrapper

def retry(exceptions: tuple[Type[BaseException], ...], tries: int = 3, delay: int = 1):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error: BaseException | None = None
            for attempt in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    logger.warning(
                        "[retry] %s failed (attempt %s/%s): %s",
                        func.__name__, attempt, tries, e,
                    )
                    if attempt < tries:
                        time.sleep(delay)
            assert last_error is not None
            raise last_error
        return wrapper
    return decorator

def rate_limit(max_calls: int, time_limit: int):
    def decorator(func: Callable) -> Callable:
        calls = deque()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            while calls and now - calls[0] > time_limit:
                calls.popleft()

            if len(calls) >= max_calls:
                sleep_time = time_limit - (now - calls[0])
                if sleep_time > 0:
                    logger.info(
                        "[rate_limit] waiting %.2fs before calling %s",
                        sleep_time, func.__name__,
                    )
                    time.sleep(sleep_time)

            calls.append(time.monotonic())
            return func(*args, **kwargs)

        return wrapper
    return decorator
