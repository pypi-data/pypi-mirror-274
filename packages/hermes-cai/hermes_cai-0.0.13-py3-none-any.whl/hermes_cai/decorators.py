"""Decorators for tokenizer."""
import time

from metrics import FUNCTION_LATENCY


def monitor(func):
    """Decorator for monitoring the latency of a function."""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        FUNCTION_LATENCY.labels(func.__qualname__).observe(stop - start)
        return result

    return wrapper
