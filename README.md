# Async CSV Logger

This module is intented to be a csv logger which will write to file async-ly.
This is especially useful for logging performance (e.g. benchmarking some algorithms) at each iteration/time-step.

Internally, it utilise threading to write to async write to file.
There are two way to initialise and use the logger.


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
