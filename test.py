import asyncio
import unittest 

from aiofastforward import (
    FastForward,
)
from aiotimeout import (
    timeout,
)


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestTimeout(unittest.TestCase):

    @async_test
    async def test_shorter_than_timeout_not_raises(self):
            loop = asyncio.get_event_loop()

            async def worker():
                with timeout(1):
                    await asyncio.sleep(0.5)

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(0.5)
                await task

    @async_test
    async def test_longer_than_timeout_raises_timeout_error(self):
            loop = asyncio.get_event_loop()

            async def worker():
                with timeout(1):
                    await asyncio.sleep(1.5)

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(1)
                with self.assertRaises(asyncio.TimeoutError):
                    await task

    @async_test
    async def test_cancel_raises_cancelled_error(self):
            loop = asyncio.get_event_loop()

            async def worker():
                with timeout(1):
                    await asyncio.sleep(0.5)

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(0.25)
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task

    @async_test
    async def test_exception_propagates(self):
            loop = asyncio.get_event_loop()

            async def worker():
                with timeout(2):
                    raise Exception('inner')

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(1)
                with self.assertRaisesRegex(Exception, 'inner'):
                    await task

    @async_test
    async def test_cleanup(self):
            loop = asyncio.get_event_loop()
            cleanup = asyncio.Event()

            async def worker():
                with timeout(1):
                    try:
                        await asyncio.sleep(2)
                    except asyncio.CancelledError:
                        cleanup.set()
                        raise

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(1)
                with self.assertRaises(asyncio.TimeoutError):
                    await task

                self.assertTrue(cleanup.is_set())

    @async_test
    async def test_ignore_timeout(self):
            loop = asyncio.get_event_loop()
            ignored = asyncio.Event()

            async def worker():
                with timeout(1):
                    try:
                        await asyncio.sleep(2)
                    except asyncio.CancelledError:
                        # Swallow the exception
                        pass
                ignored.set()

            with FastForward(loop) as forward:
                task = asyncio.ensure_future(worker())

                await forward(1)
                await task
                self.assertTrue(ignored.is_set())
