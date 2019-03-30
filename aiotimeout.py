import asyncio
import contextlib


@contextlib.contextmanager
def timeout(max_time):

    cancelling_due_to_timeout = False
    current_task = asyncio.current_task()
    loop = asyncio.get_event_loop()

    def cancel():
        nonlocal cancelling_due_to_timeout
        cancelling_due_to_timeout = True
        current_task.cancel()

    handle = loop.call_later(max_time, cancel)

    try:
        yield
    except asyncio.CancelledError:
        if not cancelling_due_to_timeout:
            raise
        else:
            raise asyncio.TimeoutError()
    finally:
        handle.cancel()
