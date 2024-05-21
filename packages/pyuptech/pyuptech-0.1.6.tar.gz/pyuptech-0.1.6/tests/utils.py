from time import perf_counter_ns


def time_it(func):
    def wrapper(*args, **kwargs):
        temp_list = []
        result = None
        for _ in range(10):
            start_time = perf_counter_ns()

            result = func(*args, **kwargs)
            elapsed_time = perf_counter_ns() - start_time
            temp_list.append(elapsed_time)
        return result, sum(temp_list) / len(temp_list)

    return wrapper
