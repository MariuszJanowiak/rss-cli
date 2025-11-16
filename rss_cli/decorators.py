import time
import functools
from collections import deque
from typing import Callable, Type

def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            result = time.perf_counter() - start
            print(f"[timer] {func.__name__} execution time: {result:.2f}s")
    return wrapper

def retry(exceptions: tuple[Type[BaseException], ...], tries: int = 3, delay: int = 1):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(0, tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"[retry] {func.__name__} failed (attempt {attempt}/{tries}): {e}")
                    if attempt < tries:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

def rate_limit(max_calls: int, time_limit: int):
    def decorator(func: Callable) -> Callable:
        calls = deque() # deque collection as a cache does object easiest to manage
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic() # Monotonic time generator used to keep clock consistent
            while calls and now - calls[0] > time_limit:
                calls.popleft()
            if len(calls) >= max_calls:
                sleep_time = time_limit - (now - calls[0])
                if sleep_time > 0:
                    print(f"[rate_limit] waiting {sleep_time:.2f}s before calling {func.__name__}")
                    time.sleep(sleep_time)
            calls.append(time.monotonic())
            return func(*args, **kwargs)
        return wrapper
    return decorator