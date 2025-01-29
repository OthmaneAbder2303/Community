import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds to execute.")
        return result

    return wrapper

@timing_decorator
def slow_function():
    time.sleep(2)
    return "I am a slow function."

print(slow_function())
