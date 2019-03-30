# aiotimeout [![CircleCI](https://circleci.com/gh/michalc/aiotimeout.svg?style=svg)](https://circleci.com/gh/michalc/aiotimeout) [![Test Coverage](https://api.codeclimate.com/v1/badges/8de540239bd7d6566f58/test_coverage)](https://codeclimate.com/github/michalc/aiotimeout/test_coverage)

Timeout context manager for asyncio Python


## Usage

```python
from aiotimeout import timeout

# Will raise an asyncio.TimeoutError
with timeout(1):
    await asyncio.sleep(1.5)

# Will not raise anything
with timeout(1):
    await asyncio.sleep(0.5)
```


## Differences to alternatives

- `asyncio.wait_for` does not offer a context manager. In some cases a context manager is clearer.

- `asyncio.wait_for` creates/uses an extra task. In some cases this is not necessary, and an extra task adds non-determinism in terms of sequence of operations.

- Clearer internal code [in the author's opinion]. Rather than a custom class, [contextlib.contextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) is used.
