"""
Тесты для задачи «Calm down».
"""
import pytest
import time

try:
    from solution.task5 import calmer
except ImportError:
    pytest.skip("Task 1 has not been implemented yet", allow_module_level=True)


def test_without_arguments():
    """
    Testing without arguments
    """

    @calmer
    def test_func():
        return "Called"

    assert test_func() == "Called"
    time.sleep(1)  # Sleep for 1 second as default max_rate is 1
    assert test_func() == "Called"


@pytest.mark.parametrize("rate", [0.5, 1, 2])
def test_different_rates(rate):
    """
    Testing different rates
    """

    @calmer(max_rate=rate)
    def test_func():
        return "Called"

    assert test_func() == "Called"
    time.sleep(1 / rate)
    assert test_func() == "Called"


@calmer
def start_timer_default_rate(start_time):
    """
    Function for calculating passed msc for default rate
    """
    passed_msc = (time.time_ns() - start_time) / (10**6)
    return passed_msc


@calmer(max_rate=4)
def start_timer_rate_four(start_time):
    """
    Function for calculating passed msc for `max_rate=4`
    """
    passed_msc = (time.time_ns() - start_time) / (10**6)
    return passed_msc


def calc_period(rate):
    """
    Function for calculating period based on given rate
    """
    return 1000 / rate


def test_five_calls_default_rate():
    """
    Testing 5 calls with default rate
    """
    period = calc_period(1)
    start_time = time.time_ns()

    assert abs(0 - start_timer_default_rate(start_time)) <= 25

    for call_iter in range(5):
        assert abs(period - start_timer_default_rate(start_time)) <= 50
        start_time = time.time_ns()


def test_ten_calls_rate_four():
    """
    Testing 10 calls with `max_rate=4`
    """
    period = calc_period(4)
    start_time = time.time_ns()
    assert abs(0 - start_timer_rate_four(start_time)) <= 25

    for call_iter in range(10):
        assert abs(period - start_timer_rate_four(start_time)) <= 50
        start_time = time.time_ns()


def test_high_frequency_calls():
    """
    Testing high frequency calls in between
    """

    @calmer(max_rate=5)
    def test_func():
        return time.time()

    start_times = []
    for _ in range(10):
        start_times.append(test_func())

    for i in range(1, len(start_times)):
        assert start_times[i] - start_times[i - 1] >= 0.2
