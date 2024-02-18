import time
from itertools import cycle
from random import choice

from tasks import task_a, task_b


MESSAGES = {
    "task_a": ("Message for task a",),
    "task_b": ("error",)
}


def receive_and_dispatch_messages():
    for msg, body in cycle(MESSAGES.items()):
        body = choice(body)

        if msg == "task_a":
            task_a.delay(body)
        elif msg == "task_b":
            task_b.delay(body)

        time.sleep(5)


if __name__ == "__main__":
    receive_and_dispatch_messages()
