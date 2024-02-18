import asyncio

from asgiref.sync import async_to_sync
from celery import Celery

from circuit_breaker import CircuitBreaker


circuit_breaker_a = CircuitBreaker(error_threshold=3)
circuit_breaker_b = CircuitBreaker(error_threshold=3)
app = Celery('tasks', broker='redis://localhost:6379/0')


async def _task_a(message):
    await asyncio.sleep(1)
    print(f"Success task executed: {message}")
    return "Success"


async def _task_b(message):
    if message == "error":
        raise Exception("task_b was failed")

    await asyncio.sleep(1)
    print(f"Success task executed: {message}")
    return "Success"


@app.task(name='task_a')
def task_a(message):
    print(f"task_a msg: {message}")

    with circuit_breaker_a:
        return async_to_sync(_task_a)(message)


@app.task(name='task_b')
def task_b(message):
    print(f"task_b msg: {message}")

    with circuit_breaker_b as cb:
        if cb.state == "open":
            print("CircuitBreaker is opened, skip task_b")
        else:
            print("CircuitBreaker is closed, execute task_b")
            return async_to_sync(_task_b)(message)
