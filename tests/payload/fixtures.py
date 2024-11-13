import signal


def handler(signum, frame):
    raise TimeoutError("Test took too long to execute")


def execute_timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm

        return wrapper

    return decorator
