# Async CSV Logger
[![PyPI](https://img.shields.io/pypi/v/asynccsv.svg)](https://pypi.python.org/pypi/asynccsv)

This module is a async csv logger that helps you log performance of your algorithm.


## Description

This module is intented to be a csv logger which will write to file async-ly.

With the hope to have minimum performance impact on benchmarking your algorithm (i.e. I/O blocking to write to disk), this is especially useful for logging performance at each iteration/time-step. Internally, it utilise threading to async write to file.

There are two way to initialise and use the logger.


## Install

```
pip install asynccsv
```


### 1. Recommended way (with block)

```python
from asynccsv import AsyncCSVLogger

with AsyncCSVLogger('path_of_your_log.csv') as logger:
    # csv titles
    logger.write(['Time', 'Accuracy', 'Num of nodes'])

    # do your other stuff
    # ......

    import datetime
    for i in range(10):
        # perform calculation
        # ....
        # write results to file
        logger.write([datetime.datetime.now(), acc, num_nodes])
```


### 2. The normal way

```python
from asynccsv import AsyncCSVLogger

class MyAwesomeAlgorithm():

    def __init__(self):
        # with the 'log_timestamp' flag it will automatically log timestamp
        self.logger = AsyncCSVLogger('path_of_your_log.csv', log_timestamp=True)

    def run(self):
        # perform calculation
        # ...
        logger.write([acc, num_nodes])


if __name__ == '__main__':
    awesome = MyAwesomeAlgorithm()
    for i in range(10):
        awesome.run()

    # You SHOULD run this to properly close the threading and force
    # everything to be written to disk
    # This is automatically done by the 'with' block in previous example
    awesome.logger.close()
```
