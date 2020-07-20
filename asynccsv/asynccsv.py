import csv
import datetime
import os
import threading
import warnings
from multiprocessing import Queue


class AsyncCSVLogger:
    """
    An async CSV logger class that encapsulate writing list to csv file async-ly.
    """

    class AsyncWriterThread(threading.Thread):
        """
        A threading class to perform async file writing.
        """

        def __init__(self, queue, args):
            """
            Initialise a thread to async write to file.

            :param queue: Python Queue object, for this thread to get job
            :param filename: String for the file name of the csv file to write into
            """
            super().__init__()
            self.queue = queue
            self.filename, acquire_lock = args
            self.lock = None
            if acquire_lock:
                import filelock

                self.lock = filelock.FileLock(f"{self.filename}.lock")

        def run(self):
            while True:
                contents = self.queue.get()
                if contents is None:
                    return  # join
                if self.lock is not None:
                    self.lock.acquire()

                with open(self.filename, "a") as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(contents)

                if self.lock is not None:
                    self.lock.release()

    def __init__(
        self,
        filename,
        log_timestamp=False,
        exist_ok=False,
        overwrite_exist=False,
        acquire_lock=False,
    ):
        """
        Initialise a logger object that async-ly write given list to csv file.

        :param filename: Filename for the csv file to write into
        :param log_timestamp: whether or not include a timestamp while logging
        :param exist_ok: If set to False, the given filename cannot exists beforehand
        :param overwrite_exist: If set to True, it overwrites existing file (assume
                                exist_ok)
        :param acquire_lock: If set to True, it will use thread lock
        """
        if overwrite_exist:
            exist_ok = True
        if not exist_ok and os.path.exists(filename):
            raise FileExistsError(
                f"File {filename} already exists! Set 'exist_ok=True' to allow it."
            )
        # try to create an empty file
        file_mode = "a"
        if overwrite_exist:
            file_mode = "w"
        open(filename, file_mode).close()
        self.log_timestamp = log_timestamp
        self._previous_field_num = None
        self.queue = Queue()
        self.async_writer = AsyncCSVLogger.AsyncWriterThread(
            self.queue, (filename, acquire_lock)
        )
        self.filename = filename
        self.async_writer.start()

    def write(self, contents):
        """
        Given a list of content, this function will async write them to a csv file.

        :param contents: List of content to write into csv file
        """
        if not isinstance(contents, list):
            raise ValueError("Given contents must be in a list")
        if self._previous_field_num is not None and self._previous_field_num != len(
            contents
        ):
            warnings.warn(
                f"Different number of fields are given! "
                f"Previous field has {self._previous_field_num} items, but now is {len(contents)}."
            )
        self._previous_field_num = len(contents)

        if self.log_timestamp:
            now = datetime.datetime.now().strftime("%m:%d-%H:%M:%S.%f")
            contents.insert(0, now)
        self.queue.put(contents)

    def write_title(self, titles):
        """
        Given a list of content, this function will write the title only if no content
        exist in the file. (i.e. will not write title twice)

        :param titles: List of titles to write into csv file
        """
        if os.stat(self.filename).st_size == 0:
            # it is an empty file, let's write the titles into file
            if self.log_timestamp:
                # add the timestamps title
                titles.insert(0, "Timestamps")
                self.log_timestamp = False
                self.write(titles)
                self.log_timestamp = True
            else:
                self.write(titles)

    def close(self):
        """
        This will join all threads.
        This should be called if the object is initialised without 'with' block.
        """
        # send request for thread to stop executing
        self.queue.put(None)
        self.async_writer.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    with AsyncCSVLogger("path_of_your_log.csv", log_timestamp=True) as logger:
        print("a")
        logger.write(["d ,sd s,d", 223, 'sad"sd"sad""",asd,asd,'])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
        logger.write([1, 323, 2, 3])
